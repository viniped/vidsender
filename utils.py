import os
from colorama import Fore
import pyfiglet
import random
from pyrogram import Client
from unidecode import unidecode

session_name = 'user'

def authenticate():
    # Get credentialas from user
    def get_credentials():
        api_id = input("Digite seu API ID: ")
        api_hash = input("Digite seu API Hash: ")
        return api_id, api_hash

    # if session file does not exists, obtain the credentials 
    if not os.path.exists(f"{session_name}.session"):
        api_id, api_hash = get_credentials()
        with Client(session_name, api_id, api_hash) as app:
            print("Você está autenticado!")
    else:
        print("Usando sessão existente.")


class Banner:
    def __init__(self, banner):
        self.banner = banner
        self.lg = Fore.LIGHTGREEN_EX
        self.w = Fore.WHITE
        self.cy = Fore.CYAN
        self.ye = Fore.YELLOW
        self.r = Fore.RED
        self.n = Fore.RESET


    def print_banner(self):
        colors = [self.lg, self.r, self.w, self.cy, self.ye]
        f = pyfiglet.Figlet(font='slant')
        banner = f.renderText(self.banner)
        print(f'{random.choice(colors)}{banner}{self.n}')
        print(f'{self.r}  Version: v 1.0.0 https://github.com/viniped \n{self.n}')


def show_banner():
    banner = Banner('Vidsender')
    banner.print_banner()

   
def generate_report(folder_path):    
    if not os.path.exists(folder_path):
        return f"Erro: O caminho '{folder_path}' não existe."
    
    total_files = 0
    total_dirs = 0
    detailed_list = []
    
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            detailed_list.append(f"Diretório: {os.path.join(root, dir_name)}")
            total_dirs += 1
        for file_name in files:
            detailed_list.append(f"Arquivo: {os.path.join(root, file_name)}")
            total_files += 1
    
    report = f"Relatório de '{folder_path}':\n"
    report += f"Total de diretórios: {total_dirs}\n"
    report += f"Total de arquivos: {total_files}\n\n"
    report += "\n".join(detailed_list)
    
    report_file_path = os.path.join(folder_path, "relatorio_conteudo.txt")
    with open(report_file_path, 'w', encoding='utf-8') as file:
        file.write(report)

    return f"Relatório salvo em: {report_file_path}"    
    
def clear_directory(directory_path):
    if not os.path.exists(directory_path):
        print(f"A pasta {directory_path} não existe.")
        return

    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            elif os.path.isfile(item_path):
                os.remove(item_path)
        except Exception as e:
            print(f"Não foi possível deletar {item_path}. Erro: {e}")
