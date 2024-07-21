# Vidsender

Este script foi projetado para fazer o upload das suas coleções audiovisuais (qualquer conteúdo que deseje como festa de noivado, vídeos de casamento etc ...) para o Telegram de forma organizada.

# Aviso LEGAL / DISCLAIMER

## Contribuições

Contribuições são muito bem-vindas! Se você deseja contribuir com este projeto, sinta-se à vontade para abrir pull requests ou issues.
Agradecemos antecipadamente pelo seu interesse e contribuição.

## Repositórios Derivados / Projetos que reproduzem este repositório de forma total ou parcial

Você está autorizado a criar repositórios derivados (forks), e reproduzir total ou parcial partes deste projeto.
No entanto, ao fazer isso, pedimos gentilmente que você forneça os devidos créditos ao repositório original. Isso pode ser feito das seguintes maneiras :

- Incluir um link para este repositório no seu README.

- Mencionar explicitamente o repositório original em qualquer documentação associada ao seu projeto derivado ou projeto que reproduz parte desse projeto.

## O que pode acontecer se eu não cumprir os termos da licença?

Caso o desenvolvedor desse repositório ['viniped/vidsender'](https://github.com/viniped/vidsender) encontre um repositório que não está cumprindo os termos da licença como reprodução total ou parcial desse repositorio ['viniped/vidsender'](https://github.com/viniped/vidsender)  
o desenvolvedor e detenteor de direitos autorais do repositório ['viniped/vidsender'](https://github.com/viniped/vidsender) irá em primeira mão procurar uma solução amigável entrando em contato direto e solicitando a atribução de créditos,
caso a via amigável seja ignorada ou não atendida o desenvolvedor, ciente dos termos de uso da plataforma doravante denominada [GitHub](https://github.com/) irá abrir uma reclamação formal 
através do formulário de suporte da plataforma ou através de um aviso de DMCA (Digital Millennium Copyright Act).

Ao utilizar, contribuir, reproduzir parte total ou parcial deste repositório, você concorda com os termos acima.

## Requisitos

# Python
Para usar esse repositório você precisa instalar o python em sua máquina, siga o passos abaixo:

1. Vá para o [Site do Python](https://www.python.org/)
2. Na tela inicial clique no botão download, e logo após no botão " Download for Windows " conforme na imagem abaixo :


<img src="https://imgur.com/a/Gz8c3wj" alt="home page python">

- FFmpeg

## Instalação

1. Clone este repositório:


   	git clone https://github.com/viniped/vidsender.git


Instale os pacotes Python necessários:


	pip install -r requirements.txt

Caso prefira execute com privilégios de administrador os arquivo ' install_requirements.bat '

Crie um aplicativo no Telegram e obtenha seu API ID e API hash. Você será solicitado a inserir esses detalhes ao executar o script pela primeira vez.

## Para criar um app no Telegram: 

 - https://www.youtube.com/watch?v=8naENmP3rg4

## Configuração

Coloque seus arquivos de vídeo na pasta input, seguindo a estrutura de pastas pasta principal > subpastas
Qualquer arquivo que não seja um video, será compactado em formato .zip, será armazenado na pasta "zip_files" e enviado após os vídeos


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

