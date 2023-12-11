from ffmpy import FFmpeg, FFprobe
from pathlib import Path
import subprocess, math

video_formats = ['.3g2', '.3gp', '.avi', '.flv', '.m4v', '.mkv', '.wmv',
                        '.mov', '.mp4', '.mpeg', '.mpg', '.ogv', '.webm']

def split_video_by_duration(video_path, max_duration):
    output_directory = video_path.parent
    output_base_name = video_path.stem + "_part"
    output_format = video_path.suffix
    parts_count = int(get_video_duration(video_path) / max_duration) + 1

    outputs = str(output_directory / (output_base_name + "%d" + output_format))
    outputs_options = (f'-hide_banner -c copy -map 0 -segment_time {max_duration} -f segment '
                                    f'-reset_timestamps 1 -segment_format {output_format} -y')
    try:
        FFmpeg(inputs={str(video_path): None}, outputs={outputs: outputs_options}).run()
        video_path.unlink()
        print(f"Successfully split {video_path} into {parts_count} parts.")
    except Exception as e:
        print(f"Failed to split {video_path}: {e}")

def convert_size_to_bytes(size_str: str):
    size_str = size_str.lower().replace(" ", "")
    unit_multipliers = {
        'kb': 10 ** 3, 'mb': 10 ** 6,
        'gb': 10 ** 9, 'tb': 10 ** 12
    }
    for unit, multiplier in unit_multipliers.items():
        if size_str.endswith(unit):
            size = float(size_str[:-2]) * multiplier
            return int(size)
    return int(size_str)

def get_video_size(video_path):
    try:
        ffprobe_cmd = FFprobe(
            inputs={str(video_path): None},
            global_options=['-v', 'error', '-show_entries', 'format=size',
                                '-of', 'default=noprint_wrappers=1:nokey=1']
        )
        result = ffprobe_cmd.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return int(result[0].strip())
    except Exception as e:
        print(f"Failed to get size of {video_path}: {e}")
        return None

def get_video_duration(video_path: Path):
    try:
        ffprobe_cmd = FFprobe(
            inputs={str(video_path): None},
            global_options=['-v', 'error', '-show_entries', 'format=duration',
                                    '-of', 'default=noprint_wrappers=1:nokey=1']
        )
        result = ffprobe_cmd.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return float(result[0].strip())
    except Exception as e:
        print(f"Failed to get duration of {video_path}: {e}")
        return None

def calculate_max_duration(video_path, video_size, size_limit):
    video_duration = get_video_duration(video_path)
    if not video_duration:
        return None
    parts_count = math.ceil(video_size / size_limit)
    return math.ceil(video_duration / parts_count)

def split_videos(folder_path, size_limit="1.9 GB", delete_corrupted_video=True):
    size_limit = convert_size_to_bytes(size_limit)
    for path in Path(folder_path).rglob('*'):
        if path.is_file() and path.suffix.lower() in video_formats:
            video_size = get_video_size(path)
            max_duration = calculate_max_duration(path, video_size, size_limit)
            if max_duration and video_size > size_limit:
                split_video_by_duration(path, max_duration)