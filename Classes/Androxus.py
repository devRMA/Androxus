# -*- coding: utf-8 -*-
# Androxus bot
# Androxus.py

__author__ = 'Rafael'

import re
from datetime import datetime
from itertools import cycle
from json import loads
from os import listdir
from string import ascii_letters
from sys import version
from traceback import format_exc

import discord
from asyncpg.pool import Pool
from discord.ext import commands, tasks
from requests import get

from EmbedModels.embedHelpCategory import embed_help_category
from database.Factories.ConnectionFactory import ConnectionFactory
from database.Repositories.BlacklistRepository import BlacklistRepository
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils import permissions
from utils.Utils import get_configs, prettify_number, get_path_from_file, pegar_o_prefixo, get_emojis_json
from utils.Utils import string_similarity, get_most_similar_item


def _warn(frase):
    """

    Args:
        frase (str): A frase que vai ser printada, com a cor amarela

    Returns:
        None

    """
    print('\033[1;33m')
    print(frase)
    print('\033[0;0m')


def _load_cogs(bot):
    bot.remove_command('help')
    bot.load_extension('jishaku')
    path_cmds = get_path_from_file('cmds/')
    path_events = get_path_from_file('events/')
    for filename in listdir(path_cmds):
        if filename.endswith('.py'):
            try:
                bot.load_extension(f'cmds.{filename[:-3]}')  # vai adicionar ao bot
            except commands.NoEntryPointError:
                print(f'⚠ - Módulo {filename[:-3]} ignorado! "def setup" não encontrado!!')
            except:
                print(f'⚠ - Módulo {filename[:-3]} deu erro na hora de carregar!\n{format_exc()}')
    for filename in listdir(path_events):  # vai listar todas os arquivos que tem na pasta "events"
        if filename.endswith('.py'):
            try:
                bot.load_extension(f'events.{filename[:-3]}')
            except commands.NoEntryPointError:
                pass  # se não achar o def setup
            except:
                print(f'⚠ - Módulo {filename[:-3]} não foi carregado!\n{format_exc()}')


class Androxus(commands.Bot):
    __version__ = '2.2.3'
    configs: dict = get_configs()
    uptime: datetime
    mudar_status: bool = True
    server_log: discord.TextChannel = None
    maintenance_mode: bool = False
    started: bool = False
    db_connection: Pool = None

    def __init__(self, *args, **kwargs):
        # Intents do discord.py 1.5.0
        intents = discord.Intents.all()
        # configurações do .json
        configs = get_configs()

        async def _prefix_or_mention(bot, message):
            prefix = await pegar_o_prefixo(bot, message)
            return commands.when_mentioned_or(prefix)(bot, message)

        kwargs['command_prefix'] = _prefix_or_mention
        kwargs['owner_id'] = configs['owners'] if len(configs['owners']) > 1 else configs['owners'][0]
        kwargs['case_insensitive'] = True
        kwargs['intents'] = intents
        # iniciando o bot
        super().__init__(*args, **kwargs)
        _load_cogs(self)
        # vai verificar se a pessoa está com a versão mais atual do bot
        url = 'https://api.github.com/repositories/294764564/commits'  # url onde ficam todos os commits do bot
        html = get(url).text
        json = loads(html)
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

    async def on_ready(self):
        if not self.started:
            self.uptime = datetime.utcnow()
            self.server_log = self.get_channel(self.configs['channels_log']['servers'])
            self.db_connection = await ConnectionFactory.get_connection()
            self.started = True
            print(('-=' * 10) + 'Androxus Online!' + ('-=' * 10))
            print(f'Logado em {self.user}')
            print(f'ID: {self.user.id}')
            print(f'{len(self.get_all_commands())} comandos!')
            print(f'{len(set(self.get_all_members()))} usuários!')
            print(f'{len(self.guilds)} servidores!')
            print(f'Versão do discord.py: {discord.__version__}')
            print(f'Versão do python: {version[0:5]}')
            print(f'Versão do bot: {self.__version__}')
            try:
                self._change_status.start()  # inicia o loop para mudar o status
            except RuntimeError:
                pass

    async def on_message(self, message):
        if (not self.started) or (self.db_connection is None):
            return
        ctx = await self.get_context(message)
        banido = (await BlacklistRepository().get_pessoa(self.db_connection, ctx.author.id))[0]
        if message.is_system() or not permissions.can_send(ctx) or ctx.author.bot or banido:
            return
        try:
            permissions.is_owner(ctx)
        except discord.ext.commands.errors.NotOwner:
            # se a pessoa não for dona do bot, e ele estiver em manutenção, simplesmente ignora a mensagem
            if self.maintenance_mode:
                return
        servidor = await ServidorRepository().get_servidor(self.db_connection, ctx.guild.id) if \
            ctx.guild is not None else None
        prefixo = await pegar_o_prefixo(self, message)
        # if isinstance(message.channel, discord.DMChannel):  # se a mensagem foi enviada no dm
        #     embed = discord.Embed(title=f'O(A) {ctx.author} mandou mensagem no meu dm',
        #                           colour=0xfdfd96,
        #                           description=message.content,
        #                           timestamp=datetime.utcnow())
        #     embed.set_footer(text=str(ctx.author.id),
        #                      icon_url='https://media-exp1.licdn.com/dms/image/C510BAQHhOjPujl' +
        #                               'cgfQ/company-logo_200_200/0?e=2159024400&v=beta&t=49' +
        #                               'Ex7j5UkZroF7-uzYIxMXPCiV7dvtvMNDz3syxcLG8')
        #     if len(message.attachments) != 0:
        #         for index, attachment in enumerate(message.attachments):
        #             embed.add_field(name=f'{index + 1} attachment',
        #                             value=attachment.url,
        #                             inline=False)
        #     embed.set_thumbnail(url=message.author.avatar_url)
        #     await self.dm_channel_log.send(embed=embed)
        if (f'<@{self.user.id}>' == message.content) or (f'<@!{self.user.id}>' == message.content):
            await ctx.reply(f'Use o comando ``{prefixo}cmds`` para obter todos os meus comandos!',
                            mention_author=False)
            if permissions.can_use_external_emojis(ctx):
                await ctx.send(self.emoji("hello"))
            return
        if (servidor is not None) and ctx.valid:
            for comando_desativado_obj in await ComandoDesativadoRepository().get_commands(self.db_connection,
                                                                                           servidor):
                comando_desativado = self.get_command(comando_desativado_obj.comando.lower())
                if comando_desativado.name == ctx.command.name:
                    return await ctx.reply(f'{self.emoji("no_no")} Este comando '
                                           'foi desativado por um administrador do servidor!', delete_after=10,
                                           mention_author=False)
        channel = message.channel
        if (servidor is not None) and (ctx.command is None):
            # vai ver se a pessoa usou algum comando personalizado
            for comando_personalizado in await ComandoPersonalizadoRepository().get_commands(self.db_connection,
                                                                                             servidor):
                if comando_personalizado.comando.lower() in message.content.lower():
                    enviar_mensagem = True
                    if not comando_personalizado.in_text and (not message.content.lower() ==
                                                                  comando_personalizado.comando.lower()):
                        enviar_mensagem = False
                    if enviar_mensagem:
                        resposta = comando_personalizado.resposta
                        variaveis = {
                            '{author_mention}': message.author.mention,
                            '{author_name}': message.author.name,
                            '{author_nametag}': str(message.author),
                            '{author_nick}': message.author.display_name,
                            '{author_id}': message.author.id,
                            '{channel_mention}': message.channel.mention,
                            '{channel_name}': message.channel.name
                        }
                        for key_value in variaveis.items():
                            # estamos dando um replace em vez de .format
                            # pois, se der um .format e o usuário colocou um {abc} por exemplo
                            # iria dar erro, pois eu não estaria passando o valor de abc
                            resposta = resposta.replace(key_value[0], str(key_value[-1]))
                        return await channel.send(resposta)
        if not ctx.valid:
            if isinstance(message.channel, discord.DMChannel):
                return
            if not message.content.startswith(prefixo):
                return
            # vai pegar toda a mensagem, depois do prefixo
            comando = message.content.lower()[len(prefixo):]
            if len(comando) == 0:
                return
            # se o primeiro caracter da mensagem, não for uma letra
            if comando[0] not in ascii_letters:
                return
            comando = comando.split(' ')[0]
            mostrar_erro = servidor.sugestao_de_comando
            commands = []
            for command in self.get_all_commands():
                if comando.lower() == command.category:
                    e = await embed_help_category(self, ctx, comando)
                    return await ctx.reply(embed=e, mention_author=False)
                commands.append(command.name)
                commands.append(command.category)
                for alias in command.aliases:
                    commands.append(alias)
            if mostrar_erro:
                msg = f'{self.emoji("sad")} eu não achei consegui ' \
                      f'achar o comando "{comando}".'
                sugestao = get_most_similar_item(comando, commands)
                if sugestao is not None:
                    # se a sugestão for pelo menos 40% semelhante ao comando
                    if string_similarity(comando, sugestao) >= 0.4:
                        msg += f'\nVocê quis dizer ``{sugestao}``?'
                msg += f'\nPara desativar esta mensagem, use o comando ``desativar_sugestão``'
                return await ctx.reply(msg, delete_after=10, mention_author=False)
        await self.process_commands(message)

    @tasks.loop(minutes=1)
    async def _change_status(self):  # loop que vai ficar alterando o status do bot
        if self.mudar_status:
            # lista com os status
            status = cycle(['Para me adicionar em um servidor, basta enviar a mensagem "invite" no meu privado!',
                            'Eu estou divertindo {servers} servidores!',
                            'Estou divertindo {pessoas} pessoas',
                            'Estou ouvindo {channels} chats!',
                            'Caso você precise de ajuda, basta me mencionar!',
                            '🤔 como que eu estou "jogando" se eu sou um bot?',
                            'Caso você queira saber mais detalhes sobre mim, use o comando "botinfo"!',
                            'Caso você queira ver meu código fonte, use o comando "source"!',
                            'Para saber todos os meus comandos, digite "cmds"!',
                            'Para obter mais informações sobre um comando, use o comando "help comando"!'
                            ])
            status_escolhido = next(status)  # escolhe o próximo status
            status_escolhido = status_escolhido.format(servers=prettify_number(len(self.guilds)),
                                                       pessoas=prettify_number(len(self.users)),
                                                       channels=prettify_number(len(set(self.get_all_channels())))
                                                       )
            await self.change_presence(activity=discord.Game(name=status_escolhido))

    async def is_owner(self, user: discord.User):
        if user.id in self.configs['owners']:
            return True

        return await super().is_owner(user)

    @staticmethod
    def get_all_categories():
        categories = [c[0] for c in get_emojis_json()['categories'].items()]
        # é retornado uma copia da lista só por segurança
        return sorted(list(set(categories)).copy())

    def is_category(self, argument):
        for category in self.get_all_categories():
            if argument.lower() == category.lower():
                return True
        return False

    def get_commands_from_category(self, category):
        commands_from_category = []
        if self.is_category(category):
            for cog in self.cogs:
                for command in self.get_cog(cog).get_commands():
                    if hasattr(command, 'category') and (command.category == category) and (not command.hidden):
                        commands_from_category.append(command)
        return sorted(commands_from_category.copy(), key=lambda c: c.name)

    def get_emoji_from_category(self, category):
        category = category.lower()
        if self.is_category(category):
            try:
                return get_emojis_json()['categories'][category]
            except KeyError:
                return ''
        return ''

    @staticmethod
    def emoji(emoji_name):
        dict_emojis = get_emojis_json()
        try:
            return dict_emojis[emoji_name]
        except KeyError:
            try:
                return dict_emojis['dances'][emoji_name]
            except KeyError:
                try:
                    return dict_emojis['categories'][emoji_name]
                except KeyError:
                    return None

    def get_emoji(self, args):
        # alteração para aceitar o id,
        # o nome do emoji que está no configs.json
        # e o uso do emoji <:nome:1234>
        args = str(args).lower()
        if args.isdigit():
            return super().get_emoji(int(args))
        emoji = self.emoji(args)
        if emoji is None:
            emoji = args
        emoji_regex = re.compile(r'<a?:.+?:([0-9]{15,21})>')
        regex_match = emoji_regex.match(emoji)
        if regex_match is not None:
            emoji_id = int(regex_match.group(1))
            return super().get_emoji(emoji_id)
        return None

    def get_all_commands(self):
        all_commands = []
        for cog in self.cogs:
            for command in self.get_cog(cog).get_commands():
                if (not command.hidden) and (hasattr(command, 'category')):
                    all_commands.append(command)
        return sorted(all_commands.copy(), key=lambda c: c.name)

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
    """
    
    Example:
        @Androxus.comando(name='comando',
                          aliases=['alias1', 'alias2'],
                          description='Descrição do comando',
                          parameters=['<parâmetro obrigatorio>', '[parâmetro opcional]'],
                          examples=['`{prefix}comando` `exemplo de uso do comando tal`',
                                    '`{prefix}alias1` `outro exemplo`'],
                          # f'Você precisa ter permissão de `{perm_user}` para usar este comando!'
                          perm_user='permissão que o usuário precisa ter',
                          # f'Eu preciso ter permissão de `{perm_bot}` para realizar este comando!'
                          perm_bot='permissão que o bot precisa ter para executar o comando',
                          category='Categoria do comando',
                          hidden=False)
        async def _comando(self, ctx, parametro_obrigatorio, parametro_opcional='valor default')
            pass

    """
    return commands.command(*args, **kwargs, cls=_BaseComando)
