import os
import subprocess
from modules.vidconverter.utils import delete_videos_without_duration
from halo import Halo

def get_codec(file_path, stream_type):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', f'{stream_type}:0',
        '-show_entries', 'stream=codec_name',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        file_path
    ]
    codec = subprocess.check_output(cmd).decode('utf-8').strip()
    return codec

def convert_file(file_path):
    video_codec = get_codec(file_path, 'v')
    audio_codec = get_codec(file_path, 'a')

    # Skip conversion if video is already in the desired format
    if video_codec == "h264" and audio_codec == "aac" and file_path.lower().endswith(".mp4"):
        return

    cmd = [
        'ffmpeg',
        '-v', 'quiet',
        '-stats',
        '-y',
        '-i', file_path,
        '-b:a', '128k'
    ]

    if video_codec != "h264" or audio_codec != "aac":
        cmd.extend(['-c:v', 'libx264', '-c:a', 'aac', '-preset', 'ultrafast', '-threads', '2'])
    else:
        cmd.extend(['-c:v', 'copy', '-c:a', 'copy'])
   
    output_file = f"{os.path.splitext(file_path)[0]}_conv.mp4"
    cmd.append(output_file)
    
    subprocess.run(cmd)
    os.remove(file_path)

def convert_videos_in_folder(folder_path):
    delete_videos_without_duration(folder_path)
    
    videos_to_convert = False
    
    spinner = Halo(text='Verificando vídeos para conversão...', spinner='dots')
    spinner.start()

    for subdir, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".mp4", ".ts", ".mpg", ".mpeg", ".avi", ".mkv", ".flv", ".3gp", ".rmvb", ".webm", ".vob", ".ogv", ".rrc",
                                      ".gifv", ".mng", ".mov", ".qt", ".wmv", ".yuv", ".rm", ".asf", ".amv", ".m4p", ".m4v", ".mp2", ".mpe",
                                      ".mpv", ".m4v", ".svi", ".3g2", ".mxf", ".roq", ".nsv", ".f4v", ".f4p", ".f4a", ".f4b")):
                file_path = os.path.join(subdir, file)
                video_codec = get_codec(file_path, 'v')
                audio_codec = get_codec(file_path, 'a')
                
                # Se os codecs já são h264 e aac e o formato é mp4, pular conversão
                if video_codec == "h264" and audio_codec == "aac" and file_path.lower().endswith(".mp4"):
                    continue
                
                # Vídeo precisa de conversão
                spinner.stop()
                convert_file(file_path)
                videos_to_convert = True
                spinner.start()  # Reinicia o spinner para a próxima iteração
                break  # Sai do loop atual para continuar a verificação no próximo diretório

    spinner.stop()  # Para o spinner depois de verificar todos os arquivos
    
    if not videos_to_convert:
        print("Todos os vídeos já estão no formato correto.")
    else:
        print("A conversão dos vídeos foi concluída.")