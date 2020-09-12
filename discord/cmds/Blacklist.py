# coding=utf-8
# Androxus bot
# Blacklist.py

__author__ = 'Rafael'

from discord.ext import commands
from discord.dao.BlacklistDao import BlacklistDao
class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(aliases=['blacklisted', 'banido'])
    @commands.is_owner()
    async def blacklist(self, ctx, *, pessoaId : int):
        if not BlacklistDao().get_pessoa(pessoaId):
            await ctx.send(f'A pessoa ta safe!')
        else:
            await ctx.send(f'Essa pessoa está banida de usar meus comandos!')
    @commands.command(aliases=['ab'])
    @commands.is_owner()
    async def add_blacklist(self, ctx, *, pessoaId: int):
        try:
            BlacklistDao().create(pessoaId)
            await ctx.send('Usuário banido!')
        except Exception as error:
            await ctx.send(f'Ocorreu o erro \n```{error}```\nna execução do comando ._.')
    @commands.command(aliases=['rb', 'whitelist'])
    @commands.is_owner()
    async def remove_blacklist(self, ctx, *, pessoaId: int):
        try:
            BlacklistDao().delete(pessoaId)
            await ctx.send('Usuário perdoado!')
        except Exception as error:
            await ctx.send(f'Ocorreu o erro \n```{error}```\nna execução do comando ._.')
def setup(bot):
    bot.add_cog(Blacklist(bot))
