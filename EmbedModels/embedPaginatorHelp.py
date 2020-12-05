# -*- coding: utf-8 -*-
# Androxus bot
# embedPaginatorHelp.py

__author__ = 'Rafael'

from datetime import datetime

import discord

from utils.Utils import random_color


def get_paginator_help(bot, ctx, color=None):
    """

    Args:
        bot (Classes.Androxus.Androxus): A instância do bot
        ctx (discord.ext.commands.context.Context): O contexto do comando
        color(hex): A cor que vai ser usada nos embeds (Default value = None)

    Returns:
        discord.Embed: O embed com as ajudas

    """
    if color is None:
        color = random_color()
    e = discord.Embed(title='Ajuda com as páginas',
                      description='Enquanto um comando estiver com os emojis para você navegar entre as páginas, '
                                  'você não pode usar o comando de novo!',
                      colour=discord.Colour(color),
                      timestamp=datetime.utcnow())
    e.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    e.set_footer(text=f'{ctx.author} ─ Página de ajuda',
                 icon_url=ctx.author.avatar_url)
    e.add_field(name='Aqui está a legenda do que cada emoji faz.',
                value=':track_previous: ─ Vai para a primeira página.\n'
                      ':arrow_backward: ─ Vai para a página anterior.\n'
                      ':stop_button: ─ Para a execução do comando.\n'
                      ':arrow_forward: ─ Vai para a próxima página.\n'
                      ':track_next: ─ Vai para a última página.\n'
                      ':grey_question: ─ Vem para está página de ajuda.',
                inline=True)
    return e
