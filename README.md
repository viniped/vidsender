# Vidsender

Este script foi projetado para fazer o upload das suas coleções audiovisuais para o Telegram de forma organizada.

## Requisitos

- Python 3.10.6 [Python 3.10.6](https://www.python.org/downloads/release/python-3106/)
- FFmpeg

## Instalação

1. Clone este repositório:


   	git clone https://github.com/viniped/vidsender.git


Instale os pacotes Python necessários:


	pip install -r requirements.txt

Crie um aplicativo no Telegram e obtenha seu API ID e API hash. Você será solicitado a inserir esses detalhes ao executar o script pela primeira vez.

## Para criar um app no Telegram: 

 - https://www.youtube.com/watch?v=8naENmP3rg4

## Configuração

Coloque seus arquivos de vídeo na pasta input, seguindo a estrutura de pastas pasta principal > subpastas
Coloque qualquer arquivo .zip que deseja fazer o upload na pasta "zip_files".


## Uso

1. Coloque seus arquivos de vídeo na pasta input


2. Execute o script

3. O script irá organizar e fazer o upload dos vídeos da pasta especificada para um canal do Telegram. Ele também fará o upload de qualquer arquivo `.zip` encontrado na pasta "zip_files".

4. O script gera uma mensagem de resumo com links para os vídeos enviados e a fixa no canal.

5. Você pode usar as hashtags (#F01, #F02, etc.) para navegar entre os vídeos enviados.

## Notas

Certifique-se de ter as permissões necessárias e acesso ao canal onde deseja fazer o upload dos vídeos.
Aproveite a organização e o compartilhamento do seu conteúdo audiovisual no Telegram!

## Caso tenha alguma duvida entre nesse grupo

https://t.me/+uxnB4OwMYPhiNWMx

