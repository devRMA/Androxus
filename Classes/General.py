# -*- coding: utf-8 -*-
# Androxus bot
# General.py

__author__ = 'Rafael'

import re
from datetime import datetime
from itertools import cycle
from os import listdir
from string import ascii_letters
from sys import version
from traceback import format_exc
from typing import List, Optional, Union

import discord
from aiohttp.client import ClientSession
from asyncpg.pool import Pool
from colorama import Fore
from discord import AllowedMentions, Colour, Webhook
from discord.ext import commands, tasks
from discord.ext.commands.view import StringView
from discord.utils import utcnow
from stopwatch import Stopwatch

from Classes.Languages import Translations
from database.Factories.ConnectionFactory import ConnectionFactory
from database.Repositories.BlacklistRepository import BlacklistRepository
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils import permissions
from utils.Utils import get_configs, prettify_number, get_path_from_file, get_prefix, get_emojis_json, \
    get_most_similar_item, string_similarity, print_colorful


async def _check_version(bot):
    # vai verificar se a pessoa está com a versão mais atual do bot
    url = 'https://api.github.com/repositories/294764564/commits'  # url onde ficam todos os commits do bot
    async with bot.session.get(url) as resp:
        json = await resp.json()
    # como os commits, sempre são assim:
    # Versão x.x.x.x
    # - alterações
    # vai pegar a primeira linha do commit e apenas a versão do último commit
    version_github = json[0]['commit']['message'].splitlines()[0].split(' ')[-1]
    # e vai comparar com a versão atual
    if version_github != bot.__version__:
        print_colorful('========== ATENÇÃO! ==========\n'
                       'Já você está usando uma versão desatualizada do Androxus!\n'
                       'Isso não vai impedir que o bot inicie, porém a sua versão pode\n'
                       'estar com algum bug que já foi resolvido ou algum comando a menos!\n'
                       'Acesse o repositório original, e baixe a nova versão!\n'
                       'Link do repositório original:\nhttps://github.com/devRMA/Androxus\n', False, color=Fore.YELLOW)
        print_colorful('Nova versão: {version_github}', color=Fore.RED, values={'version_github': version_github})
        print_colorful('Versão que você está usando: {bot_version}', color=Fore.GREEN,
                       values={'bot_version': bot.__version__})


def _recursively_format_items(i, values):
    if isinstance(i, list):
        new_iterable = []
        for c in i:
            new_iterable.append(_recursively_format_items(c, values))
    elif isinstance(i, dict):
        new_iterable = {}
        for k, v in i.items():
            new_iterable[k] = _recursively_format_items(v, values)
    elif isinstance(i, str):
        return i.format_map(values)
    else:
        return i
    return new_iterable


def _load_cogs(bot):
    bot.remove_command('help')
    bot.load_extension('jishaku')
    path_cmds = get_path_from_file('cmds/')
    path_events = get_path_from_file('events/')
    cmds_files = list(map(lambda f: f[:-3], filter(lambda f: f.endswith('.py'), listdir(path_cmds))))
    events_files = list(map(lambda f: f[:-3], filter(lambda f: f.endswith('.py'), listdir(path_events))))
    for file in cmds_files:
        # noinspection PyBroadException
        try:
            bot.load_extension(f'cmds.{file}')  # vai adicionar ao bot
        except commands.NoEntryPointError:
            print(f'⚠ - Módulo {file} ignorado! "def setup" não encontrado!!')
        except Exception:
            print(f'⚠ - Módulo {file} deu erro na hora de carregar!\n{format_exc()}')
    for file in events_files:
        # noinspection PyBroadException
        try:
            bot.load_extension(f'events.{file}')
        except commands.NoEntryPointError:
            pass  # se não achar o def setup
        except Exception:
            print(f'⚠ - Módulo {file} não foi carregado!\n{format_exc()}')


class Configurations:
    __slots__ = ('owners', 'webhook_server', 'webhook_owner', 'db_connection_string', 'default_prefix',
                 'default_lang', 'token')
    owners: List[int]
    webhook_server: Optional[Webhook]
    webhook_owner: Optional[Webhook]
    db_connection_string: str
    default_prefix: str
    default_lang: str
    token: str
    _configs: dict = get_configs()

    def __init__(self):
        self.owners = self._configs.get('owners')
        self.webhook_server = None
        self.webhook_owner = None
        self.db_connection_string = self._configs.get('connection_string')
        self.default_prefix = self._configs.get('default_prefix')
        self.default_lang = self._configs.get('default_lang')
        self.token = self._configs.get('token')

    async def init_webhooks(self, session):
        webhooks = self._configs.get('webhooks')
        wh_server = webhooks.get('server_logs')
        self.webhook_server = Webhook.partial(wh_server.get('id'), wh_server.get('token'), session=session)
        wh_owner = webhooks.get('owner_logs')
        self.webhook_owner = Webhook.partial(wh_owner.get('id'), wh_owner.get('token'), session=session)


class Androxus(commands.Bot):
    __version__ = '2.3'
    configs: Configurations
    uptime: datetime = datetime.utcnow()
    mudar_status: bool = True
    maintenance_mode: bool = False
    db_connection: Pool = None
    session: ClientSession = None
    translations: Translations
    _status = cycle(['Para me adicionar em um servidor, basta enviar a mensagem "invite" no meu privado!',
                     'To add me to a server, just send the message "invite" in my dm!',
                     'Eu estou divertindo {servers} servidores!',
                     'I\'m amusing {servers} servers!',
                     'Estou divertindo {pessoas} pessoas!',
                     'I\'m having fun {pessoas} people!',
                     'Estou ouvindo {channels} chats!',
                     'I\'m listening to {channels} chats!',
                     'Caso você precise de ajuda, basta me mencionar!',
                     'If you need help, just mention me!',
                     '🤔 como que eu estou "jogando" se eu sou um bot?',
                     '🤔 How am I "playing" if I\'m a bot?',
                     'Caso você queira saber mais detalhes sobre mim, use o comando "botinfo"!',
                     'If you want to know more details about me, use the "botinfo" command!',
                     'Caso você queira ver meu código fonte, use o comando "source"!',
                     'If you want to see my source code, use the "source" command!',
                     'Para saber todos os meus comandos, digite "ajuda"!',
                     'To know all my commands, send "help"!',
                     'Para obter mais informações sobre um comando, use o comando "ajuda comando"!',
                     'For more information about a command, use the command "help command"!'
                     ])

    def __init__(self, *args, **kwargs):
        self._startup_timer = Stopwatch()
        self.translations = Translations()
        self.configs = Configurations()

        # Intents do discord.py 1.5.0
        intents = discord.Intents.all()

        async def _prefix_or_mention(bot, message):
            prefix = await get_prefix(bot, message)
            return commands.when_mentioned_or(prefix)(bot, message)

        kwargs['command_prefix'] = _prefix_or_mention
        kwargs['owner_id'] = self.configs.owners if len(self.configs.owners) > 1 else self.configs.owners[0]
        kwargs['case_insensitive'] = True
        kwargs['intents'] = intents
        kwargs['strip_after_prefix'] = True
        kwargs['activity'] = discord.Game(name='😴 Starting ...')
        super().__init__(*args, **kwargs)
        _load_cogs(self)

    async def on_ready(self):
        if self.db_connection is None:
            self._startup_timer.stop()
            self.session = self.http._HTTPClient__session
            await self.configs.init_webhooks(self.session)
            await _check_version(self)
            self.uptime = datetime.utcnow()
            self.db_connection = await ConnectionFactory.get_connection()
            print(('-=' * 10) + 'Androxus Online!' + ('-=' * 10))
            print_colorful('Logado em {user}', values={'user': str(self.user)})
            print_colorful('Id do bot: {id}', values={'id': self.user.id})
            all_commands = []
            for group in self.get_all_groups():
                all_commands += group.commands
            print_colorful('Com {all_commands} comandos!', values={'all_commands': len(all_commands)})
            print_colorful('Chegando a {all_members} usuários!', values={
                'all_members': len(set(self.get_all_members()))
            })
            print_colorful('Em {guilds} servidores!', values={'guilds': len(self.guilds)})
            print_colorful('Disponivel em {languages} línguas!', values={
                'languages': len(self.translations.supported_languages)
            })
            print_colorful('Versão do discord.py: {dversion}', values={'dversion': discord.__version__})
            print_colorful('Versão do python: {pversion}', values={'pversion': version[0:5]})
            print_colorful('Versão do bot: {bversion}', values={'bversion': self.__version__})
            print_colorful('Tempo para iniciar: {timer}', values={'timer': self._startup_timer})
            try:
                self._change_status.start()  # inicia o loop para mudar o status
            except RuntimeError:
                pass

    async def on_message(self, message):
        if (not self.is_ready()) or (self.db_connection is None):
            return
        ctx = await self.get_context(message)
        banned = (await BlacklistRepository().get_pessoa(self.db_connection, ctx.author.id))[0]
        if message.is_system() or not permissions.can_send(ctx) or ctx.author.bot or banned:
            return
        try:
            permissions.is_owner(ctx)
        except discord.ext.commands.errors.NotOwner:
            # se a pessoa não for dona do bot, e ele estiver em manutenção, simplesmente ignora a mensagem
            if self.maintenance_mode:
                return
        if not ctx.valid and ctx.prefix:
            message_without_prefix = message.content.removeprefix(ctx.prefix)
            view = StringView(message_without_prefix)
            group = self.get_command_group(view.get_word())
            if group:
                original_content = message.content
                message.content = f'{ctx.prefix}{group.name} {message_without_prefix}'
                new_ctx = await self.get_context(message)
                if new_ctx.valid:
                    ctx = new_ctx
                message.content = original_content
        server = await ServidorRepository().get_servidor(self.db_connection, ctx.guild.id) if ctx.guild else None
        prefixes = await self.get_prefix(message)
        prefix = prefixes[-1]
        if (f'<@{self.user.id}>' == message.content) or (f'<@!{self.user.id}>' == message.content):
            messages = await self.translate(ctx, help_='mention', values_={
                'prefix': prefix
            })
            if permissions.can_react(ctx):
                await message.add_reaction(self.get_emoji('hello'))
            return await ctx.send(**messages[0])
        if server and ctx.valid:
            for cmd_disabled in await ComandoDesativadoRepository().get_commands(self.db_connection, server):
                if self.get_command(cmd_disabled.comando.lower()).name == ctx.command.name:
                    erros = await self.translate(ctx, error_='cmd_disabled', values_={
                        'no_no': self.get_emoji('no_no')
                    })
                    return await ctx.send(**erros[0])
        if server and not ctx.valid:
            # vai ver se a pessoa usou algum comando personalizado
            for cmd_pers in await ComandoPersonalizadoRepository().get_commands(self.db_connection, server):
                if cmd_pers.comando.lower() in message.content.lower():
                    send_message = True
                    if not cmd_pers.in_text and (not message.content.lower() == cmd_pers.comando.lower()):
                        send_message = False
                    if send_message:
                        answer = cmd_pers.resposta
                        variables = {
                            '{author_name}': message.author.name,
                            '{author_nametag}': str(message.author),
                            '{author_nick}': message.author.display_name,
                            '{author_mention}': message.author.mention,
                            '{author_id}': message.author.id,
                            '{channel_mention}': message.channel.mention,
                            '{channel_name}': message.channel.name
                        }
                        for key, value in variables.items():
                            # estamos dando um replace em vez de .format
                            # pois, se der um .format e o usuário colocou um {abc} por exemplo
                            # iria dar erro, pois eu não estaria passando o valor de abc
                            answer = answer.replace(key, str(value))
                        return await ctx.send(answer)
        if not ctx.valid:
            if isinstance(ctx.channel, discord.DMChannel) or not server or not ctx.prefix:
                return
            filtered_message = message.content.removeprefix(ctx.prefix)
            if filtered_message[0] not in ascii_letters:
                return
            if server.sugestao_de_comando:
                all_names = []
                for cmd_name, cmd in self.all_commands.items():
                    # noinspection PyBroadException
                    try:
                        if await cmd.can_run(ctx):
                            all_names.append(cmd_name)
                    except Exception:
                        pass
                    if isinstance(cmd, commands.core.Group):
                        for cmd2_name, cmd2 in cmd.all_commands.items():
                            # noinspection PyBroadException
                            try:
                                if await cmd2.can_run(ctx):
                                    all_names.append(cmd2_name)
                            except Exception:
                                pass
                command_name = filtered_message.split(' ')[0]
                all_names = list(set(all_names))
                suggestion = get_most_similar_item(command_name, all_names)
                use_suggestion = False
                messages = await self.translate(ctx, error_='find_command', values_={
                    'sad': self.get_emoji('sad'),
                    'suggestion': suggestion,
                    'command_name': command_name,
                    'prefix': prefix
                })
                # se a sugestão for pelo menos 50% semelhante ao comando
                if suggestion is not None and string_similarity(command_name, suggestion) >= 0.5:
                    use_suggestion = True
                return await ctx.send(**messages[0 if use_suggestion else 1])
            else:
                return
        await self.invoke(ctx)

    def get_command(self, name):
        """

        Args:
            name (str): Nome do comando

        Returns:
            discord.ext.command.Command

        """
        command = super().get_command(name)
        if command is None:
            for group in self.get_all_groups():
                command = super().get_command(f'{group.name} {name}')
                if command is not None:
                    break
        return command

    def get_command_group(self, command_name):
        """

        Args:
            command_name (str): Nome do comando

        Returns:
            discord.ext.command.Group

        """
        command = self.get_command(command_name)
        if command:
            return command.parent
        return None

    @tasks.loop(minutes=1)
    async def _change_status(self):  # loop que vai ficar alterando o status do bot
        if self.mudar_status:
            status_escolhido = next(self._status)  # escolhe o próximo status
            status_escolhido = status_escolhido.format(servers=prettify_number(len(self.guilds)),
                                                       pessoas=prettify_number(len(self.users)),
                                                       channels=prettify_number(len(set(self.get_all_channels())))
                                                       )
            await self.change_presence(activity=discord.Game(name=status_escolhido))

    async def is_owner(self, user):
        if user.id in self.configs.owners:
            return True

        return await super().is_owner(user)

    def get_all_groups(self):
        """

        Returns:
            List[discord.ext.command.Group]

        """
        groups = filter(lambda c: isinstance(c, commands.core.Group) and c.name.lower() != 'jishaku',
                        self.commands)
        return sorted(groups, key=lambda c: c.name)

    def get_all_commands(self):
        """

        Returns:
            List[discord.ext.command.Command]

        """
        all_commands = []
        for group in self.get_all_groups():
            all_commands += group.commands
        return all_commands

    @staticmethod
    def get_emoji_from_group(group_name):
        """

        Args:
            group_name (str): O nome do grupo

        Returns:
            str

        """
        return get_emojis_json()['categories'].get(group_name.lower(), '')

    def get_emoji(self, args):
        """

        Args:
            args (str or int): Nome ou id ou nome do emoji que está no configs.json ou o uso do emoji

        Returns:
            discord.Emoji

        """
        args = str(args).lower()
        if args.isdigit():
            return super().get_emoji(int(args))
        dict_emojis = get_emojis_json()
        emoji = dict_emojis['categories'].get(args)
        if emoji is None:
            emoji = dict_emojis['dances'].get(args)
            if emoji is None:
                emoji = dict_emojis.get(args)
        if emoji is None:
            emoji = args
        emoji_regex = re.compile(r'<a?:.+?:([0-9]{15,21})>')
        regex_match = emoji_regex.match(emoji)
        if regex_match is not None:
            emoji_id = int(regex_match.group(1))
            return super().get_emoji(emoji_id)
        return None

    async def send_help(self, ctx):
        await self.get_command('help')(ctx)

    async def translate(self, ctx, *, error_=None, help_=None, others_=None, values_=None):
        """

        Args:
            ctx (discord.ext.commands.context.Context): O contexto que vai ser usado para pegar o prefixo
            error_ (str or None): Caso a mensagem seja de um erro, passe nesse parâmetro o erro (Default value = None)
            help_ (str or None): Caso a mensagem seja de um help, passe nesse parâmetro (Default value = None)
            others_ (str or None): Caso seja um outro tipo de mensagem (Default value = None)
            values_ (dict or None): Os valores dinamicos do json (Default value = {})

        Returns:
            dict or list: Uma lista de dicts com os parametros para usar no discord.abc.Messageable.send

        """
        if values_ is None:
            values_ = {}
        values_['ctx'] = ctx
        values_['bot'] = ctx.bot

        values_ = DictForFormat(values_)
        language = self.translations.get(await self.get_language(ctx))
        messages = []
        raw = language.get_translations(command=ctx.command.name if ctx.command is not None else None,
                                        erro=error_, help_=help_, others=others_)
        if raw is None:
            return None
        is_list = isinstance(raw, list)
        if not is_list:
            raw = [raw]
        for message_raw in raw:
            message = {}
            message_raw_formatted = _recursively_format_items(message_raw, values_)
            embed = None
            for key, value in message_raw_formatted.items():
                if key == 'embed':
                    embed = value
                elif key == 'reference':
                    message[key] = ctx.message
                elif key == 'allowed_mentions':
                    message[key] = AllowedMentions(**value)
                else:
                    message[key] = value
            if embed is not None:
                for key, value in embed.items():
                    if key == 'color':
                        if value == 'random':
                            embed[key] = Colour.random().value
                        else:
                            embed[key] = int(value)
                    elif key == 'timestamp' and value == 'now':
                        embed[key] = str(utcnow())
                message['embed'] = discord.Embed.from_dict(embed)
            messages.append(message)
        return messages if is_list else messages[0]

    async def get_language(self, ctx):
        """

        Args:
            ctx (discord.ext.commands.Context): Contexto da mensagem

        Returns:
            str: A lingua do servidor, que está registrado no banco de dados, se não tiver, vai retornar o padrão

        """
        if ctx.guild:
            lang = (await ServidorRepository().get_servidor(self.db_connection, ctx.guild.id)).lang
        else:
            lang = self.configs.default_lang
        return lang


class DictForFormat(dict):
    def __missing__(self, k):
        return k.join("{}")
