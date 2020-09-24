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
    async def on_guild_join(self, ctx):
        # toda vez que adicionarem o bot num servidor, vai adicionar o servidor ao banco
        ServidorDao().create(ctx.id)
        try:
            to_send = sorted([chan for chan in ctx.channels if
                              chan.permissions_for(ctx.me).send_messages and isinstance(chan, discord.TextChannel)],
                             key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            adm = ''
            if ctx.me.guild_permissions.view_audit_log:
                async for entry in ctx.audit_logs(limit=2):
                    if str(entry.action).startswith('AuditLogAction.bot_add') and (str(entry.target) == str(self.bot.user)):
                        adm = f' {entry.user.mention}'
            await to_send.send(f'{get_emoji_dance()}\nOlá{adm}! Obrigado por me adicionar em seu servidor!\n' +
                               'Para saber meus comandos, digite ``--help``!')

    @commands.Cog.listener()
    async def on_guild_remove(self, ctx):
        # toda vez que removerem o bot de um servidor, vai remover o servidor do banco
        ServidorDao().delete(ctx.id)


def setup(bot):
    bot.add_cog(GuildsEvents(bot))
