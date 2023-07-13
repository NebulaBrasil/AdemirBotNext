# cogs/gpt_assistant_cog.py
import discord
from discord.ext import commands

class GPTAssistant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.hybrid_command(name="hello", with_app_command=True)
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        await ctx.send('Olá, eu nao sei fazer nada ainda. Verifique no GitHub do projeto!')

async def setup(bot):
    await bot.add_cog(GPTAssistant(bot))
    print("Cog GPT Iniciado")