# coding=utf-8
# Androxus bot
# Androxus.py

__author__ = 'Rafael'

from datetime import datetime
from operator import attrgetter

import discord
from discord.ext import commands

from utils.Utils import get_configs


class Androxus(commands.Bot):
    # atributo que vai guardar quando o bot iniciou
    uptime: datetime or None = None
    # atributo que vai ficar responsável por controlar a mudança de status
    mudar_status: bool = False
    # atributo que vai evitar que a pessoa fique pedindo para traduzir a mesma mensagem
    msg_traduzidas: list = []
    # esse atributo vai ser responsável por guardar o chat
    # que o bot vai usar quando mandarem mensagem no privado dele
    dm_channel_log: discord.TextChannel = None
    configurado: bool = False
    maintenance_mode: bool
    emoji_category: dict = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_command('help')  # remove o comando help default

    def configurar(self):
        self.uptime = datetime.utcnow()
        self.mudar_status = True
        self.msg_traduzidas = []
        self.dm_channel_log = self.get_channel(get_configs()['dm_channel'])
        self.configurado = True
        self.maintenance_mode = False
        self.emoji_category = {
            'administração': '<:staffs:763807585174290452>',
            'bot_info': '<:bot:763808270426177538>',
            'diversão': '<a:loop_fun:763809373046702110>',
            'info': '<:Info:756712227221930102>',
            'matemática': '<:pi_emoji:763806073227575346>',
            'owner': '<:dev_tag:763812174514487346>',
            'úteis': '<a:disco:763811701589803098>',
            'outros': '<:outro:763812448054018098> ',
            'personalizado': '<:gordin:763875622199623690>'
        }

    def get_all_categories(self):
        categories = [c[0] for c in self.emoji_category.items()]
        # é retornado uma copia da lista só por segurança
        return sorted(list(set(categories)).copy())

    def is_category(self, argument):
        for category in self.get_all_categories():
            if argument.lower() == category.lower():
                return True
        return False

    def get_commands_from_category(self, category):
        commands = []
        if self.is_category(category):
            for cog in self.cogs:
                for command in self.get_cog(cog).get_commands():
                    if (command.category == category) and (not command.hidden):
                        commands.append(command)
        return sorted(commands.copy(), key=attrgetter('name'))

    def get_emoji_from_category(self, category):
        category = category.lower()
        if self.is_category(category):
            try:
                return self.emoji_category[category]
            except KeyError:
                return ''
        return ''

    def get_all_commands(self):
        commands = []
        for cog in self.cogs:
            for command in self.get_cog(cog).get_commands():
                if not command.hidden:
                    commands.append(command)
        return sorted(commands.copy(), key=attrgetter('name'))

    async def send_help(self, ctx):
        await self.get_command('help')(ctx)


class Command(commands.Command):
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)
        self.category = kwargs.get('category', 'outros')
        self.parameters = kwargs.get('parameters', [])
        self.examples = kwargs.get('examples', [])
        self.perm_user = kwargs.get('perm_user', None)
        self.perm_bot = kwargs.get('perm_bot', None)
