import os
import json
import time
import subprocess
from ffmpy import FFmpeg, FFprobe
from pyrogram import Client, errors
from pathlib import Path
from natsort import natsorted
from typing import Tuple, Union
from utils import delete_residual_files, Banner, show_banner
from modules.channel_description import generate_description
from modules.summary_generator import generate_summary
from auto_zip import prepare_files_for_upload
from modules.vidconverter.video_converter import convert_videos_in_folder
from modules.video_splitter import split_videos

def clean_console():
    os.system('clear || cls')

def progress(current, total, *args):
    os.system('clear || cls')
    print(f"{args[0]}:", f"{current * 100 / total:.1f}%")

def update_channel_info(client: Client, ch_desc: str, ch_tile: str) -> Tuple[int, str, str]:
    dest_id = client.create_channel(ch_tile).id    
    invite_link = client.export_chat_invite_link(dest_id)
    ch_desc = ch_desc + f'\nConvite: {invite_link}'
    time.sleep(10)
    client.set_chat_description(dest_id, ch_desc)

    # Assuming you want to enable protection for all channels
    try:
        client.set_chat_protected_content(dest_id, True)
    except errors.ChatNotModified:
        pass

    return dest_id, ch_desc, invite_link

class VideoUploader:
    def __init__(self, folder_path: str, chat_id: Union[str, int] = None) -> None:
        self.folder_path = folder_path
        self.chat_id = chat_id
        self.ch_id = None

    def init_session(self, session_name: str = "user") -> None:
        try:
            self.client = Client(session_name)
            self.client.start()
        except (AttributeError, ConnectionError):
            phone_number = input("\nEnter your phone number: ")
            api_id = int(input("Enter your API ID: "))
            api_hash = input("Enter your API hash: ")

            self.client = Client(
                session_name=session_name,
                api_id=api_id,
                api_hash=api_hash.strip(),
                phone_number=phone_number.strip()
            )
            self.client.start()
    
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

    def generate_thumbnail(self, video_path: str) -> str:
        thumbnail_path = video_path + "_thumb.jpg"
        ff = FFmpeg(
            inputs={video_path: None},
            outputs={thumbnail_path: '-ss 00:00:02 -vframes 1 -loglevel panic'}
        )
        ff.run()
        return thumbnail_path

    def upload_files(self) -> None:
        # 1. Obter todas as pastas dentro do folder_path
        subfolders = [f for f in Path(self.folder_path).iterdir() if f.is_dir()]
        sorted_subfolders = natsorted(subfolders, key=lambda folder: folder.name)

        # Definindo o nome do canal uma vez baseado no nome da pasta fornecida
        if not self.chat_id:
            title = Path(self.folder_path).name
            self.ch_id, ch_desc, invite_link = update_channel_info(self.client, generate_description(self.folder_path), title)
        else:
            self.ch_id = int(self.chat_id) if self.chat_id.lstrip('-').isdigit() else self.chat_id

        file_count = 1  # Initialize file_count outside the loop

        for folder in sorted_subfolders:
            # 2. Para cada pasta, obter todos os arquivos de vídeo
            video_files = [f for f in folder.rglob('*') if f.is_file() and f.suffix.lower() == '.mp4']
            sorted_files = natsorted(video_files, key=lambda file: file.name)

            for video_path in sorted_files:
                metadata = self.collect_video_metadata(str(video_path))
                
                if 'streams' in metadata:
                    video_stream = next((stream for stream in metadata['streams'] if stream['codec_type'] == 'video'), None)
                    if video_stream:
                        width = int(video_stream['width'])
                        height = int(video_stream['height'])
                        duration = int(float(video_stream['duration']))
                    else:
                        width, height, duration = None, None, None
                else:
                    continue  # Skip this iteration if 'streams' key is not in metadata
                    
                thumbnail_path = self.generate_thumbnail(str(video_path))
                with open(thumbnail_path, 'rb') as thumb, open(video_path, "rb") as video_file:
                    caption = f"#F{file_count:02} {video_path.name}"
                    file_count += 1  # Increment file_count

                    self.client.send_video(
                        self.ch_id,
                        video_file,
                        width=width,
                        height=height,
                        duration=duration,
                        caption=caption,
                        progress=progress,
                        progress_args=(video_path.name,),
                        thumb=thumb
                    )

                # Após o envio, podemos excluir a miniatura para economizar espaço
                os.remove(thumbnail_path)


    def upload_zip_files(self):
        zip_folder = Path("zip_files")
        
        if not zip_folder.exists():
            print(f"Pasta {zip_folder} não encontrada!")
            return
        
        zip_files = [f for f in zip_folder.rglob('*') if f.is_file() and f.suffix == '.zip']
        
        if not zip_files:
            print("Nenhum arquivo .zip encontrado na pasta zip_files!")
            return

        print(f"{len(zip_files)} arquivos .zip encontrados. Iniciando o upload...")
        
        index = 1
        for zip_file in zip_files:
            with open(zip_file, "rb") as file:
                caption = f"#M{index:02} {zip_file.name}"
                try:
                    self.client.send_document(self.ch_id, file, caption=caption)
                    zip_file.unlink()
                    
                except Exception as e:
                    print(f"Erro ao enviar {zip_file.name}. Erro: {str(e)}")
                index += 1

        # Send summary and pin message                
        summary = generate_summary(self.folder_path)
        sent_msg = self.client.send_message(self.ch_id, summary)
        self.client.pin_chat_message(self.ch_id, sent_msg.id)
                    
show_banner()
folder_path = input("Informe o caminho da pasta que deseja fazer o upload: ")
delete_residual_files(folder_path)
clean_console()
prepare_files_for_upload(folder_path)
convert_videos_in_folder(folder_path)
split_videos(folder_path, size_limit="2 GB", delete_corrupted_video=True)
uploader = VideoUploader(folder_path)
uploader.init_session()
uploader.upload_files()
uploader.upload_zip_files()