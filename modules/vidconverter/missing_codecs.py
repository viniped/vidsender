import os
import subprocess

def has_video_codec(file_path):
    ffprobe_cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(file_path)
    ]

    try:
        result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        codec_name = result.stdout.strip()
        return codec_name != ""
    except subprocess.CalledProcessError:
        return False

def delete_files_with_missing_video_codecs(folder_path):
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_path.lower().endswith((".mp4", ".ts", ".mpg", ".mpeg", ".avi", ".mkv", ".flv", ".3gp", ".rmvb", ".webm", ".vob", ".ogv", ".rrc",
                                      ".gifv", ".mng", ".mov", ".qt", ".wmv", ".yuv", ".rm", ".asf", ".amv", ".m4p", ".m4v", ".mp2", ".mpe",
                                      ".mpv", ".m4v", ".svi", ".3g2", ".mxf", ".roq", ".nsv", ".f4v", ".f4p", ".f4a", ".f4b")):
                if not has_video_codec(file_path):
                    print(f"Deleting {file_path} (missing video codec)")
                    os.remove(file_path)