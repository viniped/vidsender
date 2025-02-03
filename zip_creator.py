import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from halo import Halo
import platform

threads = 4

bin_path = os.path.join(os.path.dirname(__file__), 'bin')

def get_executable_path(executable_name):
    """Returns the appropriate path for an executable based on the operating system."""
    if platform.system() == 'Windows':
        return os.path.join(bin_path, f"{executable_name}.exe")
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
    # Verifica se o folder_path é um diretório
    if not os.path.isdir(folder_path):
        raise ValueError(f"O caminho especificado não é um diretório: {folder_path}")

    # O nome base é extraído do nome da pasta fornecida
    base_folder_name = os.path.basename(folder_path.rstrip("\\/"))

    # Caminho para o diretório onde os arquivos zip serão salvos
    zip_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zip_files")

    # Cria o diretório zip_folder se ele não existir
    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder)

    # Cria uma pasta temporária para copiar os arquivos não .mp4
    temp_folder = os.path.join(zip_folder, 'temp_folder')
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    os.makedirs(temp_folder)

    # Cria uma subpasta 'materiais' dentro da pasta temporária
    materiais_folder = os.path.join(temp_folder, 'materiais')
    os.makedirs(materiais_folder)

    # Copia os arquivos não .mp4 para a subpasta 'materiais'
    for root, _, files in os.walk(folder_path):
        for file in files:
            if not file.endswith('.mp4'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)
                dest_path = os.path.join(materiais_folder, relative_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy(file_path, dest_path)

    # Verifica se há arquivos na pasta 'materiais'
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
        # Remove a pasta temporária
        shutil.rmtree(temp_folder)

    print("Arquivos preparados para upload!")
