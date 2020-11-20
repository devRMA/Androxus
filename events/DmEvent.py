# -*- coding: utf-8 -*-
# Androxus bot
# DmEvent.py

__author__ = 'Rafael'

from discord.ext import commands


class DmEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_private_channel_create(self, channel):
        if not self.bot.started:
            return
        await channel.send(f'Olá {channel.recipient.name}!\n'
                           'Você pode usar meus comandos aqui sem precisar do prefixo!\n'
                           'Para saber todos os meus comandos, digite `cmds`!\n'
                           'Para me adicionar num servidor, digite `invite`!\n'
                           f'{self.bot.emoji("love")}')


def setup(bot):
    """

    Args:
        bot (Classes.Androxus.Androxus): Instância do bot

    """
    bot.add_cog(DmEvent(bot))
