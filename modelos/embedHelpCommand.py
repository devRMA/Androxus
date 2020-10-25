# coding=utf-8
# Androxus bot
# embedHelpCommand.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.ext import commands

from Classes.Androxus import Androxus
from database.Conexao import Conexao
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils.Utils import random_color, pegar_o_prefixo


def embedHelpCommand(bot: Androxus = None,
                     ctx: commands.Context = None,
                     comando: str = None,
                     descricao: str = None,
                     parametros: list = [],
                     exemplos: list = [],
                     aliases: list = [],
                     perm_pessoa: str = None,
                     perm_bot: str = None,
                     cor: int = None):
    conexao = Conexao()
    # se a pessoa usou o comando, mencionando o bot:
    if ctx.prefix.replace("!", "").replace(" ", "") == bot.user.mention:
        # vai pegar o prefixo que está no banco
        prefixo = pegar_o_prefixo(bot, ctx, False, conexao)
    else:
        # se a pessoa não marcou o bot:
        prefixo = ctx.prefix
    # se a cor não for passada, vai ser usada uma cor aleatória
    cor_a_usar = cor or random_color()
    if comando is None:
        comando = ctx.command.name
    if descricao is None:
        descricao = ctx.command.description
    # precisa fazer uma copia da lista, senão
    # as alterações feitas aqui
    # vão refletir no comando fora da função
    if len(parametros) == 0:
        parametros = ctx.command.parameters.copy()
    if len(exemplos) == 0:
        exemplos = ctx.command.examples.copy()
    if len(aliases) == 0:
        aliases = ctx.command.aliases.copy()
    if perm_pessoa is None:
        perm_pessoa = ctx.command.perm_user
    if perm_bot is None:
        perm_bot = ctx.command.perm_bot
    exemplo = '\n'.join(exemplos).format(prefix=ctx.prefix,
                                         author_mention=ctx.author.mention,
                                         this_channel=f'<#{ctx.channel.id}>')
    como_usar = f'``{prefixo}{comando}`` '
    comando_esta_desativado = False
    if ctx.guild is not None:  # se a mensagem foi enviar de um server
        servidor = ServidorRepository().get_servidor(conexao, ctx.guild.id)
        cmds_desativados = ComandoDesativadoRepository().get_commands(conexao, servidor)
        # for em todos os comandos desativados
        try:
            for comando_desativado in cmds_desativados:
                if comando in comando_desativado.comando:  # vê se o comando principal, está desativado
                    comando_esta_desativado = True
                    break
                for comando_alias in aliases:  # vai verificar se algum "sinônimo" desse comando, está desativado
                    if comando_alias in comando_desativado.comando:  # verifica se o comando está desativado
                        comando_esta_desativado = True
                        raise Exception()
        except Exception:  # foi usado raise error, para conseguir parar os dois laços
            pass
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
    embed = discord.Embed(title=f'``{prefixo}{comando}``',
                          colour=discord.Colour(cor_a_usar),
                          description=descricao,
                          timestamp=datetime.utcnow())
    embed.set_author(name='Androxus',
                     icon_url=bot.user.avatar_url)
    embed.set_footer(text=f'{ctx.author}',
                     icon_url=ctx.author.avatar_url)
    embed.add_field(name='**Como usar?**',
                    value=como_usar,
                    inline=False)
    if parametros:  # novamente, só vai entrar, se tiver pelo menos 1 item nos parâmetros
        embed.add_field(
            name=f'{bot.configs["emojis"]["atencao"]} Tudo que estiver entre **<>** é obrigatório, e tudo que estiver '
                 'entre **[]** é opcional.',
            value='** **', inline=False)
    embed.add_field(name='📖 Exemplo',
                    value=exemplo,
                    inline=False)
    if aliases:
        embed.add_field(name=':twisted_rightwards_arrows: Sinônimos',
                        value=alias,
                        inline=False)
    if perm_pessoa or perm_bot:
        requisito_p = ''
        requisito_b = ''
        if perm_pessoa:
            requisito_p = f'Você precisa ter permissão de ``{perm_pessoa}`` para usar este comando!'
        if perm_bot:
            requisito_b = f'\nEu preciso ter permissão de ``{perm_bot}`` para realizar este comando!'
        embed.add_field(name=':name_badge: Requisitos:',
                        value=f'{requisito_p}{requisito_b}',
                        inline=False)
    if comando_esta_desativado:  # se o comando estiver desativado
        embed.add_field(
            name=f"{bot.configs['emojis']['atencao']} **O comando foi desativado por algum administrador do server!**",
            value="**Se você usar este comando, eu não irei responder!**",
            inline=False)
    conexao.fechar()
    return embed
