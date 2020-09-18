# coding=utf-8
# Androxus bot
# main.py

__author__ = 'Rafael'

from discord.dao.ServidorDao import ServidorDao  # classe que vai adicionar/remover servidores no banco
import discord  # import da API do discord
from discord.ext import commands, tasks  # outros imports do discord
from os import environ  # função responsável por pegas o token do bot
from os import listdir  # função responsável por pegar todos os cogs
from discord.Utils import pegar_o_prefixo  # função que vai ser usada toda vez que enviarem uma mensagem
from sys import version  # função para pegar a versão do python
from discord.events.OnMessageEvent import on_message_event  # evento que vai ser chamado, toda vez que enviarem uma menasgem
from random import choice  # função que vai ser usada para escolher "aleatóriamente" qual status do bot
# instanciamento do bot em si, passando a função "pegar_o_prefixo" no prefixo
bot = commands.Bot(command_prefix=pegar_o_prefixo, owner_id=305532760083398657)
bot.remove_command('help')  # remove o comando help default


@bot.event
async def on_ready():
    # esse evento só vai ser chamado uma vez, que é quando o bot iniciar
    print('Bot online!')
    print(f'Logado em {bot.user}')
    print(f'ID: {bot.user.id}')
    print(f'Versão do discord.py: {discord.__version__}')
    print(f'Versão do python: {version[0:5]}')
    change_status.start()  # inicia o loop para mudar o status


@bot.event
async def on_guild_join(guild):
    # toda vez que adicionarem o bot num servidor, vai adicionar o servidor ao banco
    ServidorDao().create(guild.id)


@bot.event
async def on_guild_remove(guild):
    # toda vez que removerem o bot de um servidor, vai remover o servidor do banco
    ServidorDao().delete(guild.id)


@bot.event
async def on_message(message):
    # toda mensagem que for enviada, vai ir para a função "on_message_event"
    await on_message_event(bot, message)


@bot.event
async def on_message_edit(before, after):
    # caso a pessoa tinha digitado um comando errado, e depois editado para um comando valido, vai ser verificado também
    await on_message_event(bot, after)


@tasks.loop(seconds=10)
async def change_status():  # loop que vai ficar alterando o status do bot
    status = ['Para me adicionar em um servidor, basta enviar a mensagem ``invite`` no meu privado!',
              # lista com os status
              'Eu estou divertindo {servers} servidores!',
              'Caso você precise de ajuda, basta me mencionar.',
              '🤔 como que eu estou "jogando" se eu sou um bot? 🤔']
    status_escolhido = choice(status)  # escolhe um status "aleatório"
    # vai substituir pela quantidade de servidores que o bot está
    status_escolhido = status_escolhido.replace('{servers}', f'{len(bot.guilds)}')
    await bot.change_presence(activity=discord.Game(name=status_escolhido))  # muda o status do bot


if __name__ == '__main__':
    try:
        listdir('discord/cmds')  # vai tentar achar a pasta "discord/cmd"
        path_cmds = 'discord/cmds'  # se achar, salva o path
    except FileNotFoundError:  # se não achar, salva o path como "./cmds"
        path_cmds = './cmds'
    for filename in listdir(path_cmds):  # vai listar todas os arquivos que tem na pasta "cmds"
        if filename.endswith('.py'):  # se o arquivo terminar com ".py"
            bot.load_extension(f'cmds.{filename[:-3]}')  # vai adicionar ao bot
    bot.run(environ.get('TOKEN'))  # inicia o bot
