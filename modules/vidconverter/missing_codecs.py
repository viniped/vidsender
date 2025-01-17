import os
import subprocess

def has_video_codec(file_path):
    """
    Verifica se o arquivo possui codec de vídeo usando ffprobe.
    """
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
    """
    Exclui arquivos de vídeo que não possuem codec de vídeo, usando os.scandir.
    """
    video_extensions = {".mp4", ".ts", ".mpg", ".mpeg", ".avi", ".mkv", ".flv", ".3gp", ".rmvb", ".webm", ".vob", 
                        ".ogv", ".rrc", ".gifv", ".mng", ".mov", ".qt", ".wmv", ".yuv", ".rm", ".asf", ".amv", ".m4p", 
                        ".m4v", ".mp2", ".mpe", ".mpv", ".svi", ".3g2", ".mxf", ".roq", ".nsv", ".f4v", ".f4p", 
                        ".f4a", ".f4b"}

    def scan_directory(path):
        """
        Escaneia o diretório atual e processa os arquivos recursivamente.
        """
        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        # Recursão para subdiretórios
                        scan_directory(entry.path)
                    elif entry.is_file() and entry.name.lower().endswith(tuple(video_extensions)):
                        if not has_video_codec(entry.path):
                            print(f"Deleting {entry.path} (missing video codec)")
                            os.remove(entry.path)
        except PermissionError:
            print(f"Permission denied: {path}")
    scan_directory(folder_path)