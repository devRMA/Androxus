# coding=utf-8
# Androxus bot
# ErrorCommands.py

__author__ = 'Rafael'

from discord.ext import commands
from discord_bot.dao.ServidorDao import ServidorDao


class ErrorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, ctx, guild):
        # toda vez que adicionarem o bot num servidor, vai adicionar o servidor ao banco
        ServidorDao().create(guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, ctx, guild):
        # toda vez que removerem o bot de um servidor, vai remover o servidor do banco
        ServidorDao().delete(guild.id)


def setup(bot):
    bot.add_cog(ErrorCommands(bot))
