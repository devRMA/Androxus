# coding=utf-8
# Androxus bot
# OnMessageEvent.py

__author__ = 'Rafael'

from discord.ext import commands
from discord.dao.ComandoPersonalizadoDao import ComandoPersonalizadoDao
from discord.Utils import pegar_o_prefixo


class OnMessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        mensagem_formatada = message.content.lower()
        lixos = '!@#$%*()-_=+[{]}/?ç´~;.,<>^\\|\'" '
        for char in lixos:
            mensagem_formatada = mensagem_formatada.replace(char, '')
        if not (message.guild is None):
            for comando in ComandoPersonalizadoDao().get_comandos(message.guild.id):
                if comando[0].lower() in message.content.lower():
                    resposta, inText = ComandoPersonalizadoDao().get_resposta(message.guild.id, comando[0])
                    if not inText:
                        if not message.content.lower().startswith(comando[0]):
                            return
                    await channel.send(resposta)
                    return
        if (f'<@{str(self.bot.user.id)}>' in message.content) or (f'<@!{str(self.bot.user.id)}>' in message.content):
            await channel.send(f'Use o comando ``{pegar_o_prefixo(None, message)}help`` para obter ajuda! xD')


def setup(bot):
    bot.add_cog(OnMessageEvent(bot))
