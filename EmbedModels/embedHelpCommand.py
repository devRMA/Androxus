# -*- coding: utf-8 -*-
# Androxus bot
# embedHelpCommand.py

__author__ = 'Rafael'

from datetime import datetime

import discord

from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils.Utils import random_color, pegar_o_prefixo


async def embed_help_command(bot, ctx, comando=None, descricao=None, parametros=None, exemplos=None,
                             aliases=None, perm_pessoa=None, perm_bot=None, cor=None):
    """

    Args:
        bot (Classes.Androxus.Androxus): A instância do bot
        ctx (discord.ext.commands.context.Context): O contexto que vai ser usado para pegar o prefixo e o comando
        comando (str): O comando que vai ser criado o embed (Default value = ctx.command.name)
        descricao (str): A descrição do comando (Default value = ctx.command.description)
        parametros (list): Lista de parâmetros do comando (Default value = ctx.command.parameters)
        exemplos (list): Lista com exemplos de uso do comando (Default value = ctx.command.examples)
        aliases (list): Lista de "sinônimos" do comando (Default value = ctx.command.aliases)
        perm_pessoa (str): Permissão que o usuário precisa ter para usar o comando (Default value = ctx.command.perm_user)
        perm_bot (str): Permissão que o bot precisa ter executar o comando (Default value = ctx.command.perm_bot)
        cor (hex): Cor que vai ser usada no embed (Default value = random)

    Returns:
        discord.Embed: O embed com a mensagem de help do comando

    """
    embed_error = discord.Embed(title='Comando não encontrado',
                                timestamp=datetime.utcnow())
    embed_error.set_author(name=ctx.author.name, icon_url=bot.user.avatar_url)
    if not ctx.valid:
        return embed_error
    if ctx.command.hidden or (not hasattr(ctx.command, 'perm_user')):
        return embed_error
    # se a pessoa usou o comando, mencionando o bot:
    if ctx.prefix.replace("!", "").replace(" ", "") == bot.user.mention:
        # vai pegar o prefixo que está no banco
        prefixo = await pegar_o_prefixo(bot, ctx)
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
    if parametros is None:
        parametros = ctx.command.parameters.copy()
    if exemplos is None:
        exemplos = ctx.command.examples.copy()
    if aliases is None:
        aliases = ctx.command.aliases.copy()
    if perm_pessoa is None:
        perm_pessoa = ctx.command.perm_user
    if perm_bot is None:
        perm_bot = ctx.command.perm_bot
    exemplo = '\n'.join(exemplos)
    exemplo = exemplo.replace('{prefix}', ctx.prefix)
    exemplo = exemplo.replace('{author_mention}', ctx.author.mention)
    exemplo = exemplo.replace('{this_channel}', ctx.channel.mention)
    como_usar = f'``{prefixo}{comando}`` '
    comando_esta_desativado = False
    if ctx.guild is not None:  # se a mensagem foi enviar de um server
        servidor = await ServidorRepository().get_servidor(bot.db_connection, ctx.guild.id)
        cmds_desativados = await ComandoDesativadoRepository().get_commands(bot.db_connection, servidor)
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
    embed = discord.Embed(title=f'🔑 Detalhes sobre o comando ``{prefixo}{comando}``',
                          colour=discord.Colour(cor_a_usar),
                          description=descricao,
                          timestamp=datetime.utcnow())
    embed.set_author(name=bot.user.name,
                     icon_url=bot.user.avatar_url)
    embed.set_footer(text=f'{ctx.author}',
                     icon_url=ctx.author.avatar_url)
    embed.add_field(name='🤔 **Como usar?**',
                    value=como_usar,
                    inline=False)
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
            name=f"{bot.emoji('atencao')} **O comando foi desativado por algum administrador do server!**",
            value="**Se você usar este comando, eu não irei responder!**",
            inline=False)
    if parametros:
        embed.add_field(
            name='** **',
            value=f'{bot.emoji("atencao")} Tudo que estiver entre **<>** é obrigatório, e tudo que estiver '
                  'entre **[]** é opcional.', inline=False)
    return embed
