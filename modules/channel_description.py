import os
import json
import subprocess

def get_video_info(file_path: str) -> dict:
    ffprobe_command = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]

    try:
        output = subprocess.check_output(ffprobe_command).decode('utf-8')
        metadata = json.loads(output)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return {}

    return metadata

def get_total_size_and_duration(folder_path: str):
    total_size = 0
    total_duration = 0
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.mp4'):  # Verifica a extensão do arquivo
                file_path = os.path.join(root, file)
                metadata = get_video_info(file_path)
                total_size += os.path.getsize(file_path)
                if metadata and 'format' in metadata and 'duration' in metadata['format']:
                    total_duration += float(metadata['format']['duration'])
                else:
                    print(f"File not selected {file_path}.")

    return total_size, total_duration

def generate_description(folder_path: str) -> str:
    total_size, total_duration = get_total_size_and_duration(folder_path)
    
    # Converter o tamanho total para GB
    total_size_gb = total_size / (1024 ** 3)
    
    # Converter a duração total para horas e minutos
    hours = int(total_duration // 3600)
    minutes = int((total_duration % 3600) // 60)
    
    description = (
        f"Tamanho: {total_size_gb:.2f} gb\n"
        f"Duração: {hours}h {minutes}min"
    )
    
    return description.strip()
