# coding=utf-8
# Androxus bot
# main.py

__author__ = 'Rafael'

from discord.dao.ServidorDao import ServidorDao
from discord.ext import commands
import discord
from os import environ, listdir

from discord.Utils import pegar_o_prefixo

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
    from stopwatch import Stopwatch
    msg = await bot.get_channel(753347222275620903).send('conexão com o banco iniciada')
    stopwatch = Stopwatch()
    print(pegar_o_prefixo(None, 753347222275620903))  # vai abrir a conexão com o banco, fazer um select, e fechar a conexão
    stopwatch.stop()
    await msg.edit(content=f'Demorou {str(stopwatch)} para abrir a conexão, fazer um select e fechar a conexao\n' +
                   f'Latência do bot: {int(bot.latency * 1000)}ms')
    await bot.change_presence(activity=discord.Game(
        name='😁Caso você queira ver minha programação, acesse https://github.com/devRMA/Androxus'))


@bot.event
async def on_guild_join(guild):
    ServidorDao().create(guild.id)


@bot.event
async def on_guild_remove(guild):
    ServidorDao().delete(guild.id)


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
