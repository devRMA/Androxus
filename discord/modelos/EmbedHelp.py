# coding=utf-8
# Androxus bot
# EmbedHelp.py

__author__ = 'Rafael'

import discord
from discord.ext import commands
from datetime import datetime
from discord.Utils import random_color, pegar_o_prefixo, get_emoji_dance

from discord.dao.ComandoDesativadoDao import ComandoDesativadoDao


def embedHelp(bot: commands.Bot = None,
              ctx: commands.Context = None,
              comando: str = None,
              descricao: str = None,
              parametros: list = [],
              exemplos: list = [],
              aliases: list = [],
              perm_pessoa: str = None,
              perm_bot: str = None,
              cor: int = None):
    prefixo = pegar_o_prefixo(None, ctx)
    exemplo = '\n'.join(exemplos).replace('{pref}', f'{prefixo}')
    como_usar = f'``{prefixo}{comando}`` '
    comando_esta_desativado = False
    if ctx.guild is not None:  # se a mensagem foi enviar de um server
        for comandos_desativados in ComandoDesativadoDao().get_comandos(ctx.guild.id):  # for em todos os comandos desativados
            if comando_esta_desativado: break  # se, dentro do outro for, achar o comando, vai para o for de fora também
            if comando in comandos_desativados:  # vê se o comando principal, está desativado
                comando_esta_desativado = True
                break
            for comando_alias in aliases:  # vai verificar se algum "sinônimo" desse comando, foi desativado
                if comando_esta_desativado: break
                if (comando_alias in comandos_desativados):  # verifica se o comando está desativado
                    comando_esta_desativado = True
    if parametros:  # se tiver pelo menos 1 item nos parâmetros
        for c in range(0, len(parametros)):  # vai adicionar `` antes, e depois dos parâmetros, em todos os itens
            parametros[c] = f'``{parametros[c]}``'
        como_usar += ' '.join(parametros)  # adiciona os parâmetros no "como_usar"
    if aliases:
        for c in range(0, len(aliases)):  # vai adicionar `` antes, e depois de alias
            aliases[c] = f'``{prefixo}{aliases[c]}``'
        if len(aliases) == 1:
            alias = aliases[0]
        else:
            alias = ', '.join(aliases)
    if cor is None:  # se a cor não for passada, vai ser usada uma cor aleatória
        cor_a_usar = random_color()
    else:  # se passou a cor, usa a cor passada
        cor_a_usar = cor
    embed = discord.Embed(title=f'``{prefixo}{comando}``',
                          colour=discord.Colour(cor_a_usar),
                          description=descricao,
                          timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
    embed.set_author(name='Androxus',
                     icon_url=bot.user.avatar_url)
    embed.set_footer(text=f'{ctx.author}',
                     icon_url=ctx.author.avatar_url)
    embed.add_field(name='**Como usar?**',
                    value=como_usar,
                    inline=False)
    if parametros:  # novamente, só vai entrar, se tiver pelo menos 1 item nos parâmetros
        embed.add_field(
            name='Tudo que estiver entre **<>** são obrigatorio, e tudo que estiver entre **[]** são opcionais.',
            value=get_emoji_dance(), inline=False)
    embed.add_field(name='Exemplo:',
                    value=exemplo,
                    inline=False)
    embed.add_field(name=':twisted_rightwards_arrows: Sinônimos:',
                    value=alias,
                    inline=False)
    if perm_pessoa or perm_bot:
        requisito = ''
        if perm_pessoa:
            requisito = f'Você precisa ter permissão de ``{perm_pessoa}`` para usar este comando!'
        if perm_bot:
            requisito = f'\nEu preciso ter permissão de ``{perm_pessoa}`` para realizar este comando!'
        embed.add_field(name='<a:atencao:755844029333110815> Requisitos:',
                        value=requisito,
                        inline=False)
    if comando_esta_desativado:  # se o comando estiver desativado
        embed.add_field(
            name="<a:atencao:755844029333110815> **O comando foi desativado por algum administrador do server!**",
            value="**Se você usar este comando, eu não irei responder!**",
            inline=False)
    return embed
