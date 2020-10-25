# coding=utf-8
# Androxus bot
# OnMessageEvent.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from stopwatch import Stopwatch

from database.Conexao import Conexao
from database.Repositories.BlacklistRepository import BlacklistRepository
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils import permissions


async def on_message_event(bot, message):
    if not bot.is_ready():
        return
    try:
        permissions.is_owner(message)
    except discord.ext.commands.errors.NotOwner:
        # se a pessoa não for dona do bot, e ele estiver em manutenção, simplesmente ignora a mensagem
        if bot.maintenance_mode:
            return
    if message.author.id == bot.user.id:
        return
    if message.is_system():
        return
    ctx = await bot.get_context(message)
    if not permissions.can_send(ctx):
        # se o bot não tiver permissão para enviar mensagens:
        return
    stopwatch = Stopwatch()
    # se a pessoa não usar um comando do bot, vai chegar None como prefixo
    conexao = Conexao()
    servidor = None
    if message.guild:
        servidor = ServidorRepository().get_servidor(conexao, message.guild.id)
    if servidor:
        prefixo = servidor.prefixo
    else:
        prefixo = ''
    banido = BlacklistRepository().get_pessoa(conexao, message.author.id)[0]
    if banido or message.author.bot:
        stopwatch.stop()
        return conexao.fechar()
    if isinstance(message.channel, discord.DMChannel):  # se a mensagem foi enviada no dm
        embed = discord.Embed(title=f'O(A) {message.author} mandou mensagem no meu dm',
                              colour=0xfdfd96,
                              description=f'{message.content}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{message.author.id}',
                         icon_url='https://media-exp1.licdn.com/dms/image/C510BAQHhOjPujl' +
                                  'cgfQ/company-logo_200_200/0?e=2159024400&v=beta&t=49' +
                                  'Ex7j5UkZroF7-uzYIxMXPCiV7dvtvMNDz3syxcLG8')
        if len(message.attachments) != 0:
            for attachment in message.attachments:
                embed.set_image(url=attachment.url)
        embed.set_thumbnail(url=message.author.avatar_url)
        await bot.dm_channel_log.send(embed=embed)
    if message.mention_everyone:  # verifica se marcou here ou everyone
        emoji = bot.get_emoji(755774680220172340)  # emoji de ping pistola
        await message.add_reaction(emoji)  # adiciona a reação com o emoji
    if servidor:  # Se foi usado num server, vai ver se o comando está desativado
        # aqui, vai verificar se o comando foi desativado
        for comando_desativado in ComandoDesativadoRepository().get_commands(conexao, servidor):
            # aqui, estamos retirando o prefixo da mensagem, e criando uma lista com todas as palavras
            palavras_formatadas = message.content.lower().replace(prefixo, '').split(' ')
            # se a primeira palavra, for diferente de '' e o comando desativado estiver nela:
            if (palavras_formatadas[0] != '') and (
                    comando_desativado.comando.lower() in palavras_formatadas[0].lower()):
                # se ela corresponder, a um comando que está desativado:
                await message.channel.send(f'{bot.configs["emojis"]["no_no"]} Este comando ' +
                                           'foi desativado por um administrador do servidor!')
                stopwatch.stop()
                return conexao.fechar()
    channel = message.channel
    usando_comando = False
    if servidor:  # se a mensagem foi enviar num servidor
        try:
            #  como tem 3 for, um dentro do outro, é mais facil força um erro, do que ir dando break em cada um
            for cog in bot.cogs:  # verifica se a mensagem, está chamando algum comando
                # laço que vai passar por todos os comandos que o bot tem
                for command in bot.get_cog(cog).get_commands():
                    if message.content.lower().startswith(f'{prefixo}{command.name}'):  # Se a mensagem tiver o comando
                        usando_comando = True
                        raise Exception()  # para o laço
                    for aliases in command.aliases:  # também verifica os "sinônimos"
                        if message.content.lower().startswith(f'{prefixo}{aliases}'):  # se achar o comando
                            usando_comando = True
                            raise Exception()  # para o laço
        except Exception:
            pass
        if not usando_comando:  # se não estiver usando um comando do bot
            # vai ver se a pessoa usou algum comando personalizado
            # só existem comandos personalizados em servidores, então aqui verifica se está num server
            if servidor:
                for comando_personalizado in ComandoPersonalizadoRepository().get_commands(conexao, servidor):
                    # se identificar o comando, na mensagem
                    if comando_personalizado.comando.lower() in message.content.lower():
                        enviar_mensagem = True
                        # se não for para ignorar a posição, vai ver se a mensagem inicia com o comando
                        if not comando_personalizado.in_text:
                            if not message.content.lower().startswith(comando_personalizado.comando.lower()):
                                # se for obrigatorio que a mensagem comesse com o comando, e ela não estiver começando
                                enviar_mensagem = False  # não vai responder
                        if enviar_mensagem:
                            stopwatch.stop()
                            await channel.send(comando_personalizado.resposta.format(tempo=str(stopwatch)))
                            return
    if (f'<@{str(bot.user.id)}>' == message.content) or (f'<@!{str(bot.user.id)}>' == message.content):
        await channel.send(f'Use o comando ``{prefixo}cmds`` para obter todos os meus comandos!')
        if permissions.can_use_external_emojis(ctx):
            await channel.send(bot.configs["emojis"]["hello"])
        conexao.fechar()
        stopwatch.stop()
        return
    conexao.fechar()
    stopwatch.stop()
    await bot.process_commands(message)
