# coding=utf-8
# Androxus bot
# Androxus.py

__author__ = 'Rafael'

from datetime import datetime
from json import loads  # função que vai converter de json pra dicionario

import discord
from discord.ext import commands
from requests import get  # função que vai pegar o html da página

from utils.Utils import get_configs


def _warn(frase: str) -> None:
    """
    :param frase: a frase que vai ser printada, com a cor amarela
    :return: Não possui retorno
    :type frase: str
    :rtype: None
    """
    print('\033[1;33m', end='')
    print(frase)
    print('\033[0;0m')


class Androxus(commands.Bot):
    # versão do bot
    __version__ = '2.1.3'
    # dicionário com todas as configurações do arquivo configs.json
    configs = get_configs()
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_command('help')  # remove o comando help default
        # vai verificar se a pessoa está com a versão mais atual do bot
        url = 'https://api.github.com/repositories/294764564/commits'  # url onde ficam todos os commits do bot
        html = get(url).text  # vai pegar o texto da página
        json = loads(html)  # transformar de json para dicionario
        # como os commits, sempre são assim:
        # Versão x.x.x.x
        # - alterações
        # vai pegar a primeira linha do commit e apenas a versão do último commit
        version_github = json[0]['commit']['message'].splitlines()[0].split(' ')[-1]
        # e vai comparar com a versão atual
        if version_github != self.__version__:
            _warn('========== ATENÇÃO! ==========\n'
                  'Já você está usando uma versão desatualizada do Androxus!\n'
                  'Isso não vai impedir que o bot inicie, porém a sua versão pode\n'
                  'estar com algum bug que já foi resolvido ou algum comando a menos!\n'
                  'Acesse o repositório original, e baixe a nova versão!\n'
                  'Link do repositório original:\nhttps://github.com/devRMA/Androxus\n'
                  f'Nova versão: {version_github}\n'
                  f'Versão que você está usando: {self.__version__}')

    def configurar(self):
        self.uptime = datetime.utcnow()
        self.mudar_status = True
        self.msg_traduzidas = []
        self.dm_channel_log = self.get_channel(self.configs['dm_channel'])
        self.configurado = True
        self.maintenance_mode = False

    def get_all_categories(self):
        categories = [c[0] for c in self.configs['emojis']['categories'].items()]
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
        return sorted(commands.copy(), key=lambda x: x.name)

    def get_emoji_from_category(self, category):
        category = category.lower()
        if self.is_category(category):
            try:
                return self.configs['emojis']['categories'][category]
            except KeyError:
                return ''
        return ''

    def get_all_commands(self):
        commands = []
        for cog in self.cogs:
            for command in self.get_cog(cog).get_commands():
                if not command.hidden:
                    commands.append(command)
        return sorted(commands.copy(), key=lambda x: x.name)

    async def send_help(self, ctx):
        await self.get_command('help')(ctx)


class _BaseComando(commands.Command):
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)
        self.category = kwargs.get('category', 'outros')
        self.parameters = kwargs.get('parameters', [])
        self.examples = kwargs.get('examples', [])
        self.perm_user = kwargs.get('perm_user', None)
        self.perm_bot = kwargs.get('perm_bot', None)


def comando(*args, **kwargs):
    return commands.command(*args, **kwargs, cls=_BaseComando)
