# main.py
import asyncio
import os
import interactions
import config

client = interactions.Client()

@interactions.listen()
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