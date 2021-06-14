# -*- coding: utf-8 -*-
# Androxus bot
# DmEvent.py

__author__ = 'Rafael'

from colorama import Fore, Style
from discord.ext import commands


class DmEvent(commands.Cog):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.General.Androxus): Instância do bot

        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_private_channel_create(self, channel):
        if not self.bot.is_ready():
            return
        async for message in channel.history(limit=1):
            if message.author != self.bot.user:
                await channel.send(f'Olá {channel.recipient.name}!\n'
                                   'Você pode usar meus comandos aqui sem precisar do prefixo!\n'
                                   'Para saber todos os meus comandos, digite `cmds`!\n'
                                   'Para me adicionar num servidor, digite `invite`!\n'
                                   f'{self.bot.get_emoji("love")}')


def setup(bot):
    cog = DmEvent(bot)
    cmds = f'{Fore.BLUE}{len(cog.get_listeners())}{Fore.LIGHTMAGENTA_EX}'
    print(f'{Style.BRIGHT}{Fore.GREEN}[{"EVENT LOADED":^16}]' +
          f'{Fore.LIGHTMAGENTA_EX}{cog.qualified_name}({cmds}){Style.RESET_ALL}'.rjust(60))
    bot.add_cog(cog)
