import os
import json
import shutil
import time
import subprocess
from modules.renamer import *
from unidecode import unidecode
from ffmpy import FFmpeg, FFprobe
from pyrogram import Client, errors
from pathlib import Path
from natsort import natsorted
from typing import Tuple, Union
import modules.utils as utils
from modules.channel_description import generate_description
from modules.summary_generator import *
from zip_creator import prepare_files_for_upload
from modules.vidconverter.video_converter import convert_videos_in_folder
from modules.video_splitter import split_videos
from modules.vidconverter.missing_codecs import delete_files_with_missing_video_codecs
from concurrent.futures import ThreadPoolExecutor

threads = 4
path_to_input = 'input'
letra = utils.load_letra_sumario()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    time.sleep(20)
    client.set_chat_description(dest_id, ch_desc)

    try:
        client.set_chat_protected_content(dest_id, True)
    except errors.ChatNotModified:
        pass
    return dest_id, ch_desc, invite_link

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
        self.invite_link = None

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
        folder_path = Path(self.folder_path)

        if not self.chat_id:
            if self.upload_status["channel_id"]:
                self.ch_id = self.upload_status["channel_id"]
            else:
                title = folder_path.name
                self.ch_id, ch_desc, self.invite_link = update_channel_info(self.client, generate_description(folder_path), title)
                self.upload_status["channel_id"] = self.ch_id
                self.write_upload_status()
        else:
            self.ch_id = int(self.chat_id) if self.chat_id.lstrip('-').isdigit() else self.chat_id

        if not self.invite_link:
            self.invite_link = self.client.export_chat_invite_link(self.ch_id)

        video_paths = [
            video_path for video_path, metadata in self.upload_status["videos"].items()
            if metadata["status"] == 0  
        ]

        if not video_paths:
            print("Nenhum vídeo pendente para upload.")
            return

        video_paths = sorted(
            video_paths,
            key=lambda video: self.upload_status["videos"][video]["index"]
        )

        for video_path in video_paths:
            
            full_path = Path(video_path)

            if not full_path.exists():  
                print(f"Arquivo não encontrado: {full_path}")
                input("Pressione Enter para continuar...")

            print(f"Iniciando upload do vídeo: {video_path}")

            metadata = self.collect_video_metadata(str(full_path))

            if not metadata or 'streams' not in metadata:
                print(f"Metadados inválidos para o vídeo: {video_path}")
                continue

            video_stream = next((stream for stream in metadata['streams'] if stream['codec_type'] == 'video'), None)
            if video_stream:
                width = int(video_stream['width'])
                height = int(video_stream['height'])
                duration = int(float(video_stream['duration']))
            else:
                width, height, duration = None, None, None

            thumbnail_path = Path('templates/thumb.jpg')
            if not thumbnail_path.exists():
                thumbnail_path = generate_thumbnail(str(full_path))

            with open(thumbnail_path, 'rb') as thumb, open(full_path, "rb") as video_file:
                current_video = self.upload_status["videos"][video_path]["index"]
                caption = f"#{letra}{current_video:02} {full_path.name}"

                start_time = time.time()

                self.client.send_video(
                    self.ch_id,
                    video_file,
                    width=width,
                    height=height,
                    duration=duration,
                    caption=caption,
                    progress=progress,
                    progress_args=(current_video, len(video_paths), start_time),
                    thumb=thumb,
                )

            os.remove(thumbnail_path)
            self.update_video_status(video_path, 1)

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
                start_time = time.time()  
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

#        print(f"Generated summary: {summary}")
#        print(f"Formatted summary: {formatted_summary}")
#        input('Press enter to continue...')

        max_length = 4000
        if len(formatted_summary) > max_length:
            summaries = split_summary(formatted_summary, max_length)
            for idx, s in enumerate(summaries):
                sent_msg = self.client.send_message(self.ch_id, s,disable_web_page_preview=True)
                if idx == 0:
                    self.client.pin_chat_message(self.ch_id, sent_msg.id)
        else:
            sent_msg = self.client.send_message(self.ch_id, formatted_summary, disable_web_page_preview=True)
            self.client.pin_chat_message(self.ch_id, sent_msg.id)

def create_upload_plan(folder_path: str):
    """
    Cria ou lê o plano de upload para pastas e subpastas, garantindo que o nome do plano
    e do canal seja baseado na pasta principal diretamente abaixo de 'input'.
    """
    folder_path = Path(folder_path)
    main_folder = folder_path if folder_path.parent.name == "input" else Path(path_to_input) / folder_path.parts[1]

    json_filename = f"{main_folder.stem}_upload_plan.json"
    upload_plan_path = Path('projects') / json_filename

    if not upload_plan_path.exists():
        video_paths = [
            str(video_path.relative_to(path_to_input))
            for video_path in main_folder.rglob('*.mp4') 
        ]

        if not video_paths:
            print(f"Nenhum vídeo encontrado em: {main_folder}")
            return {"channel_id": None, "videos": {}}

        sorted_paths = natsorted(video_paths)

        videos = {
            f"input/{video_path}": {"status": 0, "index": i + 1}
            for i, video_path in enumerate(sorted_paths)
        }

        upload_status = {"channel_id": None, "videos": videos}

        os.makedirs('projects', exist_ok=True)

        with open(upload_plan_path, 'w', encoding='utf-8') as file:
            json.dump(upload_status, file, ensure_ascii=False, indent=4)

        print(f"Plano de upload criado para {main_folder.name}: {upload_plan_path}")
        return upload_status
    else:
        print(f"Plano de upload já existe para {main_folder.name}: {upload_plan_path}")
        return VideoUploader.read_upload_status(main_folder)

def process_folder_or_subfolders(client, folder_path):
    """
    Processa a pasta atual verificando se ela contém vídeos diretamente ou subpastas,
    e move a pasta principal para 'output' após o processamento.
    """
    folder_path = Path(folder_path)
    if not folder_path.is_dir():
        return

    subfolders = [f for f in folder_path.iterdir() if f.is_dir()]
    if subfolders:

        for subfolder in natsorted(subfolders, key=lambda f: str(f)):
            print(f"Processing subfolder: {subfolder}")
            process_folder_or_subfolders(client, subfolder)
    else:

        print(f"Processing folder with videos: {folder_path}")
        process_videos_in_folder(client, folder_path)

    main_folder = folder_path if folder_path.parent.name == "input" else Path(path_to_input) / folder_path.parts[1]
    if folder_path == main_folder: 
        output_folder = Path("output") / main_folder.name
        if not output_folder.exists():  
            shutil.move(main_folder, output_folder)
            print(f"Pasta principal {main_folder.name} movida para 'output' com subpastas intactas.")

def process_videos_in_folder(client, folder_path):
    """
    Processa uma pasta contendo vídeos diretamente ou em subpastas,
    garantindo que o plano de upload seja gerado e os vídeos sejam enviados.
    """
    folder_path = Path(folder_path)
    main_folder = folder_path if folder_path.parent.name == "input" else Path(path_to_input) / folder_path.parts[1]
    upload_status = VideoUploader.read_upload_status(main_folder)
    if not upload_status["videos"]:  # Se não houver vídeos no plano, criar
        utils.clear_directory('zip_files')
        delete_files_with_missing_video_codecs(main_folder)
        convert_videos_in_folder(main_folder)
        split_videos(main_folder, size_limit="2 GB", delete_corrupted_video=True)
        utils.generate_report(main_folder)
        prepare_files_for_upload(main_folder, threads)
        upload_status = create_upload_plan(main_folder)

    uploader = VideoUploader(client, main_folder, upload_status=upload_status)
    uploader.upload_files()
    uploader.upload_zip_files()

    print(f"Uploads concluídos para a pasta {main_folder.name}")

def main():
    session_user_path = Path('sessions') / 'user'
    session_bot_path = Path('sessions') / 'bot'
    client = Client(str(session_user_path))
    client_bot = Client(str(session_bot_path))
    clear()
    utils.show_banner()
    utils.authenticate()
    client.start()
    input_folder_path = Path("input")
    output_folder_path = Path("output")
    output_folder_path.mkdir(exist_ok=True)
    rename_files_and_folders(path_to_input)

    for folder in input_folder_path.iterdir():
        if folder.is_dir():
            print(f"Processing folder: {folder}")
            process_folder_or_subfolders(client, folder)

    client.stop()

if __name__ == "__main__":
    main()
    while True:
        main()
        input('Finished. Press enter to restart')
