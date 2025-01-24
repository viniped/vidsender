import os
from colorama import Fore
import pyfiglet
import random
from pyrogram import Client
from unidecode import unidecode
import json
import shutil
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent

def load_letra_sumario():
    JSON_PATH = SCRIPT_PATH.parent / 'templates' / 'letra_sumario.json'
    with open(JSON_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data.get("Letra") 

def clean_console():
    os.system("cls" if os.name == "nt" else "clear")

def create_directories():
    directories = ["input", "output", "zip_files", "sessions", "projects", "cursos"]
    for dir_name in directories:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

# TODO Função de autenticação checar no futuro para bugs e refatoração
def authenticate():
    # Define a pasta onde as sessões serão armazenadas
    sessions_folder = "sessions"
    os.makedirs(sessions_folder, exist_ok=True)  # Cria a pasta se não existir

    # Nomes dos arquivos de sessão
    session_name_user = os.path.join(sessions_folder, "user")
    session_name_bot = os.path.join(sessions_folder, "bot")

    # Verifica se o arquivo de sessão do usuário existe
    if not os.path.exists(f"{session_name_user}.session"):
        # Obter as credenciais
        api_id = input("Enter your API ID: ")
        api_hash = input("Enter your API Hash: ")
        # Autentica o usuário
        with Client(session_name_user, api_id=int(api_id), api_hash=api_hash) as app:
            print("Conta user autenticada!")
    else:
        print("[USER] Usando sessão existente.")

    # Checa se o arquivo de sessão do bot existe
    if not os.path.exists(f"{session_name_bot}.session"):
        bot_token = input("Enter your Bot Token: ")
        # Autentica o bot usando o mesmo API ID e API Hash
        with Client(session_name_bot, api_id=int(api_id), api_hash=api_hash, bot_token=bot_token) as app:
            print("Conta bot autenticada!")
    else:
        print("[BOT] Usando sessão existente.")


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
    """
    Gera um relatório detalhado do conteúdo de um diretório usando os.scandir, em ordem sequencial.
    """
    if not os.path.exists(folder_path):
        return f"Erro: O caminho '{folder_path}' não existe."

    total_files = 0
    total_dirs = 0
    detailed_list = []

    def scan_directory(path):
        """
        Escaneia o diretório atual, adiciona arquivos e diretórios à lista detalhada.
        """
        nonlocal total_files, total_dirs
        try:
            with os.scandir(path) as entries:
                entries = sorted(entries, key=lambda e: e.name)  # Ordena por nome
                for entry in entries:
                    if entry.is_dir():
                        detailed_list.append(f"Diretório: {entry.path}")
                        total_dirs += 1
                        scan_directory(entry.path)  # Recursão para subdiretórios
                    elif entry.is_file():
                        detailed_list.append(f"Arquivo: {entry.path}")
                        total_files += 1
        except PermissionError:
            detailed_list.append(f"Sem permissão para acessar: {path}")

    # Inicia a varredura no diretório especificado
    scan_directory(folder_path)

    # Cria o relatório
    report = f"Relatório de '{folder_path}':\n"
    report += f"Total de diretórios: {total_dirs}\n"
    report += f"Total de arquivos: {total_files}\n\n"
    report += "\n".join(detailed_list)

    # Salva o relatório no arquivo "relatorio_conteudo.txt"
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

def json_load(path):
	with open(path, 'r', encoding='utf8') as j:
		content = json.load(j)
	return content