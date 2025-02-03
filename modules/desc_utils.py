import os
import codecs

def edit_desc_file(file_path: str):
    # Abre o arquivo com decodificação utf-8
    with codecs.open(file_path, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()
    
    # Separa a linha com as hashtags do restante do texto
    texto_com_hashtags = ""
    resto_do_texto = ""
    encontrou_hashtags = False

    for linha in linhas:
        if linha.strip().startswith("#"):
            encontrou_hashtags = True
            texto_com_hashtags += linha
        else:
            resto_do_texto += linha

    # Limitar o restante do texto a 800 caracteres, contando espaços
    if len(resto_do_texto) > 800:
        resto_do_texto = resto_do_texto[:800] + " (...)"

    # Reabre o arquivo para escrita e escreve o texto editado
    with codecs.open(file_path, 'w', encoding='utf-8') as arquivo:
        arquivo.write(resto_do_texto)
        if encontrou_hashtags:
            arquivo.write("\n" + texto_com_hashtags)

