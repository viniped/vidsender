# Vidsender

Este script foi projetado para fazer o upload das suas coleções audiovisuais para o Telegram de forma organizada.

## Requisitos

- Python 3.x
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

Coloque seus arquivos de vídeo na pasta que deseja fazer o upload, seguindo a estrutura de pastas desejada.
Coloque qualquer arquivo .zip que deseja fazer o upload na pasta "zip_files".

## Thumbnail personalizada

Coloque uma foto em 1280 x 720 com o nome thumb.jpg na pasta templates

## Uso

1. Coloque seus arquivos de vídeo na pasta que deseja fazer o upload
  Atenção: o script não aceita acentuação no nome da pasta principal

2. Execute o script e forneça o nome da pasta que deseja fazer o upload quando solicitado.

3. O script irá organizar e fazer o upload dos vídeos da pasta especificada para um canal do Telegram. Ele também fará o upload de qualquer arquivo `.zip` encontrado na pasta "zip_files".

4. O script gera uma mensagem de resumo com links para os vídeos enviados e a fixa no canal.

5. Você pode usar as hashtags (#F01, #F02, etc.) para navegar entre os vídeos enviados.

## Notas

Certifique-se de ter as permissões necessárias e acesso ao canal onde deseja fazer o upload dos vídeos.
Aproveite a organização e o compartilhamento do seu conteúdo audiovisual no Telegram!

## Caso tenha alguma duvida entre nesse grupo

https://t.me/+uxnB4OwMYPhiNWMx

## Caso o script tenha sua execução interrompida por motivos externos

Informe novamente o caminho da pasta e ele deve retomar da onde parou


