from pathlib import Path
from natsort import natsorted
from typing import List, Union

def get_sorted_list_of_files(folder_path: Path, extension_filter: str = None) -> list:
	if extension_filter:
		return natsorted([
			str(f) for f in folder_path.rglob('*') if f.suffix.lower() == extension_filter
		])
	else:
		return natsorted([str(f) for f in folder_path.glob('*')])

def split_summary(summary: str, max_length: int = 4000) -> List[str]:
    chunks, current_chunk, current_length = [], '', 0
    for line in summary.splitlines(True):
        line_length = len(line)

        if current_length + line_length <= max_length:
            current_chunk += line
            current_length += line_length
        else:
            chunks.append(current_chunk)
            current_chunk = line
            current_length = line_length

    chunks.append(current_chunk)
    return chunks


def generate_summary(folder_path: Union[str, Path]) ->  str:
    def video_summary(summary: str, folder: Path, indent: int = 1) -> None:
        for path in natsorted(folder.glob('*')):
            if path.is_file() and path.suffix.lower() == '.mp4':
                summary += f"#F{folder_path_filtered.index(str(path))} "
            elif path.is_dir():
                if [f for f in list(path.rglob('*')) if f.suffix.lower() == '.mp4']:
                    summary += '\n' # Try to fix bug that occurs when files are not in a folder
                    summary += "=" * indent + f" {path.name}\n"
                    summary = video_summary(summary, path, indent + 1)

        return summary + '\n\n'

    folder_path = Path(folder_path)
    folder_path_filtered = get_sorted_list_of_files(folder_path, '.mp4')
    lines = video_summary('', folder_path).splitlines(True)
    lines = [line.replace(' \n', '\n') for line in lines]
    summary = ''.join(l for l in lines)
    summary = (summary.replace('\n' * 5, '\n' * 3)
                .replace('\n' * 4, '\n' * 3)
                .replace('\n' * 3, '\n' * 2) # Try to fix bug that occurs when files are not in a folder
                .rstrip('\n'))
    return summary