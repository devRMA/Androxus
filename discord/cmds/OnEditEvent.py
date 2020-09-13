# coding=utf-8
# Androxus bot
# OnEditEvent.py

__author__ = 'Rafael'

from discord.ext import commands
from discord.dao.BlacklistDao import BlacklistDao
from discord.dao.ComandoDesativadoDao import ComandoDesativadoDao


class OnEditEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if BlacklistDao().get_pessoa(after.author.id) or after.author.bot: return
        if not (after.guild is None):  # Se foi usado num server, vai ver se o comando está desativado
            if after.content.lower() in ComandoDesativadoDao().get_comandos(after.guild.id): return
        if after.author.id == self.bot.user.id: return
        await self.bot.process_commands(
            after)  # se a pessoa editar a mensagem, verifica se ela editou para um comando valido


def setup(bot):
    bot.add_cog(OnEditEvent(bot))
