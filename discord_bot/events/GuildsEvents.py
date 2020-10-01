# coding=utf-8
# Androxus bot
# GuildsEvents.py

__author__ = 'Rafael'

import discord
from discord.ext import commands

from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.ServidorRepository import ServidorRepository
from discord_bot.database.Servidor import Servidor
from discord_bot.utils.Utils import get_emoji_dance


class GuildsEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, ctx):
        # toda vez que adicionarem o bot num servidor, vai adicionar o servidor ao banco
        servidor = Servidor(ctx.id)
        conexao = Conexao()
        try:
            ServidorRepository.create(conexao, servidor)
        except Exception as e:
            raise e
        finally:
            conexao.fechar()
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
                    if str(entry.action).startswith('AuditLogAction.bot_add') and (
                            str(entry.target) == str(self.bot.user)):
                        adm = f' {entry.user.mention}'
            await to_send.send(f'{get_emoji_dance()}\nOlá{adm}! Obrigado por me adicionar em seu servidor!\n' +
                               'Para saber meus comandos, digite ``--help``!')

    @commands.Cog.listener()
    async def on_guild_remove(self, ctx):
        # toda vez que removerem o bot de um servidor, vai remover o servidor do banco
        servidor = Servidor(ctx.id)
        conexao = Conexao()
        try:
            ServidorRepository.delete(conexao, servidor)
        except Exception as e:
            raise e
        finally:
            conexao.fechar()


def setup(bot):
    bot.add_cog(GuildsEvents(bot))
