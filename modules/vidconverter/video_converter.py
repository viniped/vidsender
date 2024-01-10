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

    if video_codec == "h264" and audio_codec == "aac" and file_path.lower().endswith(".mp4"):
        return

    cmd = [
        'ffmpeg',
        '-v', 'quiet',
        '-stats',
        '-y',
        '-i', file_path,
        '-b:a', '128k',
        '-hide_banner'
          
    ]  
     
    if video_codec == "h264" and audio_codec == "aac":
        cmd.extend(['-c:v', 'copy', '-c:a', 'copy'])
    
    elif video_codec != "h264" and audio_codec == "aac":
        cmd.extend(['-c:v', 'libx264', '-preset', 'ultrafast', '-threads', '2', '-c:a', 'copy','-crf', '23', '-maxrate', '4M'])

    elif video_codec == "h264" and audio_codec != "aac":
        cmd.extend(['-c:v', 'copy', '-c:a', 'aac', '-preset', 'ultrafast', '-threads', '2','-crf', '23', '-maxrate', '4M'])
    elif video_codec != "h264" and audio_codec != "aac":
        cmd.extend(['-c:v', 'h264', '-c:a', 'aac', '-preset', 'ultrafast', '-threads', '2','-crf', '23', '-maxrate', '4M'])
    else:        
        cmd.extend(['-c:v', 'h264', '-c:a', 'aac', '-preset', 'ultrafast', '-threads', '2','-crf' '23', '-maxrate' '4M'])
   
   
    output_file = f"{os.path.splitext(file_path)[0]}_conv.mp4"
    cmd.append(output_file)
    
    print(cmd)
    subprocess.run(cmd)
    os.remove(file_path)

def convert_videos_in_folder(folder_path):
    delete_videos_without_duration(folder_path)
    
    spinner = Halo(text='Verificando vídeos para conversão...', spinner='dots')
    spinner.start()

    videos_to_convert = []

    for subdir, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".mp4", ".ts", ".mpg", ".mpeg", ".avi", ".mkv", ".flv", ".3gp", ".rmvb", ".webm", ".vob", ".ogv", ".rrc",
                                      ".gifv", ".mng", ".mov", ".qt", ".wmv", ".yuv", ".rm", ".asf", ".amv", ".m4p", ".m4v", ".mp2", ".mpe",
                                      ".mpv", ".m4v", ".svi", ".3g2", ".mxf", ".roq", ".nsv", ".f4v", ".f4p", ".f4a", ".f4b")):
                file_path = os.path.join(subdir, file)
                video_codec = get_codec(file_path, 'v')
                audio_codec = get_codec(file_path, 'a')
                
                if not (video_codec == "h264" and audio_codec == "aac" and file_path.lower().endswith(".mp4")):
                    videos_to_convert.append(file_path)

    spinner.stop()

    total_videos = len(videos_to_convert)
    
    if total_videos == 0:
        print("Todos os vídeos já estão no formato correto.")
        return
    else:
        print(f"{total_videos} vídeos precisam ser convertidos.")

    for index, video_path in enumerate(videos_to_convert):
        remaining_videos = total_videos - index
        print(f"Vídeos restantes: {remaining_videos}")
        convert_file(video_path)

    print("A conversão dos vídeos foi concluída.")