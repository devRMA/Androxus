# -*- coding: utf-8 -*-
# Androxus bot
# GuildsEvents.py

__author__ = 'Rafael'

from datetime import datetime

import asyncio
import discord
from discord.ext import commands

from database.Models.Servidor import Servidor
from database.Repositories.ServidorRepository import ServidorRepository
from utils.Utils import get_emoji_dance, datetime_format, prettify_number


class GuildsEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # se o bot for adicionado num server antes dele iniciar, vai esperar até o bot iniciar
        while (not self.bot.started) or (self.bot.db_connection is None):
            await asyncio.sleep(0.5)

        e = discord.Embed(title=f'📥 Bot foi adicionado no servidor `{guild.name}`!',
                          colour=discord.Colour.green(),
                          timestamp=datetime.utcnow())
        e.set_footer(text=str(guild.owner), icon_url=guild.owner.avatar_url)
        if guild.banner:
            e.set_image(url=guild.banner_url)
        if guild.icon:
            e.set_thumbnail(url=guild.icon_url)
        e.add_field(name='Quando o servidor foi criado',
                        value=f'`{datetime_format(guild.created_at)}`',
                        inline=True)
        e.add_field(name='Id do servidor',
                        value=f'`{guild.id}`',
                        inline=True)
        e.add_field(name='Quantos membros',
                        value=f'`{prettify_number(len(guild.members))}`',
                        inline=True)
        e.add_field(name='Dono',
                        value=f'`{guild.owner}`(`{guild.owner.id}`)',
                        inline=True)
        e.add_field(name='Agora o bot está em quantos servidores',
                    value=f'`{prettify_number(len(self.bot.guilds))}`',
                    inline=True)
        await self.bot.server_log.send(embed=e)
        servidor = Servidor(guild.id, self.bot.configs['default_prefix'])
        try:
            await ServidorRepository().create(self.bot.db_connection, servidor)
        except Exception as e:
            raise e
        try:
            # source: https://github.com/AlexFlipnote/discord_bot.py/blob/master/cogs/events.py#L52
            to_send = sorted([chan for chan in guild.channels if
                              chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)],
                             key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            try:
                adm = ''
                if guild.me.guild_permissions.view_audit_log:
                    async for entry in guild.audit_logs(limit=5):
                        if str(entry.action).startswith('AuditLogAction.bot_add') and (
                                str(entry.target) == str(self.bot.user)):
                            adm = f' {entry.user.mention}'
                await to_send.send(f'{get_emoji_dance()}\nOlá{adm}! Obrigado por me adicionar em seu servidor!\n' +
                                   f'Para saber todos os meus comandos, digite ``{self.bot.configs["default_prefix"]}cmds``!')
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # se o bot for removido de um server antes dele iniciar, vai esperar até o bot iniciar
        while (not self.bot.started) or (self.bot.db_connection is None):
            await asyncio.sleep(0.5)
        e = discord.Embed(title=f'📤 Bot foi removido do servidor {guild.name}.',
                          colour=discord.Colour.red(),
                          timestamp=datetime.utcnow())
        e.set_footer(text=str(guild.owner), icon_url=guild.owner.avatar_url)
        if guild.banner:
            e.set_image(url=guild.banner_url)
        if guild.icon:
            e.set_thumbnail(url=guild.icon_url)
        e.add_field(name='Quando o servidor foi criado',
                    value=f'``{datetime_format(guild.created_at)}``',
                    inline=True)
        e.add_field(name='Id do servidor',
                    value=f'``{guild.id}``',
                    inline=True)
        e.add_field(name='Quantos membros',
                    value=f'``{prettify_number(len(guild.members))}``',
                    inline=True)
        e.add_field(name='Dono',
                    value=f'``{guild.owner}``(``{guild.owner.id}``)',
                    inline=True)
        e.add_field(name='Agora o bot está em quantos servidores',
                    value=f'`{prettify_number(len(self.bot.guilds))}`',
                    inline=True)
        await self.bot.server_log.send(embed=e)
        servidor = Servidor(guild.id)
        try:
            await ServidorRepository().delete(self.bot.db_connection, servidor)
        except Exception as e:
            raise e


def setup(bot):
    """

    Args:
        bot (Classes.Androxus.Androxus): Instância do bot

    """
    bot.add_cog(GuildsEvents(bot))
