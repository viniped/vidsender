import os
import json
import shutil
import time
import subprocess
from modules.renamer import *
import modules.utils as utils
from unidecode import unidecode
from ffmpy import FFmpeg, FFprobe
from pyrogram import Client, errors
from pathlib import Path
from natsort import natsorted
from typing import Tuple, Union
from modules.channel_description import generate_description
from modules.summary_generator import *
from zip_creator import prepare_files_for_upload
from modules.vidconverter.video_converter import convert_videos_in_folder
from modules.video_splitter import split_videos
from modules.vidconverter.missing_codecs import delete_files_with_missing_video_codecs
from concurrent.futures import ThreadPoolExecutor
from modules.desc_utils import edit_desc_file

conf = utils.json_load('config.json')
sticker_id = conf['unique_id']
channel_ids = conf['channel_ids']
threads = conf['threads']
thumbnail_path = Path('templates/thumb.jpg')
path_to_input = 'input'
letra = utils.load_letra_sumario()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def send_sticker(client: Client, chat_ids, unique_id):
    if not isinstance(chat_ids, list):
        chat_ids = [chat_ids]
    for chat_id in chat_ids:
        try:
            client.send_sticker(chat_id, unique_id)
        except Exception as e:
            print(f"Erro ao enviar para {chat_id}: {e}")

def progress(current, total, video_number, total_videos, start_time):
    clear()
    upload_percentage = (current * 100) / total
    elapsed_time = time.time() - start_time
    upload_speed_mbps = (current * 8) / (1024 * 1024 * elapsed_time)
    total_size_mb = total / (1024 * 1024)
    print(f"Uploading video {video_number}/{total_videos} {upload_percentage:.1f}% of {total_size_mb:.2f} MB at {upload_speed_mbps:.2f} Mbps")

def update_channel_info(client: Client, ch_desc: str, ch_tile: str) -> Tuple[int, str, str]:
    dest_id = client.create_channel(ch_tile).id
    invite_link = client.export_chat_invite_link(dest_id)
    ch_desc = ch_desc + f'\nConvite: {invite_link}'
    time.sleep(10)
    client.set_chat_description(dest_id, ch_desc)

    try:
        client.set_chat_protected_content(dest_id, True)
    except errors.ChatNotModified:
        pass
    return dest_id, ch_desc, invite_link

def send_invite(client_bot: Client, channel_ids: List[Union[str, int]], folder_path: str, invite_link: str, ch_desc: str):
    cover_path = Path(folder_path) / 'cover.jpg'
    desc_path = Path(folder_path) / 'desc.txt'

    if desc_path.exists():
        edit_desc_file(desc_path)

    # Read the content of desc.txt if it exists
    if desc_path.exists():
        with open(desc_path, 'r', encoding='utf-8') as file:
            desc_content = file.read()
            # Concatenate the channel title and the contents of desc.txt
            invite_desc = f"{Path(folder_path).name}\n\n{ch_desc}\n\n{desc_content}"
    else:
        invite_desc = f"{Path(folder_path).name}\n\n{ch_desc}"

    invite_desc += f"\n\n🔗 **Acesse Aqui:** [Clique para entrar]({invite_link})"

    message_ids = []

    for channel_id in channel_ids:
        if cover_path.exists():
            with open(cover_path, 'rb') as photo:
                message_id = client_bot.send_photo(
                    chat_id=channel_id,
                    photo=photo,
                    caption=invite_desc  
                ).id
                message_ids.append(message_id)
        else:
            message_id = client_bot.send_message(
                chat_id=channel_id,
                text=invite_desc
            ).id
            message_ids.append(message_id)

    return message_ids

def generate_thumbnail(video_path: str) -> str:
    thumbnail_path = f"{video_path}_thumb.jpg"
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)  # Remove the existing thumbnail if it exists
    ff = FFmpeg(
        inputs={video_path: None},
        outputs={thumbnail_path: '-ss 00:00:02 -vframes 1 -loglevel panic'}
    )
    ff.run()
    return thumbnail_path

class VideoUploader:
    def __init__(self, client: Client, folder_path: str, chat_id: Union[str, int] = None, upload_status=None) -> None:
        self.client = client
        self.folder_path = folder_path
        self.chat_id = chat_id
        self.upload_status = upload_status if upload_status else self.read_upload_status(folder_path)
        self.invite_link = None  # Inicializando invite_link como None

    @staticmethod
    def read_upload_status(folder_path):
        json_filename = f"{Path(folder_path).stem}_upload_plan.json"
        try:
            with open(Path('projects') / json_filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"channel_id": None, "videos": {}}

    def write_upload_status(self):
        json_filename = f"{Path(self.folder_path).stem}_upload_plan.json"
        os.makedirs('projects', exist_ok=True)
        with open(Path('projects') / json_filename, 'w', encoding='utf-8') as file:
            json.dump(self.upload_status, file, ensure_ascii=False, indent=4)

    def update_video_status(self, video_path, status):
        self.upload_status["videos"][video_path]["status"] = status
        self.write_upload_status()

    def collect_video_metadata(self, video_path: str) -> dict:
        if Path(video_path).suffix.lower() != ".mp4":
            return {}

        ffprobe_cmd = FFprobe(
            inputs={video_path: None},
            global_options=['-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams']
        )
        result = ffprobe_cmd.run(stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        output_str = result[0].decode('utf-8').strip()
        metadata = json.loads(output_str)
        return metadata

    def format_summary_from_template(self, summary: str) -> str:
        template_path = Path('templates/summary_template.txt')
        with open(template_path, 'r', encoding='utf-8') as template_file:
            template = template_file.read()
            return template.format(summary_content=summary)

    def upload_files(self):
        upload_status = self.upload_status
        sorted_videos = sorted(
            [(video_path, upload_status["videos"][video_path]["index"]) 
            for video_path in upload_status["videos"] if upload_status["videos"][video_path]["status"] == 0],
            key=lambda x: x[1]
        )  

        # Verifica ou cria o canal para upload
        if not self.chat_id:
            if self.upload_status["channel_id"]:
                self.ch_id = self.upload_status["channel_id"]
            else:
                title = Path(self.folder_path).name
                self.ch_id, ch_desc, invite_link = update_channel_info(
                    self.client, generate_description(self.folder_path), title
                )
                self.upload_status["channel_id"] = self.ch_id
                self.write_upload_status()
        else:
            self.ch_id = int(self.chat_id) if self.chat_id.lstrip('-').isdigit() else self.chat_id

        # Processa os vídeos em ordem do plano de upload
        total_videos = len(sorted_videos)
        for video_path, index in sorted_videos:
            full_path = Path(video_path)
            video_str_path = str(full_path)

            # Verifica se o vídeo já foi enviado
            if self.upload_status["videos"][video_str_path]["status"] == 1:
                continue

            # Coleta os metadados do vídeo
            metadata = self.collect_video_metadata(video_str_path)
            if 'streams' in metadata:
                video_stream = next((stream for stream in metadata['streams'] if stream['codec_type'] == 'video'), None)
                if video_stream:
                    width = int(video_stream['width'])
                    height = int(video_stream['height'])
                    duration = int(float(video_stream['duration']))
                else:
                    width, height, duration = None, None, None
            else:
                continue  # Pula vídeos que não puderem ser analisados

            # Obtém o thumbnail ou gera um novo se necessário
            thumbnail_path = Path('templates/thumb.jpg')
            if not thumbnail_path.exists():
                thumbnail_path = generate_thumbnail(str(full_path))

            # Envia o vídeo
            with open(thumbnail_path, 'rb') as thumb, open(video_path, "rb") as video_file:
                caption = f"#{letra}{index:02} {full_path.name}"
                start_time = time.time()

                self.client.send_video(
                    self.ch_id,
                    video_file,
                    width=width,
                    height=height,
                    duration=duration,
                    caption=caption,
                    progress=progress,
                    progress_args=(index, total_videos, start_time),
                    thumb=thumb
                )

            # Remove o thumbnail temporário
            os.remove(thumbnail_path)

            # Atualiza o status do vídeo no plano de upload
            self.update_video_status(video_str_path, 1)

    def upload_zip_files(self):
        zip_folder = Path("zip_files")

        if not zip_folder.exists():
            print(f"Pasta {zip_folder} não encontrada!")
            return

        zip_files = sorted([f for f in zip_folder.rglob('*') if f.is_file() and re.match(r'.*\.zip\..*', f.name)], key=lambda f: f.stem)

        if not zip_files:
            print("Nenhum arquivo .zip encontrado na pasta zip_files!")
            return

        print(f"{len(zip_files)} arquivos .zip encontrados. Iniciando o upload...")

        for index, zip_file in enumerate(zip_files, start=1):
            caption = f"#M{index:02} {zip_file.name}"
            try:
                start_time = time.time()  # Adiciona a variável start_time

                def progress_wrapper(current, total, file_index=index, total_files=len(zip_files)):
                    progress(current, total, file_index, total_files, start_time)

                self.client.send_document(
                    self.ch_id,
                    zip_file,
                    caption=caption,
                    progress=progress_wrapper,
                )

            except Exception as e:
                print(f"Erro ao enviar {zip_file.name}. Erro: {str(e)}")

        summary = generate_summary(self.folder_path)
        formatted_summary = self.format_summary_from_template(summary)

        max_length = 4000
        if len(formatted_summary) > max_length:
            summaries = split_summary(formatted_summary, max_length)
            for idx, s in enumerate(summaries):
                sent_msg = self.client.send_message(self.ch_id, s)
                if idx == 0:
                    self.client.pin_chat_message(self.ch_id, sent_msg.id)
        else:
            sent_msg = self.client.send_message(self.ch_id, formatted_summary)
            self.client.pin_chat_message(self.ch_id, sent_msg.id)

def create_upload_plan(folder_path: str):
    """
    Cria um plano de upload para todos os vídeos dentro da pasta especificada,
    independentemente da estrutura de subpastas.
    """
    json_filename = f"{Path(folder_path).stem}_upload_plan.json"
    upload_plan_path = Path('projects') / json_filename

    if not upload_plan_path.exists():
        video_paths = [str(video_path) for video_path in Path(folder_path).rglob('*.mp4')]            
        normalized_paths = [unidecode(path) for path in video_paths]            
        sorted_paths = natsorted(normalized_paths)
        videos = {video_path: {"status": 0, "index": i + 1} for i, video_path in enumerate(sorted_paths)}
        upload_status = {"channel_id": None, "videos": videos}
        os.makedirs('projects', exist_ok=True)
        with open(upload_plan_path, 'w', encoding='utf-8') as file:
            json.dump(upload_status, file, ensure_ascii=False, indent=4)
        return upload_status
    else:
        return VideoUploader.read_upload_status(folder_path)

def main():
    session_user_path = Path('sessions') / 'user'
    session_bot_path = Path('sessions') / 'bot'  
    client = Client(str(session_user_path))
    client_bot = Client(str(session_bot_path))
    utils.clean_console()                        
    utils.show_banner()
    utils.authenticate()
    client.start()
    path_to_input = "input"
    rename_files_and_folders(path_to_input)
    input_folder_path = Path("input")
    output_folder_path = Path("output")
    output_folder_path.mkdir(exist_ok=True)


    for folder in input_folder_path.iterdir():
        if folder.is_dir():
            folder_path = str(folder)
            upload_status = VideoUploader.read_upload_status(folder_path)
            if not upload_status["videos"]:
                utils.clear_directory('zip_files')
                utils.clean_console()
                delete_files_with_missing_video_codecs(folder_path)
                convert_videos_in_folder(folder_path)        
                split_videos(folder_path, size_limit="2 GB", delete_corrupted_video=True)
                utils.generate_report(folder_path)
                prepare_files_for_upload(folder_path,   4)
                upload_status = create_upload_plan(folder_path)
                

            uploader = VideoUploader(client, folder_path, upload_status=upload_status)            
            uploader.upload_files()
            uploader.upload_zip_files()
            invite_link = client.export_chat_invite_link(uploader.ch_id)
            ch_desc = generate_description(folder_path)
            client_bot.start()
            if channel_ids :
                send_invite(client_bot, channel_ids, folder_path, invite_link, ch_desc)
                send_sticker(client_bot, channel_ids, sticker_id)
            else:
                pass
            client_bot.stop()
            shutil.move(folder_path, output_folder_path / folder.name)
            print(f"Pasta {folder.name} movida para 'output'")

    client.stop()

if __name__ == "__main__":
    main()

    while True:
        main()
        input('Finished. Press enter to restart')
