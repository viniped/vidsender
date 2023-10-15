import os
import subprocess
from modules.vidconverter.utils import delete_videos_without_duration

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

    # Verifica se a conversão é necessária
    if file_path.lower().endswith("_conv.mp4"):
        return

    cmd = [
        'ffmpeg',
        '-v', 'quiet',
        '-stats',
        '-y',
        '-i', file_path,
        '-b:a', '128k'
    ]

     # se video_codec = h264 e audio_codec = aac copiar ambos os codecs
    if video_codec == "h264" and audio_codec == "aac":
        cmd.extend(['-c:v', 'copy', '-c:a', 'copy'])
    # se video_codec diferente de h264 e audio codec = aac transformar codec de video para h264 e copiar o codec de audio
    elif video_codec != "h264" and audio_codec == "aac":
        cmd.extend(['-c:v', 'libx264', '-preset', 'ultrafast', '-threads', '2', '-c:a', 'copy','-crf', '23', '-maxrate', '4M'])
    # se audio_codec diferente de aac e video_codec = h264 transformar codec de audio para aac e copiar o codec de video
    elif video_codec == "h264" and audio_codec != "aac":
        cmd.extend(['-c:v', 'copy', '-c:a', 'aac', '-preset', 'ultrafast', '-threads', '2','-crf', '23', '-maxrate', '4M'])
    elif video_codec != "h264" and audio_codec != "aac":
        cmd.extend(['-c:v', 'h264', '-c:a', 'aac', '-preset', 'ultrafast', '-threads', '2','-crf', '23', '-maxrate', '4M'])
    else:        
        cmd.extend(['-c:v', 'h264', '-c:a', 'aac', '-preset', 'ultrafast', '-threads', '2','-crf' '23', '-maxrate' '4M'])
   
    output_file = f"{os.path.splitext(file_path)[0]}_conv.mp4"
    cmd.append(output_file)
    
    subprocess.run(cmd)
    os.remove(file_path)

def convert_videos_in_folder(folder_path):
    delete_videos_without_duration(folder_path)
    
    # Flag para rastrear se há vídeos para converter
    videos_to_convert = False
    
    for subdir, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".mp4", ".ts", ".mpg", ".mpeg", ".avi", ".mkv", ".flv", ".3gp", ".rmvb", ".webm", ".vob", ".ogv", ".rrc",
                                      ".gifv", ".mng", ".mov", ".qt", ".wmv", ".yuv", ".rm", ".asf", ".amv", ".m4p", ".m4v", ".mp2", ".mpe",
                                      ".mpv", ".m4v", ".svi", ".3g2", ".mxf", ".roq", ".nsv", ".f4v", ".f4p", ".f4a", ".f4b")):
                file_path = os.path.join(subdir, file)
                convert_file(file_path)
                if not file_path.lower().endswith("_conv.mp4"):
                    videos_to_convert = True

    # Verifica se há vídeos para converter antes de imprimir a mensagem
    if not videos_to_convert:
        print("there are no videos to convert")
