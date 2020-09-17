# coding=utf-8
# Androxus bot
# Blacklist.py

__author__ = 'Rafael'

from discord.ext import commands
from discord.dao.BlacklistDao import BlacklistDao
from discord.Utils import get_emoji_dance


class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['blacklisted', 'banido'], hidden=True)
    @commands.is_owner()
    async def blacklist(self, ctx, *, pessoaId : int):
        if not BlacklistDao().get_pessoa(pessoaId):
            await ctx.send(f'A pessoa pode usar meus comandos! {get_emoji_dance()}')
        else:
            await ctx.send(f'<a:no_no:755774680325029889> Essa pessoa está banida de usar meus comandos!')

    @commands.command(aliases=['ab'], hidden=True)
    @commands.is_owner()
    async def add_blacklist(self, ctx, *, pessoaId: int):
        BlacklistDao().create(pessoaId)
        await ctx.send('Usuário banido! <a:banned:756138595882107002>}')

    @commands.command(aliases=['rb', 'whitelist'], hidden=True)
    @commands.is_owner()
    async def remove_blacklist(self, ctx, *, pessoaId: int):
        BlacklistDao().delete(pessoaId)
        await ctx.send(f'Usuário perdoado! {get_emoji_dance()}')


def setup(bot):
    bot.add_cog(Blacklist(bot))
