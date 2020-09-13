# coding=utf-8
# Androxus bot
# Blacklist.py

__author__ = 'Rafael'

from discord.ext import commands
from discord.dao.BlacklistDao import BlacklistDao


class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['blacklisted', 'banido'], hidden=True)
    @commands.is_owner()
    async def blacklist(self, ctx, *, pessoaId : int):
        if not BlacklistDao().get_pessoa(pessoaId):
            await ctx.send(f'A pessoa pode usar meus comandos!')
        else:
            await ctx.send(f'Essa pessoa está banida de usar meus comandos!')

    @commands.command(aliases=['ab'], hidden=True)
    @commands.is_owner()
    async def add_blacklist(self, ctx, *, pessoaId: int):
        BlacklistDao().create(pessoaId)
        await ctx.send('Usuário banido!')

    @commands.command(aliases=['rb', 'whitelist'], hidden=True)
    @commands.is_owner()
    async def remove_blacklist(self, ctx, *, pessoaId: int):
        BlacklistDao().delete(pessoaId)
        await ctx.send('Usuário perdoado!')


def setup(bot):
    bot.add_cog(Blacklist(bot))
