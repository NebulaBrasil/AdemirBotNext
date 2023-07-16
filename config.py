# config.py
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv('MongoServer')
DATABASE_NAME = "ademir"
PREMIUM_GUILDS = os.getenv('PremiumGuilds')
OPENAPI_TOKEN = os.getenv('ChatGPTKey')
SPOTIFY_CLIENT_ID = os.getenv('SpotifyApiClientId')
SPOTIFY_CLIENT_SECRET = os.getenv('SpotifyApiClientSecret')
TOKEN = os.getenv('AdemirAuth')

BOT_NAME = "Ademir"
DESCRICAO_BOT = "Bot"
PREFIX = ">>"
CHAT_GPT_MODEL = "gpt-3.5-turbo"