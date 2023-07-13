# AdemirBot

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Descrição
O projeto "Ademir" é um bot criado para melhorar a experiência de comunidades focadas em bem-estar. Ele permite reproduzir músicas, criar macros, efetuar ações de moderação em massa e conversar com a API do ChatGPT.

## Funcionalidades
[ ] Falar com o bot apenas mencionando o mesmo
[ ] Reprodução/download de músicas/playlists em canal de audio
[ ] Suporte a links de vídeo do YouTube
[ ] Suporte a links de musicas do Spotify
[ ] Suporte a links de albuns do Spotify
[ ] Suporte a links de playlists públicas do Spotify
[ ] Suporte a links de playlists públicas do YouTube
[ ] Denunciar um usuário através do comando `/denunciar`
[ ] Denunciar uma mensagem com o menu de contexto

## Comandos de Booster
[ ] Falar com o bot em uma thread com o comando `/thread`
[ ] Gerar imagens com o comando `/dall-e`
[ ] Gerar texto com o comando `/completar`

## Comandos do Administrador
[ ] Configurar o Canal de Denúncias: Comando `/config-denuncias`
[ ] Criar macros através do comando `/macro`
[ ] Editar macros: comando `/editar-macro`
[ ] Excluir macro: comando `/excluir-macro`
[ ] Banir em massa: comando `/massban`
[ ] Expulsar em massa: comando `/masskick`
[ ] Importar histórico de mensagens: comando `/importar-historico-mensagens`
[ ] Extrair lista de usuarios por atividade no servidor `/usuarios-inativos`
[ ] Configurar cargo extra para falar com o bot: comando `/config-cargo-ademir`

## Comandos de Música
[ ] `>>play <link/track/playlist/album>`: Reproduz uma música, playlist ou álbum.
[ ] `>>skip`: Pula para a próxima música da fila.
[ ] `>>back`: Pula para a música anterior da fila.
[ ] `>>replay`: Reinicia a música atual.
[ ] `>>pause`: Pausa/Retoma a reprodução da música atual.
[ ] `>>stop`: Interrompe completamente a reprodução de música.
[ ] `>>loop`: Habilita/Desabilita o modo de repetição de faixa.
[ ] `>>loopqueue`: Habilita/Desabilita o modo de repetição de playlist.
[ ] `>>queue`: Lista as próximas 20 músicas da fila.
[ ] `>>join`: Puxa o bot para o seu canal de voz.
[ ] `>>quit`: Remove o bot da chamada de voz.
[ ] `>>volume <valor>`: Ajusta o volume da música.

## Instalação (DevEnv)

### Dependências externas
Para utilizar todos os recursos desenvolvidos nesse projeto é necessário:
1. Criar um aplicativo no [Developer Portal do Discord](https://discord.com/developers/docs/getting-started)
2. Criar um aplicativo no [Developer Console do Spotify](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
3. Criar uma conta (paga) no OpenAI e criar uma [API Key](https://platform.openai.com/account/api-keys)
4. Criar uma instância MongoDB para o Bot guardar os dados de configuração

### Passo a passo
Para utilizar o bot "Ademir" em seu servidor do Discord, siga as etapas abaixo:
1. Clone este repositório em sua máquina local.
2. Instale as dependências necessárias executando o comando `pip install -r requirements.txt`.
3. Defina as seguintes varáveis de ambiente:
   - `SpotifyApiClientId`: Client ID do Aplicativo Spotify.
   - `SpotifyApiClientSecret`: Client Secret do Aplicativo Spotify
   - `PremiumGuilds`: IDs dos Servers permitidos para utilizar o ChatGPT
   - `AdemirAuth`: Token de autenticação do bot do Discord
   - `MongoServer`: String de conexão do Mongo DB
   - `ChatGPTKey`: Token de autenticação da conta de API do ChatGPT
4. Execute o bot utilizando o comando `python main.py`.

## Instalação (Docker)
Rode o seguintes comandos para iniciar o Ademir no docker:

Para construir a imagem:
```sh
docker build -t ademir .
```

Para iniciar o container:
```sh
docker run -e SpotifyApiClientId=<Client ID do Aplicativo Spotify> \
           -e SpotifyApiClientSecret=<Client Secret do Aplicativo Spotify> \
           -e PremiumGuilds=<IDs dos Servers permitidos para utilizar o ChatGPT> \
           -e AdemirAuth=<Token de autenticação do bot do Discord> \
           -e MongoServer=<String de conexão do Mongo DB> \
           -e ChatGPTKey=<Token de autenticação da conta de API do ChatGPT> \
           ademir
```

## Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE.txt](LICENSE.txt) para obter mais informações.

## Contato
Se você tiver alguma dúvida ou sugestão sobre o projeto "Ademir", sinta-se à vontade para entrar em contato:
- [Discord](https://discord.gg/invite/Q6fQrf5jWX)
