import os
import shutil
import zipfile

def prepare_files_for_upload(folder_path):
    zip_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zip_files")
    base_folder_name = os.path.basename(folder_path)

    # Verificar se há arquivos que não são .mp4 para serem zipados
    has_files_to_zip = False
    for root, _, files in os.walk(folder_path):
        if any(not f.endswith('.mp4') for f in files):
            has_files_to_zip = True
            break

    if not has_files_to_zip:
        print("Não há arquivos a serem zipados.")
        return

    # Passo 1: Criar pasta zip_files se não existir
    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder)

    def get_total_size_of_folder(folder_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def generate_zip_name(base_name, index):
        return os.path.join(zip_folder, f"{base_name}_materiais_{index:02}.zip")

    def compress_directory(src_dir, zip_name):
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(src_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, src_dir)
                    zipf.write(file_path, arcname)

    zip_index = 1

    for root, dirs, files in os.walk(folder_path):
        # Apenas considerar diretórios que tenham arquivos
        if not files:
            continue

        # Somente os arquivos que não são .mp4 serão incluídos no zip
        non_mp4_files = [f for f in files if not f.endswith('.mp4')]
        
        if not non_mp4_files:
            continue

        temp_folder = os.path.join(zip_folder, "temp_folder")
        os.makedirs(temp_folder, exist_ok=True)

        for file in non_mp4_files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder_path)
            dest_path = os.path.join(temp_folder, relative_path)
            
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(file_path, dest_path)

        while get_total_size_of_folder(temp_folder) > 1.9 * (1024 ** 3):
            zip_name = generate_zip_name(base_folder_name, zip_index)
            compress_directory(temp_folder, zip_name)
            zip_index += 1
            shutil.rmtree(temp_folder)
            os.makedirs(temp_folder, exist_ok=True)

    if os.listdir(temp_folder):
        zip_name = generate_zip_name(base_folder_name, zip_index)
        compress_directory(temp_folder, zip_name)

    shutil.rmtree(temp_folder)

    print("Files prepared for upload!")