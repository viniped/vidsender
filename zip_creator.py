import os
import sys
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from halo import Halo
import platform

threads = 4

def resource_path(relative_path):
    """Resolve o caminho corretamente para recursos em modo .py e modo PyInstaller (.exe)"""
    try:
        base_path = sys._MEIPASS  # quando for executável PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # quando for script Python
    return os.path.join(base_path, relative_path)

bin_path = resource_path('bin')

def get_executable_path(executable_name):
    """Retorna o caminho do executável, usando a pasta local 'bin' se for Windows."""
    if platform.system() == 'Windows':
        exe_path = os.path.join(bin_path, f"{executable_name}.exe")
        if os.path.isfile(exe_path):
            return exe_path
        else:
            raise FileNotFoundError(f"Executável '{exe_path}' não encontrado.")
    else:
        return shutil.which(executable_name)

def compress_directory_with_7zip(src_dir, zip_name, zip_folder, part_size_mib):
    zip_file_path = os.path.join(zip_folder, zip_name)   
    seven_zip_executable = get_executable_path('7z')

    command = [
        seven_zip_executable, 'a', 
        '-tzip',  # Define o formato como zip
        f'-v{part_size_mib}m',  # Define o tamanho da parte em MiB
        zip_file_path, 
        os.path.join(src_dir, '*')
    ]

    subprocess.run(command, check=True)

def prepare_files_for_upload(folder_path, threads):
    if not os.path.isdir(folder_path):
        raise ValueError(f"O caminho especificado não é um diretório: {folder_path}")

    base_folder_name = os.path.basename(folder_path.rstrip("\\/"))
    zip_folder = os.path.join(os.getcwd(), "zip_files")


    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder)

    temp_folder = os.path.join(zip_folder, 'temp_folder')
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    os.makedirs(temp_folder)

    materiais_folder = os.path.join(temp_folder, 'materiais')
    os.makedirs(materiais_folder)

    for root, _, files in os.walk(folder_path):
        for file in files:
            if not file.endswith('.mp4'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)
                dest_path = os.path.join(materiais_folder, relative_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy(file_path, dest_path)

    if not any(os.scandir(materiais_folder)):
        print("Não há arquivos a serem zipados.")
        return

    spinner = Halo(text='Compactando arquivos...', spinner='dots', color='magenta')
    spinner.start()

    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [
                executor.submit(
                    compress_directory_with_7zip, 
                    temp_folder, 
                    f"{base_folder_name}.zip",  
                    zip_folder, 
                    1900  
                )
            ]

            for future in futures:
                future.result()

        spinner.succeed("Compactação concluída com sucesso!")
    except Exception as e:
        spinner.fail("Erro durante a compactação.")
        print(e)
        return
    finally:
        shutil.rmtree(temp_folder)

    print("Arquivos preparados para upload!")
