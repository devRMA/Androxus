# coding=utf-8
# Androxus bot
# OnMessageEvent.py

__author__ = 'Rafael'

from discord.ext import commands
from discord.dao.ComandoPersonalizadoDao import ComandoPersonalizadoDao
from discord.Utils import pegar_o_prefixo
from discord.dao.BlacklistDao import BlacklistDao
from discord.dao.ComandoDesativadoDao import ComandoDesativadoDao


class OnMessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # verifica se a pessoa pode usar o comando, verifica se o comando está ativado e verifica se a pessoa é um bot
        if BlacklistDao().get_pessoa(message.author.id) or message.author.bot: return
        if not (message.guild is None):  # Se foi usado num server, vai ver se o comando está desativado
            if message.content.lower() in ComandoDesativadoDao().get_comandos(message.guild.id): return
        if message.author.id == self.bot.user.id: return
        channel = message.channel
        mensagem_formatada = message.content.lower()
        prefixo = pegar_o_prefixo(None, message)
        lixos = '!@#$%*()-_=+[{]}/?ç´~;.,<>^\\|\'" '
        for char in lixos:
            mensagem_formatada = mensagem_formatada.replace(char, '')
        if message.guild is not None:  # se a mensagem foi enviar num servidor
            for cog in self.bot.cogs:  # verifica se a mensagem, vai ser chamada por algum comando
                for command in self.bot.get_cog(cog).get_commands():
                    if message.content.lower().startswith(f'{prefixo}{command.name}'):  # se achar o comando
                        return  # para
            for comando in ComandoPersonalizadoDao().get_comandos(message.guild.id):
                if comando[0].lower() in message.content.lower():
                    resposta, inText = ComandoPersonalizadoDao().get_resposta(message.guild.id, comando[0])
                    if not inText:
                        if not message.content.lower().startswith(comando[0]):
                            return
                    await channel.send(resposta)
                    return
        if (f'<@{str(self.bot.user.id)}>' == message.content) or (f'<@!{str(self.bot.user.id)}>' == message.content):
            await channel.send(f'Use o comando ``{prefixo}help`` para obter ajuda! xD')


def setup(bot):
    bot.add_cog(OnMessageEvent(bot))
