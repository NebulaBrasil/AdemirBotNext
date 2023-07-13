# cogs/gpt_assistant_cog.py
from discord.ext import commands

class GPTAssistantCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Olá, eu sou um exemplo de comando em um cog!')

def setup(bot):
    bot.add_cog(GPTAssistantCog(bot))