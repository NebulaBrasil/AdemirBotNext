# config.py
import os
from dotenv import load_dotenv
load_dotenv()

# Configurações do MongoDB
MONGO_URI = os.getenv('MongoServer')
DATABASE_NAME = "ademir"
PREMIUM_GUILDS = os.getenv('PremiumGuilds')
OPENAPI_TOKEN = os.getenv('ChatGPTKey')
SPOTIFY_CLIENT_ID = os.getenv('SpotifyApiClientId')
SPOTIFY_CLIENT_SECRET = os.getenv('SpotifyApiClientSecret')

# Token do bot
TOKEN = os.getenv('AdemirAuth')

# Token do bot
TOKEN = os.getenv('AdemirAuth')

# Prefixo dos comandos (opcional)
PREFIX = ">>"

# Outras configurações do bot
NOME_BOT = "Ademir"
DESCRICAO_BOT = "Bot"