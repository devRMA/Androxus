# coding=utf-8
# Androxus bot
# main.py

__author__ = 'Rafael'

from discord.dao.ServidorDao import ServidorDao
from discord.ext import commands
import discord
from os import environ, listdir
from discord.Utils import pegar_o_prefixo
from discord.dao.BlacklistDao import BlacklistDao
from discord.dao.ComandoDesativadoDao import ComandoDesativadoDao

bot = commands.Bot(command_prefix=pegar_o_prefixo, owner_id=305532760083398657)
bot.remove_command('help')  # remove o comando help que já vem


@bot.event
async def on_ready():
    print('Bot online :D')
    print(f'Logado em {bot.user}')
    print(f'ID: {bot.user.id}')
    print(f'Versão do discord.py: {discord.__version__}')
    print(
        f'link para adicionar o bot:\nhttps://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8')
    await bot.change_presence(activity=discord.Game(
        name='😁Caso você queira ver minha programação, acesse https://github.com/devRMA/Androxus'))


@bot.event
async def on_guild_join(guild):
    ServidorDao().create(guild.id)


@bot.event
async def on_guild_remove(guild):
    ServidorDao().delete(guild.id)

@bot.event
async def on_message(message):
    # verifica se a pessoa pode usar o comando, verifica se o comando está ativado e verifica se a pessoa é um bot
    prefixo = pegar_o_prefixo(None, message)
    if BlacklistDao().get_pessoa(message.author.id) or message.author.bot: return
    if message.guild is not None:  # Se foi usado num server, vai ver se o comando está desativado
        for comandos_desativados in ComandoDesativadoDao().get_comandos(message.guild.id):
            for palavra in message.content.lower().replace(prefixo, '').split(' '):
                if (palavra == 'reativar_comando') or (palavra == 'reactivate_command'):
                    break
                if palavra in comandos_desativados:
                    await message.channel.send(f'Este comando foi desativado ;-;')
                    return
    if message.author.id == bot.user.id: return
    await bot.process_commands(message)  # Vai para os comandos cogs

if __name__ == '__main__':
    try:
        listdir('discord/cmds')
        path_cmds = 'discord/cmds'
    except FileNotFoundError:
        path_cmds = './cmds'
    for filename in listdir(path_cmds):
        if filename.endswith('.py'):
            bot.load_extension(f'cmds.{filename[:-3]}')
    bot.run(environ.get('TOKEN'))
