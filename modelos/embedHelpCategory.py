# coding=utf-8
# Androxus bot
# eHelpCategory.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.ext import commands

from Classes.Androxus import Androxus
from database.Conexao import Conexao
from utils.Utils import capitalize
from utils.Utils import random_color, pegar_o_prefixo


def embedHelpCategory(bot: Androxus = None,
                      ctx: commands.Context = None,
                      category: str = None):
    conexao = Conexao()
    # se a pessoa usou o comando, mencionando o bot:
    if ctx.prefix.replace("!", "").replace(" ", "") == bot.user.mention:
        # vai pegar o prefixo que está no banco
        prefixo = pegar_o_prefixo(bot, ctx, False, conexao)
    else:
        # se a pessoa não marcou o bot:
        prefixo = ctx.prefix
    e = discord.Embed(title=f'Categoria: {bot.get_emoji_from_category(category)} {capitalize(category)}',
                      colour=discord.Colour(random_color()),
                      description='Todos os comandos que estão nesta categoria!\nPara obter mais detalhes sobre '
                                  f'um comando, digite `{prefixo}help comando`!',
                      timestamp=datetime.utcnow())
    e.set_author(name='Androxus',
                 icon_url=bot.user.avatar_url)
    e.set_footer(text=f'{ctx.author}',
                 icon_url=ctx.author.avatar_url)
    comandos = [f'``{c.name}``' for c in bot.get_commands_from_category(category)]
    comandos = ', '.join(comandos)
    e.add_field(name='📖 Comandos:',
                value=comandos,
                inline=False)
    conexao.fechar()
    return e
