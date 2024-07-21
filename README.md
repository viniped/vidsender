# Vidsender

Este script foi projetado para fazer o upload das suas coleções audiovisuais (qualquer conteúdo que deseje como festa de noivado, vídeos de casamento etc ...) para o Telegram de forma organizada.

## Aviso LEGAL / DISCLAIMER

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

### Python

Para usar esse repositório você precisa instalar o python em sua máquina, siga o passos abaixo:

1. Vá para o [Site do Python](https://www.python.org/)
2. Na tela inicial clique no botão download, e logo após no botão " Download for Windows " conforme na imagem abaixo :

![site python](https://github.com/user-attachments/assets/1a729329-4311-4b3d-974e-68715a2d7215)

3. Após fazer o download do executável do python , abra-o com privilégios de administrador, você deve se deparar com uma janela como essa:

![add python to path](https://github.com/user-attachments/assets/69df84b3-6250-47cf-a544-04ee61e1debf)

Marque as caixas " Use admin privileges when instaling py.exe" e "Add python.exe to PATH" e por fim clique em "Install Now"

# Ferramentas de Build do Microsoft C++

As Ferramentas de Build do Microsoft C++ (Microsoft C++ Build Tools) são um conjunto de ferramentas e bibliotecas que incluem compiladores, vinculadores e outras ferramentas necessárias para compilar código C++ no Windows. Embora sejam projetadas principalmente para desenvolvimento em C++, elas também são frequentemente necessárias ao instalar e usar pacotes Python que contêm extensões em C ou C++.

#### Por que são necessárias para Python?

1. **Compilação de Extensões em C/C++:**
   - Muitos pacotes Python, especialmente aqueles voltados para desempenho ou integração com bibliotecas de baixo nível, incluem componentes escritos em C ou C++. Estes componentes precisam ser compilados quando o pacote é instalado. Exemplos incluem `numpy`, `scipy`, `pandas`, `lxml` e muitos outros.
   - As Ferramentas de Construção do Microsoft C++ fornecem o compilador e as ferramentas necessárias para essa compilação.

2. **Instalação de Pacotes a partir do Código-fonte:**
   - Quando você instala pacotes Python a partir do código-fonte (por exemplo, usando `pip install` em vez de baixar uma roda precompilada), o processo de instalação pode exigir a compilação do código. Isso é comum em ambientes onde rodas precompiladas não estão disponíveis para a versão do Python ou plataforma específica.

#### Como instalar as Ferramentas de Construção do Microsoft C++?

Você pode instalar as Ferramentas de Construção do Microsoft C++ seguindo estes passos:

1. **Baixe o instalador:**
   - Acesse o [site oficial do Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/) e baixe o instalador das Ferramentas de Construção do Microsoft C++. conforme a imagem abaixo:

   ![Design sem nome](https://github.com/user-attachments/assets/ff4b0a0e-df71-488b-bf26-0ce6a7582293)

2. **Execute o instalador:**
   - Durante a instalação, selecione a opção "Desenvolvimento de desktop com C++" para garantir que você está instalando os componentes necessários. (Veja a imagem abaixo)

   <img width="637" alt="vs2022-installer-workloads" src="https://github.com/user-attachments/assets/45fbe88b-223f-450a-a26b-e9cdfb5b685c">

3. **Adicione às variáveis de ambiente (se necessário):**
   - Em algumas situações, você pode precisar adicionar os caminhos das Ferramentas de Construção do Microsoft C++ às variáveis de ambiente do sistema para que possam ser encontradas durante a compilação.

### FFmpeg

Para usar o script será necessario também o ffmpeg vamos utilizar a versão [Windows builds from gyan.dev](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z) .
Após fazer o download você deve obter um arquivo como na imagem :

![Captura de tela de 2024-07-21 19-44-39](https://github.com/user-attachments/assets/eec8e583-0a88-4d3e-ad2a-733c3c0d203c)

faça a extração do arquivo , crie uma pasta `bin`no disco C, dentro da pasta `bin`crie uma pasta `ffmpeg` o resultado obtido deve ser :


![Captura de tela de 2024-07-21 19-51-49](https://github.com/user-attachments/assets/f8a6d30a-389e-401d-a4e2-4e55cd237fc0)

copie o caminho da barra de navegação : ``C:\bin\ffmpeg``

Pesquise no menu iniciar por " Editar as variáveis de ambiente do sistema ":

![Captura de tela de 2024-07-21 19-55-51](https://github.com/user-attachments/assets/a0824b59-e73a-497f-a779-c8a03d8334e7)

Após clique em 

1 - " Variáveis de Ambiente" ,
2 - Em " Variáveis de sistema " , clique em Path 
3 - Por fim clique em "Novo"

![1](https://github.com/user-attachments/assets/220fbb6b-ee84-49d6-8968-e3e677f870e0)

4 - Após clicar em Novo cole o caminho de onde estão os seus arquivos do ffmpeg :

![3](https://github.com/user-attachments/assets/76f47e32-6c89-4d42-9cc0-559780e3e349)

5 - Faça o caminho inverso clicando em todas as janelas abertas em "OK" , pronto o ffmpeg está configurado.

6 - Confira se o ffmpeg foi instalado corretamente usando o comando `ffmpeg -version` a saida deve ser :

![Captura de tela de 2024-07-21 20-22-52](https://github.com/user-attachments/assets/6c004dfe-bb84-4f34-9d9f-f7991df04643)


## Instalação do script

1. Clone este repositório:

	`git clone https://github.com/viniped/vidsender.git`


ou baixe o zip e extraia no lugar que melhor lhe conver:

![Design sem nome (1)](https://github.com/user-attachments/assets/b9c4934c-27f1-43a5-85ca-94b16d5ac2a2)


Instale os pacotes Python necessários, nessa atualização será instalado por meio de um ambiente virtual então execute com privilégios de administrador o arquivo 

`install_requirements.bat`

Após instalar e configurar , você deve sempre executar o script através desse arquivo:

`exec_vidsender.bat`

Crie um aplicativo no Telegram e obtenha seu API ID e API hash. Você será solicitado a inserir esses detalhes ao executar o script pela primeira vez.

## Para criar um app no Telegram: 

 - https://www.youtube.com/watch?v=8naENmP3rg4

## Configuração

Coloque seus arquivos de vídeo na pasta input, seguindo a estrutura de pastas pasta principal > subpastas.

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

https://t.me/+0djb3eRSPrQzZGUx

## Doações

Caso queira apoiar a iniciativa open-source:

[Live - Pix](https://livepix.gg/vinitemaceta)

[Buy Me a Coffee](https://buymeacoffee.com/vinitemaceta)
