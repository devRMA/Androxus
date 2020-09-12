# coding=utf-8
# Androxus bot
# main.py

__author__ = 'Rafael'

from discord.dao.ServidorDao import ServidorDao
from discord.dao.BlacklistDao import BlacklistDao
from discord.ext import commands
import discord
from os import environ, listdir


def pegar_o_prefixo(bot, message):
    if message.guild != None:
        prefixo = ServidorDao().get_prefix(message.guild.id)[0]
        if prefixo != None:
            return prefixo
    return '--'


bot = commands.Bot(command_prefix=pegar_o_prefixo, owner_id=305532760083398657)
bot.remove_command('help')  # remove o comando help que já vem


@bot.event
async def on_ready():
    print('Bot online :D')
    print(f'Logado em {bot.user}')
    print(f'ID: {bot.user.id}')
    print(f'link de acesso:\nhttps://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8')
    await bot.change_presence(activity=discord.Game(
        name='😁Caso você queira ver minha programação, acesse https://github.com/devRMA/Androxus'))


@bot.event
async def on_guild_join(guild):
    if await ServidorDao.create(guild.id):
        print(f'Servidor {guild} adicionado com sucesso!')

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
