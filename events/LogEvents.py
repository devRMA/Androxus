# -*- coding: utf-8 -*-
# Androxus bot
# OnUpdateEvent.py

__author__ = 'Rafael'

from datetime import datetime
from io import BytesIO

import discord
from PIL import Image
from colorama import Fore, Style
from discord.ext import commands

from database.Repositories.ServidorRepository import ServidorRepository
from utils.Utils import difference_between_lists, get_path_from_file, cut_string


class LogEvent(commands.Cog):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.General.Androxus): Instância do bot

        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.bot or self.bot.maintenance_mode \
                or (not self.bot.is_ready()) or (self.bot.db_connection is None):
            return
        server = await ServidorRepository().get_servidor(self.bot.db_connection, after.guild.id)
        if server is None:
            return
        if server.channel_id_log is not None:
            channel = self.bot.get_channel(server.channel_id_log)
            if channel is not None:
                if before.nick != after.nick and server.nick_alterado:
                    embed = discord.Embed(title='Nick alterado',
                                          colour=discord.Colour.random(),
                                          description=f'O(A) {after.name} mudou de nick!\n'
                                                      f'User: {after.mention}\n'
                                                      f'Id: {after.id}\n'
                                                      f'Nick antigo: {before.nick}\n'
                                                      f'Nick novo: {after.nick}',
                                          timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=str(after.avatar.url))
                    await channel.send(embed=embed)
                if before.roles != after.roles and server.role_alterado:
                    cargos = [f'<@&{c.id}>' for c in difference_between_lists(before.roles, after.roles)]
                    # se a pessoa ficou com mais cargos, do que ela tinha antes
                    if len(before.roles) < len(after.roles):
                        desc = None
                        if len(cargos) == 1:
                            desc = f'Novo cargo: {cargos[0]}'
                        elif len(cargos) > 1:
                            desc = 'Novos cargo: ' + ', '.join(cargos)
                    else:  # se foi o contrário
                        desc = None
                        if len(cargos) == 1:
                            desc = f'Cargo removido: {cargos[0]}'
                        elif len(cargos) > 1:
                            desc = 'Cargos removidos: ' + ', '.join(cargos)
                    embed = discord.Embed(title='Cargos alterados',
                                          colour=discord.Colour.random(),
                                          description=f'O(A) {after.name} sofreu alteração nos cargos!\n'
                                                      f'User: {after.mention}\n'
                                                      f'Id: {after.id}\n'
                                                      f'{desc}',
                                          timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=str(after.avatar.url))
                    await channel.send(embed=embed)
                if (before.premium_since is None) and (after.premium_since is not None) and server.role_alterado:
                    # pessoa começou a dar boost
                    embed = discord.Embed(title='Novo booster',
                                          colour=discord.Colour(0xffdcf4),
                                          description=f'O(A) {after.name} começou a dar boost!\n'
                                                      f'User: {after.mention}\n'
                                                      f'Id: {after.id}\n',
                                          timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=str(after.avatar.url))
                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if after.bot or self.bot.maintenance_mode \
                or (not self.bot.is_ready()) or (self.bot.db_connection is None):
            return
        servers_with_user = []
        for guild in after.mutual_guilds:
            servers_with_user.append(await ServidorRepository().get_servidor(self.bot.db_connection, guild.id))
        if len(servers_with_user) == 0:
            return
        if before.name != after.name:
            embed = discord.Embed(title='Nome alterado',
                                  colour=discord.Colour.random(),
                                  description=f'O(A) {after.name} mudou de nome!\n'
                                              f'User: {after.mention}\n'
                                              f'Id: {after.id}\n'
                                              f'Nome antigo: {before.name}\n'
                                              f'Nome novo: {after.name}',
                                  timestamp=datetime.utcnow())
            embed.set_thumbnail(url=after.avatar.url)
            for server in servers_with_user:
                if server.channel_id_log is not None:
                    channel = self.bot.get_channel(server.channel_id_log)
                    if (channel is not None) and server.nome_alterado:
                        await channel.send(embed=embed)
        if before.discriminator != after.discriminator:
            embed = discord.Embed(title='Tag alterada',
                                  colour=discord.Colour.random(),
                                  description=f'O(A) {after.name} mudou a tag!\n'
                                              f'User: {after.mention}\n'
                                              f'Id: {after.id}\n'
                                              f'Tag antiga: {before.discriminator}\n'
                                              f'Tag nova: {after.discriminator}',
                                  timestamp=datetime.utcnow())
            embed.set_thumbnail(url=after.avatar.url)
            for server in servers_with_user:
                if server.channel_id_log is not None:
                    channel = self.bot.get_channel(server.channel_id_log)
                    if (channel is not None) and server.tag_alterado:
                        await channel.send(embed=embed)
        if before.avatar.url != after.avatar.url:
            avatar_erros = discord.NotFound, discord.HTTPException, discord.DiscordException
            path_401_image = get_path_from_file('401.png', 'images/')
            try:
                before_avatar = BytesIO(await before.avatar.replace(format='png', size=512).read())
            except avatar_erros:
                before_avatar = path_401_image
            try:
                after_avatar = BytesIO(await after.avatar.replace(format='png', size=512).read())
            except avatar_erros:
                after_avatar = path_401_image
            if before_avatar == after_avatar:
                return
            avatar_antigo = Image.open(before_avatar).resize((512, 512), Image.ANTIALIAS)
            avatar_novo = Image.open(after_avatar).resize((512, 512), Image.ANTIALIAS)
            base = Image.new('RGBA', (1024, 512), (0, 0, 0, 0))
            base.paste(avatar_antigo, (0, 0))
            base.paste(avatar_novo, (512, 0))
            embed = discord.Embed(title='Avatar alterado',
                                  colour=discord.Colour.random(),
                                  description=f'O(A) {after.name} mudou o avatar!\n'
                                              f'User: {after.mention}\n'
                                              f'Id: {after.id}\n'
                                              f'[Avatar antigo]({before.avatar.url})'
                                              f' → [avatar novo]({after.avatar.url})',
                                  timestamp=datetime.utcnow())
            embed.set_image(url='attachment://avatar.png')
            for server in servers_with_user:
                if server.channel_id_log is not None:
                    channel = self.bot.get_channel(server.channel_id_log)
                    if (channel is not None) and server.avatar_alterado:
                        arr = BytesIO()
                        base.save(arr, format='PNG')
                        arr.seek(0)
                        file = discord.File(arr, filename='avatar.png')
                        await channel.send(file=file, embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot or after.is_system() or self.bot.maintenance_mode \
                or ((after.guild is None) or (before.guild is None)) \
                or (not self.bot.is_ready()) or (before.content == after.content) \
                or (self.bot.db_connection is None):
            return
        server = await ServidorRepository().get_servidor(self.bot.db_connection, after.guild.id)
        if server.channel_id_log is not None:
            channel = self.bot.get_channel(server.channel_id_log)
            if channel is not None:
                if server.mensagem_editada:
                    before.content = cut_string(before.content, width=800)
                    if before.content.count('`') >= 3:
                        msg_antiga = f'\n{before.content}\n'
                    else:
                        msg_antiga = f'```{before.content}```'
                    after.content = cut_string(after.content, width=800)
                    if after.content.count('`') >= 3:
                        msg_nova = f'\n{after.content}\n'
                    else:
                        msg_nova = f'```{after.content}```'
                    embed = discord.Embed(title='Mensagem editada',
                                          colour=discord.Colour.random(),
                                          description=f'Autor: {after.author.name}\n'
                                                      f'Menção: {after.author.mention}\n'
                                                      f'Id: {after.author.id}\n'
                                                      f'Chat: {after.channel.mention}\n'
                                                      f'Mensagem antiga:{msg_antiga}'
                                                      f'[Mensagem nova]({after.jump_url}):'
                                                      f'{msg_nova}',
                                          timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=after.author.avatar.url)
                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or message.is_system() or self.bot.maintenance_mode \
                or (message.guild is None) or (not self.bot.is_ready()) or (len(message.content) == 0) \
                or (self.bot.db_connection is None):
            return
        server = await ServidorRepository().get_servidor(self.bot.db_connection, message.guild.id)
        if server.channel_id_log is not None:
            channel = self.bot.get_channel(server.channel_id_log)
            if channel is not None:
                if server.mensagem_deletada:
                    message.content = cut_string(message.content, width=800)
                    if message.content.count('`') >= 3:
                        msg_escaped = f'\n{message.content}\n'
                    else:
                        msg_escaped = f'```{message.content}```'
                    embed = discord.Embed(
                        title=f'Mensagem deletada',
                        colour=discord.Colour.random(),
                        description=f'Autor: {message.author.name}\n'
                                    f'Menção: {message.author.mention}\n'
                                    f'Id: {message.author.id}\n'
                                    f'Chat: {message.channel.mention}\n'
                                    f'Mensagem deletada:{msg_escaped}',
                        timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=message.author.avatar.url)
                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        if (self.bot.db_connection is None) or self.bot.maintenance_mode or (messages[0].guild is None) or \
                (not self.bot.is_ready()):
            return
        server = await ServidorRepository().get_servidor(self.bot.db_connection, messages[0].guild.id)
        if server.channel_id_log is not None:
            channel = self.bot.get_channel(server.channel_id_log)
            if (channel is not None) and server.mensagem_deletada:
                messages = list(filter(lambda m: not m.is_system() and len(m.content) != 0, messages))
                if len(messages) == 0:
                    return
                msg = '[day.month.year hour:minute:second] user#tag (id): message\n\n'
                for message in messages:
                    msg += f'[{message.created_at.strftime("%d.%m.%Y %H:%M:%S")}] '
                    msg += f'{message.author} '
                    msg += f'({message.author.id}): '
                    msg += f'{message.content}\n'
                from io import BytesIO
                data = BytesIO(bytes(msg, 'utf-8'))
                embed = discord.Embed(title=f'{len(messages)} mensagens deletadas',
                                      colour=discord.Colour.random(),
                                      description=f'Chat: {messages[0].channel.mention}\n',
                                      timestamp=datetime.utcnow())
                embed.set_footer(text=f'{messages[0].author}', icon_url=messages[0].author.avatar.url)
                file = discord.File(data,
                                    f'bulk_message_delete_'
                                    f'{messages[0].guild.name.replace(" ", "_")}-'
                                    f'{messages[0].channel.name.replace(" ", "_")}-'
                                    f'{messages[0].created_at.strftime("%d-%m-%Y_%H-%M-%S")}.log')
                return await channel.send(embed=embed, file=file)


def setup(bot):
    cog = LogEvent(bot)
    cmds = f'{Fore.BLUE}{len(cog.get_listeners())}{Fore.LIGHTMAGENTA_EX}'
    print(f'{Style.BRIGHT}{Fore.GREEN}[{"EVENT LOADED":^16}]' +
          f'{Fore.LIGHTMAGENTA_EX}{cog.qualified_name}({cmds}){Style.RESET_ALL}'.rjust(60))
    bot.add_cog(cog)
