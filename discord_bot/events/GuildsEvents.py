# coding=utf-8
# Androxus bot
# GuildsEvents.py

__author__ = 'Rafael'

from discord.ext import commands
import discord

from discord_bot.dao.ServidorDao import ServidorDao
from discord_bot.utils.Utils import get_emoji_dance, pegar_o_prefixo


class GuildsEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, ctx, guild):
        # toda vez que adicionarem o bot num servidor, vai adicionar o servidor ao banco
        ServidorDao().create(guild.id)
        try:
            for channel in sorted(guild.channels):
                if channel.permissions_for(guild.me).send_messages and isinstance(channel, discord.TextChannel):
                    await channel.send(f'{get_emoji_dance()}\nOlá! Obrigado por me adicionar em seu servidor!\n' +
                                       f'Para saber meus comandos, digite ``{pegar_o_prefixo(None, ctx)}help``!')
                    return
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self, ctx, guild):
        # toda vez que removerem o bot de um servidor, vai remover o servidor do banco
        ServidorDao().delete(guild.id)


def setup(bot):
    bot.add_cog(GuildsEvents(bot))
