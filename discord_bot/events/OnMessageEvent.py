# coding=utf-8
# Androxus bot
# OnMessageEvent.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from stopwatch import Stopwatch

from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.BlacklistRepository import BlacklistRepository
from discord_bot.database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from discord_bot.database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from discord_bot.database.Repositories.ServidorRepository import ServidorRepository
from discord_bot.database.Servidor import Servidor


async def on_message_event(bot, message):
    if not bot.is_ready():
        return
    if message.author.id == bot.user.id:
        return
    stopwatch = Stopwatch()
    ctx = await bot.get_context(message)
    # se a pessoa não usar um comando do bot, vai chegar None como prefixo
    conexao = Conexao()
    if message.guild:
        prefixo = ServidorRepository().get_prefix(conexao, message.guild.id)
    else:
        prefixo = ''
    banido = BlacklistRepository().get_pessoa(conexao, message.author.id)
    servidor = None
    if message.guild:
        servidor = Servidor(message.guild.id, prefixo)
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
            # aqui, estamos retirando o prefixo da mensagem, e pegando apenas a primeira palavra da mensagem
            if message.content.lower().replace(prefixo, '').split(' ')[0] in comando_desativado.comando:
                # se ela corresponder, a um comando que está desativado:
                await message.channel.send('<a:no_no:755774680325029889> Este comando ' +
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
                        if not comando_personalizado.inText:
                            if not message.content.lower().startswith(comando_personalizado.comando.lower()):
                                # se for obrigatorio que a mensagem comesse com o comando, e ela não estiver começando
                                enviar_mensagem = False  # não vai responder
                        if enviar_mensagem:
                            stopwatch.stop()
                            await channel.send(comando_personalizado.resposta.format(tempo=str(stopwatch)))
                            return
    if (f'<@{str(bot.user.id)}>' == message.content) or (f'<@!{str(bot.user.id)}>' == message.content):
        await channel.send(f'Use o comando ``{prefixo}help`` para obter ajuda!')
        await channel.send('<a:hello:755774680949850173>')
    conexao.fechar()
    stopwatch.stop()
    await bot.process_commands(message)
    
