# -*- coding: utf-8 -*-
# Androxus bot
# HelpGroup.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.ext import commands

from utils.Utils import capitalize


async def embed_help_group(ctx, group=None, group_commands=None, color=None):
    """

    Args:
        ctx (commands.context.Context): O contexto da mensagem
        group (commands.core.Group or str): Grupo que vai ser extraido os comandos (Default value = ctx.command)
        group_commands (list): A lista com os comandos, do grupo (Default value = group.commands)
        color(hex): A cor que vai ser usada nos embeds. (Default value = random)

    Returns:
        discord.Embed: O embed com todos os comandos do grupo passado

    """
    if group is None:
        group = ctx.command
    if group_commands is None:
        group_commands = map(lambda c: c.name, group.commands)
    group_commands = sorted(group_commands)
    group_name = group if isinstance(group, str) else group.name
    bot = ctx.bot
    groups_name = (await bot.translate(ctx, others_='help')).get('groups', {})
    color = discord.Colour(int(color)) if color else discord.Colour.random()
    info = await bot.translate(ctx, others_='help_group', values_={
        'emoji': bot.get_emoji(group_name),
        'group_name': capitalize(groups_name.get(group_name)),
        'prefix': (await bot.get_prefix(ctx.message))[-1]
    })
    e = discord.Embed(title=info['title'],
                      colour=color,
                      description=info['description'],
                      timestamp=datetime.utcnow())
    e.set_author(name=bot.user.name,
                 icon_url=bot.user.avatar.url)
    e.set_footer(text=f'{ctx.author}',
                 icon_url=ctx.author.avatar.url)
    e.add_field(name=info['field_name'],
                value=', '.join(f'`{c}`' for c in group_commands),
                inline=False)
    return e
