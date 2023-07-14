import logging
import asyncio
import os
import config
from interactions import Client, Intents, listen

logging.basicConfig()
cls_log = logging.getLogger("Ademir")
cls_log.setLevel(logging.DEBUG)

client = Client(intents=Intents.ALL, sync_interactions=True, asyncio_debug=True, logger=cls_log)

@listen()
async def on_startup():
    print("Bot ready")
    
async def load_cogs():
    for filename in os.listdir('./extensions'):
        if filename.endswith('.py'):
            client.load_extension(f'extensions.{filename[:-3]}')
  
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(load_cogs())   
    client.start(config.TOKEN)