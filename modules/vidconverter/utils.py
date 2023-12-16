import os
import subprocess
from pathlib import Path

def is_mp3_renamed_as_mp4(file_path):
    # Verifica se o arquivo possui características de um MP3 renomeado como MP4
    if file_path.suffix.lower() == '.mp4':
        ffprobe_cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'stream=codec_type',
            '-of', 'default=nokey=1:noprint_wrappers=1',
            str(file_path)
        ]

        try:
            result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            output = result.stdout.strip()
            return "video" not in output  # Não deve conter stream de vídeo
        except subprocess.CalledProcessError:
            return False

    return False

def delete_videos_without_duration(folder_path):
    folder_path = Path(folder_path)
    for path in folder_path.rglob('*'):
        if path.is_file() and not has_duration_and_video_stream(path) and not is_mp3_renamed_as_mp4(path):
            print(f"Deleting {path}")
            os.remove(str(path))




import os
import subprocess
from pathlib import Path

def has_duration(file_path):
    ffprobe_cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(file_path)
    ]

    try:
        result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        duration = result.stdout.strip()
        return duration != ""
    except subprocess.CalledProcessError:
        return False

def is_mp3_renamed_as_mp4(file_path):
    # Verifica se o arquivo possui características de um MP3 renomeado como MP4
    if file_path.suffix.lower() == '.mp4':
        ffprobe_cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(file_path)
        ]

        try:
            result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            duration = result.stdout.strip()
            return duration == ""
        except subprocess.CalledProcessError:
            return False

    return False

def delete_videos_without_duration(folder_path):
    folder_path = Path(folder_path)
    for path in folder_path.rglob('*.mp4'):
        if path.is_file() and is_mp3_renamed_as_mp4(path):
            print(f"Deleting {path}")
            os.remove(str(path))