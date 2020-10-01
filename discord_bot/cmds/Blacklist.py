# coding=utf-8
# Androxus bot
# Blacklist.py

__author__ = 'Rafael'

from discord.ext import commands

from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.BlacklistRepository import BlacklistRepository
from discord_bot.utils import permissions
from discord_bot.utils.Utils import get_emoji_dance


class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['blacklisted', 'banido'], hidden=True)
    @commands.check(permissions.is_owner)
    async def blacklist(self, ctx, *, pessoaId: int):
        conexao = Conexao()
        if not BlacklistRepository().get_pessoa(conexao, pessoaId):
            await ctx.send(f'A pessoa pode usar meus comandos! {get_emoji_dance()}')
        else:
            await ctx.send(f'<a:no_no:755774680325029889> Essa pessoa não usar meus comandos!')
        conexao.fechar()

    @commands.command(aliases=['ab'], hidden=True)
    @commands.check(permissions.is_owner)
    async def add_blacklist(self, ctx, *, pessoaId: int):
        conexao = Conexao()
        BlacklistRepository().create(conexao, pessoaId)
        await ctx.send('Este usuário não vai poder usar meus comandos! <a:banned:756138595882107002>}')
        conexao.fechar()

    @commands.command(aliases=['rb', 'whitelist'], hidden=True)
    @commands.check(permissions.is_owner)
    async def remove_blacklist(self, ctx, *, pessoaId: int):
        conexao = Conexao()
        BlacklistRepository().delete(conexao, pessoaId)
        await ctx.send(f'Usuário perdoado! {get_emoji_dance()}')
        conexao.fechar()


def setup(bot):
    bot.add_cog(Blacklist(bot))
