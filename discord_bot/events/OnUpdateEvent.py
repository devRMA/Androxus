# coding=utf-8
# Androxus bot
# OnUpdateEvent.py

__author__ = 'Rafael'

from datetime import datetime
from io import BytesIO

import discord
import requests
from PIL import Image, UnidentifiedImageError
from discord.ext import commands

from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.ServidorRepository import ServidorRepository
from discord_bot.utils.Utils import random_color, difference_between_lists


class OnUpdateEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.bot: return
        if not self.bot.is_ready(): return
        conexao = Conexao()
        server = ServidorRepository().get_servidor(conexao, after.guild.id)
        conexao.fechar()
        if server.channel_id_log is not None:
            channel = self.bot.get_channel(server.channel_id_log)
            if channel is not None:
                if before.nick != after.nick:
                    if server.nick_alterado:
                        embed = discord.Embed(title=f'O(A) {after} mudou de nick!\n(id: {after.id})',
                                              colour=discord.Colour(random_color()),
                                              description=f'Nick antigo: {before.nick}\n'
                                                          f'Nick novo: {after.nick}',
                                              timestamp=datetime.utcnow())
                        embed.set_thumbnail(url=str(after.avatar_url))
                        await channel.send(embed=embed)
                if before.roles != after.roles:
                    if server.role_alterado:
                        cargos = [c.id for c in difference_between_lists(before.roles, after.roles)]
                        # se a pessoa ficou com mais cargos, do que ela tinha antes
                        if len(before.roles) < len(after.roles):
                            desc = None
                            if len(cargos) == 1:
                                desc = f'Novo cargo: <@&{cargos[0]}>'
                            elif len(cargos) > 1:
                                desc = 'Novos cargo: ' + ', '.join(cargos)
                        else:  # se foi o contrário
                            desc = None
                            if len(cargos) == 1:
                                desc = f'Cargo removido: <@&{cargos[0]}>'
                            elif len(cargos) > 1:
                                desc = 'Cargo removido: ' + ', '.join(cargos)
                        embed = discord.Embed(title=f'O(A) {after} sofreu alteração nos cargos!\n(id: {after.id})',
                                              colour=discord.Colour(random_color()),
                                              description=desc,
                                              timestamp=datetime.utcnow())
                        embed.set_thumbnail(url=str(after.avatar_url))
                        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if after.bot: return
        if not self.bot.is_ready(): return
        conexao = Conexao()
        servers_with_user = []
        for guild in self.bot.guilds:
            if guild.get_member(after.id) is not None:
                servers_with_user.append(ServidorRepository().get_servidor(conexao, guild.id))
        conexao.fechar()
        if before.name != after.name:
            embed = discord.Embed(title=f'O(A) {after} mudou de nome!\n(id: {after.id})',
                                  colour=discord.Colour(random_color()),
                                  description=f'Nome antigo: {before.name}\n'
                                              f'Nome novo: {after.name}',
                                  timestamp=datetime.utcnow())
            embed.set_thumbnail(url=after.avatar_url)
            for server in servers_with_user:
                if server.channel_id_log is not None:
                    channel = self.bot.get_channel(server.channel_id_log)
                    if (channel is not None) and server.nome_alterado:
                        await channel.send(embed=embed)
        if before.discriminator != after.discriminator:
            embed = discord.Embed(title=f'O(A) {after} mudou a tag!\n(id: {after.id})',
                                  colour=discord.Colour(random_color()),
                                  description=f'Username antigo: {before}\n'
                                              f'Username novo: {after}',
                                  timestamp=datetime.utcnow())
            embed.set_thumbnail(url=after.avatar_url)
            for server in servers_with_user:
                if server.channel_id_log is not None:
                    channel = self.bot.get_channel(server.channel_id_log)
                    if (channel is not None) and server.tag_alterado:
                        await channel.send(embed=embed)
        if before.avatar != after.avatar:
            try:
                url_antigo = before.avatar_url
                url_novo = after.avatar_url

                response_antigo = requests.get(url_antigo)
                response_novo = requests.get(url_novo)

                avatar_antigo = Image.open(BytesIO(response_antigo.content)).resize((512, 512), Image.ANTIALIAS)
                avatar_novo = Image.open(BytesIO(response_novo.content)).resize((512, 512), Image.ANTIALIAS)

                base = Image.new('RGB', (1024, 512), (0, 0, 0))
                base.paste(avatar_antigo, (0, 0))
                base.paste(avatar_novo, (512, 0))
                arr = BytesIO()
                base.save(arr, format='PNG')
                arr.seek(0)
                file = discord.File(arr, filename='avatar.png')
                embed = discord.Embed(title=f'O(A) {after} mudou o avatar!\n(id: {after.id})',
                                      colour=discord.Colour(random_color()),
                                      description='Avatar antigo → avatar novo',
                                      timestamp=datetime.utcnow())
                embed.set_image(url='attachment://avatar.png')
                for server in servers_with_user:
                    if server.channel_id_log is not None:
                        channel = self.bot.get_channel(server.channel_id_log)
                        if (channel is not None) and server.avatar_alterado:
                            await channel.send(file=file, embed=embed)
            except UnidentifiedImageError:
                pass
            except Exception as e:
                raise e


def setup(bot):
    bot.add_cog(OnUpdateEvent(bot))
