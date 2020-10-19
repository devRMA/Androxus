# coding=utf-8
# Androxus bot
# main.py

__author__ = 'Rafael'

from os import environ  # função responsável por pegas o token do bot
from os import listdir  # função responsável por pegar todos os cogs
from random import choice  # função que vai ser usada para escolher "aleatoriamente" qual status do bot
from sys import version  # função para pegar a versão do python

import discord  # import da API do discord
from discord.ext import commands, tasks  # outros imports do discord
from requests import get  # função que vai fazer os requests no site

from Classes.Androxus import Androxus  # classe que herda o commands.Bot
# evento que vai ser chamado, toda vez que enviarem uma mensagem
from events.OnMessageEvent import on_message_event
from utils.Utils import get_configs  # função que pega as configurações do json
from utils.Utils import pegar_o_prefixo  # função que vai ser usada toda vez que enviarem uma mensagem


def prefix_or_mention(bot, message):
    # vai pegar o prefixo que está no banco
    prefixo = pegar_o_prefixo(bot, message)
    # o bot vai responder se ele for mencionado ou quando a mensagem iniciar com o prefixo
    return commands.when_mentioned_or(prefixo)(bot, message)


configs = get_configs()

intents = discord.Intents.default()
intents.members = True
intents.presences = True
# criação do bot em si, passando a função "prefix_or_mention" no prefixo
if len(configs['owners']) > 1:  # se tiver mais de um owner
    bot = Androxus(command_prefix=prefix_or_mention,
                   owner_ids=configs['owners'],
                   case_insensitive=True,
                   intents=intents)
else:  # se só tiver 1:
    bot = Androxus(command_prefix=prefix_or_mention,
                   owner_id=configs['owners'][0],
                   case_insensitive=True,
                   intents=intents)


@bot.event
async def on_ready():
    # esse evento vai ser chamado quando o bot iniciar
    print('Bot online!')
    print(f'Logado em {bot.user}')
    print(f'ID: {bot.user.id}')
    print(f'Versão do discord.py: {discord.__version__}')
    print(f'Versão do python: {version[0:5]}')
    if not bot.configurado:
        bot.configurar()
    try:
        change_status.start()  # inicia o loop para mudar o status
        request_no_site.start()  # inicia o loop que vai fazer os requests no site
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
        if before.content != after.content:
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
                  'Caso você queira ver meu código fonte, use o comando "source"!',
                  'Para saber todos os meus comandos, digite "cmds"!',
                  'Para obter mais informações sobre um comando, use o comando "help comando"!']
        status_escolhido = choice(status)  # escolhe um status "aleatório"
        status_escolhido = status_escolhido.format(servers=len(bot.guilds), pessoas=len(bot.users))
        await bot.change_presence(activity=discord.Game(name=status_escolhido))  # muda o status do bot


@tasks.loop(minutes=3)
async def request_no_site():
    # um request no site, para que ele não fique off
    # como o projeto está no heroku, e é um plano free
    # se o site ficar 5 minutos sem ter um acesso, o heroku
    # desliga a aplicação, então a cada 3 minutos o bot vai fazer
    # um request, para que ele não caia
    url = 'https://androxus.herokuapp.com/'
    html = get(url)
    del (url)
    del (html)


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
