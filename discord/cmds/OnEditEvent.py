# coding=utf-8
# Androxus bot
# OnEditEvent.py

__author__ = 'Rafael'

from discord.ext import commands
from discord.dao.BlacklistDao import BlacklistDao


class OnEditEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if BlacklistDao().get_pessoa(after.author.id) or (not after.author.bot): return
        await self.bot.process_commands(
            after)  # se a pessoa editar a mensagem, verifica se ela editou para um comando valido


def setup(bot):
    bot.add_cog(OnEditEvent(bot))
