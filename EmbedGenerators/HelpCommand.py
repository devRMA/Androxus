# -*- coding: utf-8 -*-
# Androxus bot
# HelpCommand.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.ext import commands

from Classes.General import Androxus
from Classes.Erros import Stop
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ServidorRepository import ServidorRepository


async def embed_help_command(ctx, command=None, color=None):
    """

    Args:
        ctx (commands.context.Context): O contexto que vai ser usado para pegar o prefixo e o comando
        command (commands.Command): O comando que vai ser criado o embed (Default value = ctx.command)
        color (hex): Cor que vai ser usada no embed (Default value = random)

    Returns:
        discord.Embed: O embed com a mensagem de help do comando

    """
    if command is None:
        command = ctx.command
    color = discord.Colour(int(color)) if color else discord.Colour.random()
    bot: Androxus = ctx.bot
    prefix = (await bot.get_prefix(ctx.message))[-1]
    infos = await bot.translate(ctx, help_=command.name, values_={
        'prefix': prefix
    })
    perm_user = infos.get('perm_user')
    perm_bot = infos.get('perm_bot')
    description = infos.get('description')
    examples = '\n'.join(infos.get('examples'))
    aliases = command.aliases.copy()
    how_to_use = infos.get('how_to_use')
    have_parameters = '[' in how_to_use or '<' in how_to_use
    disabled_command = False
    if ctx.guild:
        server = await ServidorRepository().get_servidor(bot.db_connection, ctx.guild.id)
        commands_disable = await ComandoDesativadoRepository().get_commands(bot.db_connection, server)
        try:
            for cmd_obj in commands_disable:
                if command.name in cmd_obj.comando:  # vê se o nome do comando, está desativado
                    disabled_command = True
                    break
                for alias in aliases:  # vai verificar se algum "alias" desse comando, está desativado
                    if alias in cmd_obj.comando:
                        disabled_command = True
                        raise Stop()  # foi usado o raise, para conseguir parar os dois laços
        except Stop:
            pass
    if aliases:
        aliases = list(map(lambda a: f'`{a}`', aliases))
    embed_info = await bot.translate(ctx, others_='help_command', values_={
        'command_name': command.name,
        'description': description,
        'perm_user': perm_user,
        'perm_bot': perm_bot,
        'atencao': bot.get_emoji('atencao')
    })
    perm_user = embed_info['perm_user'] if perm_user else ''
    perm_bot = embed_info['perm_bot'] if perm_bot else ''
    embed = discord.Embed(title=embed_info['title'],
                          colour=color,
                          description=embed_info['description'],
                          timestamp=datetime.utcnow())
    embed.set_author(name=bot.user.name,
                     icon_url=bot.user.avatar.url)
    embed.set_footer(text=f'{ctx.author}',
                     icon_url=ctx.author.avatar.url)
    embed.add_field(name=embed_info['how_to_use'],
                    value=how_to_use,
                    inline=False)
    embed.add_field(name=embed_info['example' if len(examples) == 1 else 'examples'],
                    value=examples,
                    inline=False)
    if aliases:
        embed.add_field(name=embed_info['aliases'],
                        value=', '.join(aliases),
                        inline=False)
    if perm_user != '' or perm_bot != '':
        embed.add_field(name=embed_info['requirements'],
                        value=perm_user + perm_bot,
                        inline=False)
    if disabled_command:
        embed.add_field(name=embed_info['disabled_command_name'],
                        value=embed_info['disabled_command_value'],
                        inline=False)
    if have_parameters:
        embed.add_field(name=embed_info['parameters'],
                        value='** **',
                        inline=False)
    return embed
