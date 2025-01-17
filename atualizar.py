import os
import requests
import zipfile
from io import BytesIO
import shutil
from pathlib import Path

zip_url = "https://github.com/viniped/vidsender/archive/refs/heads/master.zip"

zip_filename = "master.zip"

folders_to_preserve = ['bin', 'input', 'output', 'projects', 'zip_files', 'templates','sessions']
files_to_preserve = ['user.session', 'user.session-journal']

def download_zip_file(url, dest_path):
    response = requests.get(url)
    if response.status_code == 200:
        with dest_path.open('wb') as f:
            f.write(response.content)
        print(f"Arquivo {dest_path} baixado com sucesso.")
    else:
        print(f"Erro ao baixar o arquivo: {response.status_code}")
        response.raise_for_status()

def extract_zip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Arquivo {zip_path} extraído com sucesso.")

def main():
    script_dir = Path(__file__).parent.absolute()
    temp_dir = script_dir / "temp_extract"
    zip_path = script_dir / zip_filename
    user_input = input("Pressione Enter para atualizar os arquivos, ou qualquer outra tecla para cancelar: ")
    if user_input.strip():
        print("Atualização cancelada pelo usuário.")
        return

    download_zip_file(zip_url, zip_path)

    temp_dir.mkdir(parents=True, exist_ok=True)

    extract_zip_file(zip_path, temp_dir)

    print(f"Conteúdo do diretório temporário após extração: {list(temp_dir.iterdir())}")

    extracted_dir = temp_dir / "vidsender-main"

    if not extracted_dir.exists():
        print(f"Erro: Diretório {extracted_dir} não encontrado.")
        return

    for item in extracted_dir.iterdir():
        destination_path = script_dir / item.name

        if item.is_dir() and item.name in folders_to_preserve:
            continue  

        if item.is_file() and item.name in files_to_preserve:
            continue  

        if destination_path.exists():
            if destination_path.is_dir():
                shutil.rmtree(destination_path)
            else:
                destination_path.unlink()

        if item.is_dir():
            shutil.copytree(item, destination_path)
        else:
            shutil.copy2(item, destination_path)
    
    print(f"Arquivos atualizados com sucesso.")

    shutil.rmtree(temp_dir)
    zip_path.unlink()
    print(f"Limpeza concluída.")

if __name__ == "__main__":
    os.system('cls' if os.name =='nt' else 'clear')
    main()