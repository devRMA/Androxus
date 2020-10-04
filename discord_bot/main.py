# coding=utf-8
# Androxus bot
# main.py

__author__ = 'Rafael'

from datetime import datetime  # Esse módulo vai ser usado para definir a hora que o bot iniciou
from os import environ  # função responsável por pegas o token do bot
from os import listdir  # função responsável por pegar todos os cogs
from random import choice  # função que vai ser usada para escolher "aleatoriamente" qual status do bot
from sys import version  # função para pegar a versão do python

import discord  # import da API do discord
from discord.ext import commands, tasks  # outros imports do discord

# evento que vai ser chamado, toda vez que enviarem uma mensagem
from discord_bot.events.OnMessageEvent import on_message_event
from discord_bot.utils.Utils import get_configs  # função que pega as configurações do json
from discord_bot.utils.Utils import pegar_o_prefixo  # função que vai ser usada toda vez que enviarem uma mensagem

configs = get_configs()

# criação do bot em si, passando a função "pegar_o_prefixo" no prefixo
if len(configs['owners']) > 1:
    bot = commands.Bot(command_prefix=pegar_o_prefixo,
                       owner_ids=configs['owners'],
                       case_insensitive=True)
else:
    bot = commands.Bot(command_prefix=pegar_o_prefixo,
                       owner_id=configs['owners'][0],
                       case_insensitive=True)
bot.remove_command('help')  # remove o comando help default


@bot.event
async def on_ready():
    # esse evento vai ser chamado quando o bot iniciar
    print('Bot online!')
    print(f'Logado em {bot.user}')
    print(f'ID: {bot.user.id}')
    print(f'Versão do discord.py: {discord.__version__}')
    print(f'Versão do python: {version[0:5]}')
    if not hasattr(bot, 'uptime'):  # se o bot não tiver o atributo "uptime"
        bot.uptime = datetime.utcnow()  # vai criar o atributo, com a data e hora atual
    if not hasattr(bot, 'mudar_status'):  # se o bot não tiver o atributo "mudar_status"
        bot.mudar_status = True  # atributo que vai ficar responsável por controlar a mudança de status
    if not hasattr(bot, 'msg_traduzidas'):  # se o bot não tiver o atributo "msg_traduzidas"
        bot.msg_traduzidas = []  # atributo que vai evitar que a pessoa fique pedindo para traduzir a msm mensagem
    if not hasattr(bot, 'dm_channel_log'):  # se o bot não tiver o atributo "dm_channel_log"
        # esse atributo vai ser responsável por guardar o chat
        # que o bot vai usar quando mandarem mensagem no privado dele
        bot.dm_channel_log = bot.get_channel(configs['dm_channel'])
    try:
        change_status.start()  # inicia o loop para mudar o status
    except RuntimeError:
        pass


@bot.event
async def on_message(message):
    # toda mensagem que for enviada, vai ir para a função "on_message_event"
    try:
        await on_message_event(bot, message)
    except discord.errors.NotFound:
        pass


@bot.event
async def on_message_edit(before, after):
    # caso a pessoa tinha digitado um comando errado, e depois editado para um comando valido, vai ser verificado também
    try:
        await on_message_event(bot, after)
    except discord.errors.NotFound:
        pass


@tasks.loop(seconds=10)
async def change_status():  # loop que vai ficar alterando o status do bot
    if bot.mudar_status:
        # lista com os status
        status = ['Para me adicionar em um servidor, basta enviar a mensagem "invite" no meu privado!',
                  'Eu estou divertindo {servers} servidores!',
                  'Estou divertindo {pessoas} pessoas',
                  'Caso você precise de ajuda, basta me mencionar!',
                  '🤔 como que eu estou "jogando" se eu sou um bot?',
                  'Caso você queira saber mais detalhes sobre mim, use o comando "botinfo"!',
                  'Caso você queira ver meu código fonte, use o comando "source"!']
        status_escolhido = choice(status)  # escolhe um status "aleatório"
        status_escolhido = status_escolhido.format(servers=len(bot.guilds), pessoas=len(bot.users))
        await bot.change_presence(activity=discord.Game(name=status_escolhido))  # muda o status do bot


if __name__ == '__main__':
    try:
        listdir('discord_bot/')  # vai tentar achar a pasta "discord/cmd"
        path = 'discord_bot/'  # se achar, salva o path
    except FileNotFoundError:  # se não achar, salva o path como "./cmds"
        path = './'
    for filename in listdir(f'{path}cmds'):  # vai listar todas os arquivos que tem na pasta "cmds"
        if filename.endswith('.py'):  # se o arquivo terminar com ".py"
            try:
                bot.load_extension(f'cmds.{filename[:-3]}')  # vai adicionar ao bot
            except commands.NoEntryPointError:
                print(f'⚠ - Módulo {filename[:-3]} ignorado! "def setup" não encontrado!!')
            except Exception as e:
                print(f'⚠ - Módulo {filename[:-3]} deu erro na hora de carregar!\nerro: {e}')
    for filename in listdir(f'{path}events'):  # vai listar todas os arquivos que tem na pasta "events"
        if filename.endswith('.py'):  # se o arquivo terminar com ".py"
            try:  # vai verificar se o arquivo tem o "def setup"
                bot.load_extension(f'events.{filename[:-3]}')  # vai adicionar ao bot
            except commands.NoEntryPointError:
                pass  # se não achar o def setup
            except:
                print(f'⚠ - Módulo {filename[:-3]} não foi carregado!')
    if configs['token'] == 'token_bot':
        token = environ.get('TOKEN')
    else:
        token = configs['token']
    bot.run(token)  # inicia o bot
