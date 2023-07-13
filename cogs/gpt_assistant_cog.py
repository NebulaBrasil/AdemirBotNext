# cogs/gpt_assistant_cog.py
from discord.ext import commands

class GPTAssistantCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Olá, eu nao sei fazer nada ainda. Verifique no GitHub do projeto!')

def setup(bot):
    bot.add_cog(GPTAssistantCog(bot))