import os
import subprocess
from pathlib import Path

def has_duration(file_path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(file_path)], capture_output=True, text=True)
    duration = result.stdout.strip()
    return duration != ""


def delete_videos_without_duration(folder_path):
    folder_path = Path(folder_path)
    for path in folder_path.rglob('*.mp4'):
        if path.is_file() and not has_duration(path):
            print(f"Deleting {path}")
            os.remove(str(path))
