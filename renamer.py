import os
import re
from unidecode import unidecode

def sanitize_name(name):
    sanitized_name = unidecode(name)
    sanitized_name = re.sub(r'[<>:"/\\|?*]', ' ', sanitized_name)
    return sanitized_name

def rename_files_and_folders(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            sanitized_name = sanitize_name(name)
            if sanitized_name != name:
                os.rename(os.path.join(root, name), os.path.join(root, sanitized_name))

        for name in dirs:
            sanitized_name = sanitize_name(name)
            if sanitized_name != name:
                os.rename(os.path.join(root, name), os.path.join(root, sanitized_name))