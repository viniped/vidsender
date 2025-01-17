import os
import re
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
                #summary += f"#F{folder_path_filtered.index(str(path))} "
                summary += f"#F{folder_path_filtered.index(str(path)) + 1:02} "
            elif path.is_dir():
                if [f for f in list(path.rglob('*')) if f.suffix.lower() == '.mp4']:
                    summary += '\n'  # Try to fix bug that occurs when files are not in a folder
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
               .replace('\n' * 3, '\n' * 2)  # Try to fix bug that occurs when files are not in a folder
               .rstrip('\n'))

    # Process the "zip_files" folder
    zip_root = Path("zip_files")
    zip_summary = ""
    #zip_entries = [entry for entry in zip_root.iterdir() if entry.is_file() and entry.suffix == '.zip']
    zip_entries = [entry for entry in zip_root.iterdir() if entry.is_file() and re.match(r'.*\.zip\..*', entry.name)]

    for i, entry in enumerate(zip_entries):
        zip_summary += f"#M{i+1:02} "

    # Add to the summary only if there are .zip files in the "zip_files" folder
    if zip_summary:
        summary += "\n\n== Materiais do Curso\n\n"
        summary += zip_summary.rstrip() + "\n"

    return summary
