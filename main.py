import logging
import os
import config
import interactions
from interactions import Client, Intents

logging.basicConfig()
cls_log = logging.getLogger(config.BOT_NAME)
cls_log.setLevel(logging.ERROR)

client = Client(intents=Intents.ALL, sync_interactions=True, logger=cls_log)

@interactions.listen()
async def on_startup():
    print(f"{config.BOT_NAME} iniciado.")
    
def load_extensions():
    for filename in os.listdir('./extensions'):
        if filename.endswith('.py'):
            client.load_extension(f'extensions.{filename[:-3]}')
  
if __name__ == '__main__':
    load_extensions() 
    client.start(config.TOKEN)