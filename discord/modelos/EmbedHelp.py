# coding=utf-8
# Androxus bot
# EmbedHelp.py

__author__ = 'Rafael'

import discord
from discord.ext import commands
from datetime import datetime
from discord.Utils import random_color, pegar_o_prefixo, get_emoji_dance


def embedHelp(bot: commands.Bot = None,
              ctx: commands.Context = None,
              comando: str = None,
              descricao: str = None,
              parametros: list = [],
              exemplos: list = [],
              aliases: list = [],
              perm_pessoa: str = None,
              perm_bot: str = None):
    prefixo = pegar_o_prefixo(None, ctx)
    exemplos = '\n'.join(exemplos).replace('{pref}', f'{prefixo}')
    aliases = ''
    como_usar = f'``{prefixo}{comando}`` '
    if parametros:  # se tiver pelo menos 1 item nos parâmetros
        for c in range(0, len(parametros)):  # vai adicionar `` antes, e depois dos parâmetros, em todos os itens
            parametros[c] = f'``{parametros[c]}``'
        como_usar += ' '.join(parametros) # adiciona os parâmetros no "como_usar"
    if aliases:
        for c in range(0, len(aliases)):  # vai adicionar `` antes, e depois de alias
            aliases[c] = f'``{prefixo}{aliases[c]}``'
        if len(aliases) == 1:
            aliases = aliases[0]
        else:
            aliases = ', '.join(aliases)
    embed = discord.Embed(title=f'``{prefixo}{comando}``',
                          colour=discord.Colour(random_color()),
                          description=descricao,
                          timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
    embed.set_author(name='Androxus',
                     icon_url=f'{bot.user.avatar_url}')
    embed.set_footer(text=f'{ctx.author}',
                     icon_url=f'{ctx.author.avatar_url}')
    embed.add_field(name='**Como usar?**',
                    value=como_usar,
                    inline=False)
    if parametros:  # novamente, só vai entrar, se tiver pelo menos 1 item nos parâmetros
        embed.add_field(
            name='Tudo que estiver entre **<>** são obrigatorio, e tudo que estiver entre **[]** são opcionais.',
            value=get_emoji_dance(), inline=False)
    embed.add_field(name='Exemplo:',
                    value=exemplos,
                    inline=False)
    embed.add_field(name=':twisted_rightwards_arrows: Sinônimos:',
                    value=aliases,
                    inline=False)
    if perm_pessoa or perm_bot:
        __requisito = ''
        if perm_pessoa:
            __requisito = f'Você precisa ter permissão de ``{perm_pessoa}`` para usar este comando!'
        if perm_bot:
            __requisito = f'\nEu preciso ter permissão de ``{perm_pessoa}`` para realizar este comando!'
        embed.add_field(name='<a:atencao:755844029333110815> Requisitos:',
                        value=__requisito,
                        inline=False)
    return embed
