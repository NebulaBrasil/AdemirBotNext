# main.py
import os
import discord
from discord.ext import commands
import config

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    await load_cogs()

if __name__ == '__main__':
    bot.run(config.TOKEN)