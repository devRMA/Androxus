# coding=utf-8
# Androxus bot
# OnMessageEvent.py

__author__ = 'Rafael'

from discord.ext import commands
from discord.dao.BlacklistDao import BlacklistDao
from discord.main import pegar_o_prefixo


class OnMessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if BlacklistDao().get_pessoa(message.author.id) or message.author.bot: return
        channel = message.channel
        mensagem_formatada = message.content
        lixos = '!@#$%*()-_=+[{]}/?ç´~;., <>^\\|\'"'
        for char in lixos:
            mensagem_formatada = mensagem_formatada.replace(char, '')
        if (f'<@{str(self.bot.user.id)}>' in message.content) or (f'<@!{str(self.bot.user.id)}>' in message.content):
            await channel.send(f'Use o comando ``{pegar_o_prefixo(None, message)}help`` para obter ajuda! xD')

        await self.bot.process_commands(message)  # caso não tenha passado por nenhuma mensagem a cima, vai para os comandos


def setup(bot):
    bot.add_cog(OnMessageEvent(bot))
