# coding=utf-8
# Androxus bot
# main.py

__author__ = 'Rafael'

import os
from discord.dao.ServidorDao import ServidorDao
from discord.ext import commands
import discord
from os import environ


def get_prefixo(bot, message):
    prefixo = ServidorDao().get_prefix(message.guild.id)[0]
    if prefixo != None:
        return prefixo
    else:
        return '--'


modulos = [
    'cmds.Ping',
]

bot = commands.Bot(command_prefix=get_prefixo, owner_id=305532760083398657)
bot.remove_command('help')  # remove o comando help que já vem


@bot.event
async def on_ready():
    print('Bot online :D')
    print(f'Logado em {bot.user}')
    print(f'ID: {bot.user.id}')
    print(f'link de acesso:\nhttps://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8')
    await bot.change_presence(activity=discord.Game(name='🤔 como que eu estou "jogando" se eu sou um bot? 🤔'))


@bot.event
async def on_guild_join(guild):
    if await ServidorDao.create(guild.id):
        print("Server adicionado com sucesso!")
@bot.event
async def on_message(message):
    channel = message.channel
    mensagem_formatada = message.content
    lixos = '!@#$%*()-_=+[{]}/?ç´~;., <>^\\|\'"'
    for char in lixos:
        mensagem_formatada = mensagem_formatada.replace(char, '')
    if (f'<@{str(bot.user.id)}>' in message.content) or (f'<@!{str(bot.user.id)}>' in message.content):
        try:
            await channel.send(f'Use o comando ``{get_prefixo(None, message)}help`` para obter ajuda! xD')
        except Exception as error:
            await channel.send(f'Ocorreu o erro \n```{error}```na execução do comando ._.')

    await bot.process_commands(message)  # caso não tenha passado por nenhuma mensagem a cima, vai para os comandos
@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)  # se a pessoa editar a mensagem, verifica se ela editou para um comando valido

if __name__ == '__main__':
    for filename in os.listdir('./cmds'):
        if filename.endswith('.py'):
            bot.load_extension(f'cmds.{filename[:-3]}')

    bot.run(environ.get('TOKEN'))

