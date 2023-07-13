# main.py
import os
import discord
from discord.ext import commands
import config

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Carregar os cogs
initial_extensions = [
    'cogs.gpt_assistant_cog'
]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

    bot.run(config.TOKEN)