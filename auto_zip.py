import os
import shutil
import zipfile
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from halo import Halo

threads = 4

def compress_directory(src_dir, zip_name, total_size, zip_folder):
    # Caminho completo para o arquivo zip
    zip_file_path = os.path.join(zip_folder, zip_name)

    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_STORED) as zipf:
        with tqdm(total=total_size, desc=f"Compactando {zip_name}", unit="B", unit_scale=True) as pbar:            
            for root, _, files in os.walk(src_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, src_dir)
                    zipf.write(file_path, arcname)
                    pbar.update(os.path.getsize(file_path))

def create_subfolders(files, max_size):
    subfolders = []
    current_subfolder = []
    current_size = 0
    for file, size in sorted(files.items(), key=lambda item: -item[1]):
        if current_size + size > max_size:
            if current_subfolder:
                subfolders.append(current_subfolder)
                current_subfolder = []
                current_size = 0
        current_subfolder.append(file)
        current_size += size
    if current_subfolder:
        subfolders.append(current_subfolder)
    return subfolders

def generate_zip_name(base_name, index):
    return f"{base_name}_parte_{index:02}.zip"

def prepare_files_for_upload(folder_path, threads):
    if not os.path.isdir(folder_path):
        raise ValueError(f"O caminho especificado não é um diretório: {folder_path}")
    base_folder_name = os.path.basename(folder_path.rstrip("\\/"))  
    zip_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zip_files")
    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder)
    files = {os.path.join(root, file): os.path.getsize(os.path.join(root, file))
             for root, dirs, files in os.walk(folder_path)
             for file in files if not file.endswith('.mp4')}
    
    if not files:
        print("Não há arquivos a serem zipados.")
        return

    spinner = Halo(text='Dividindo pastas...', spinner='dots', color='magenta')
    spinner.start()
    subfolders = []
    temp_folders = []
    try:
        subfolders = create_subfolders(files, 1900 * (1024 ** 2))  # 1900 MB

        for index, subfolder in enumerate(subfolders, start=1):
            temp_folder = os.path.join(zip_folder, f"temp_folder_{index}")
            os.makedirs(temp_folder, exist_ok=True)

            total_size = sum(files[file] for file in subfolder)
            temp_folders.append((temp_folder, total_size))
            
            for file in subfolder:
                relative_path = os.path.relpath(file, folder_path)
                dest_path = os.path.join(temp_folder, relative_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy(file, dest_path)
                
        spinner.succeed("Pastas divididas com sucesso!")
    except Exception as e:
        spinner.fail("Erro ao dividir as pastas.")
        print(e)
        return

    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [
                executor.submit(
                    compress_directory, 
                    temp_folder, 
                    generate_zip_name(base_folder_name, index), 
                    total_size,
                    zip_folder  # Adiciona o caminho da pasta zip_folder
                ) for index, (temp_folder, total_size) in enumerate(temp_folders, start=1)
            ]            
            for future in futures:
                future.result()

        print("Compactação concluída com sucesso!")
    except Exception as e:
        print("Erro durante a compactação.")
        print(e)

    for temp_folder, _ in temp_folders:
        shutil.rmtree(temp_folder)

    print("Arquivos preparados para upload!")