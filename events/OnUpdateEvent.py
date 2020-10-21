# coding=utf-8
# Androxus bot
# OnUpdateEvent.py

__author__ = 'Rafael'

from datetime import datetime
from io import BytesIO

import aiohttp
import discord
from PIL import Image
from discord.ext import commands

from database.Conexao import Conexao
from database.Repositories.ServidorRepository import ServidorRepository
from utils.Utils import random_color, difference_between_lists


class OnUpdateEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.bot: return
        if not self.bot.is_ready(): return
        if self.bot.maintenance_mode: return
        conexao = Conexao()
        server = ServidorRepository().get_servidor(conexao, after.guild.id)
        conexao.fechar()
        if server is None:
            return
        if server.channel_id_log is not None:
            channel = self.bot.get_channel(server.channel_id_log)
            if channel is not None:
                if before.nick != after.nick:
                    if server.nick_alterado:
                        embed = discord.Embed(title='Nick alterado',
                                              colour=discord.Colour(random_color()),
                                              description=f'O(A) {after.name} mudou de nick!\n'
                                                          f'User: {after.mention}\n'
                                                          f'Id: {after.id}\n'
                                                          f'Nick antigo: {before.nick}\n'
                                                          f'Nick novo: {after.nick}',
                                              timestamp=datetime.utcnow())
                        embed.set_thumbnail(url=str(after.avatar_url))
                        await channel.send(embed=embed)
                if before.roles != after.roles:
                    if server.role_alterado:
                        cargos = [f'<@&{c.id}>' for c in difference_between_lists(before.roles, after.roles)]
                        # se a pessoa ficou com mais cargos, do que ela tinha antes
                        if len(before.roles) < len(after.roles):
                            desc = None
                            if len(cargos) == 1:
                                desc = f'Novo cargo: {cargos[0]}'
                            elif len(cargos) > 1:
                                desc = 'Novos cargo: ' + ', '.join(cargos)
                        else:  # se foi o contrário
                            desc = None
                            if len(cargos) == 1:
                                desc = f'Cargo removido: {cargos[0]}'
                            elif len(cargos) > 1:
                                desc = 'Cargos removidos: ' + ', '.join(cargos)
                        embed = discord.Embed(title='Cargos alterados',
                                              colour=discord.Colour(random_color()),
                                              description=f'O(A) {after.name} sofreu alteração nos cargos!\n'
                                                          f'User: {after.mention}\n'
                                                          f'Id: {after.id}\n'
                                                          f'{desc}',
                                              timestamp=datetime.utcnow())
                        embed.set_thumbnail(url=str(after.avatar_url))
                        await channel.send(embed=embed)
                if (before.premium_since is None) and (after.premium_since is not None):
                    if server.role_alterado:
                        # pessoa começou a dar boost
                        embed = discord.Embed(title='Novo booster',
                                              colour=discord.Colour(0xffdcf4),
                                              description=f'O(A) {after.name} começou a dar boost!\n'
                                                          f'User: {after.mention}\n'
                                                          f'Id: {after.id}\n',
                                              timestamp=datetime.utcnow())
                        embed.set_thumbnail(url=str(after.avatar_url))
                        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if after.bot: return
        if not self.bot.is_ready(): return
        if self.bot.maintenance_mode: return
        conexao = Conexao()
        servers_with_user = []
        for guild in self.bot.guilds:
            if guild.get_member(after.id) is not None:
                servers_with_user.append(ServidorRepository().get_servidor(conexao, guild.id))
        conexao.fechar()
        if len(servers_with_user) == 0:
            return
        if before.name != after.name:
            embed = discord.Embed(title='Nome alterado',
                                  colour=discord.Colour(random_color()),
                                  description=f'O(A) {after.name} mudou de nome!\n'
                                              f'User: {after.mention}\n'
                                              f'Id: {after.id}\n'
                                              f'Nome antigo: {before.name}\n'
                                              f'Nome novo: {after.name}',
                                  timestamp=datetime.utcnow())
            embed.set_thumbnail(url=after.avatar_url)
            for server in servers_with_user:
                if server.channel_id_log is not None:
                    channel = self.bot.get_channel(server.channel_id_log)
                    if (channel is not None) and server.nome_alterado:
                        await channel.send(embed=embed)
        if before.discriminator != after.discriminator:
            embed = discord.Embed(title='Tag alterada',
                                  colour=discord.Colour(random_color()),
                                  description=f'O(A) {after.name} mudou a tag!\n'
                                              f'User: {after.mention}\n'
                                              f'Id: {after.id}\n'
                                              f'Tag antiga: {before.discriminator}\n'
                                              f'Tag nova: {after.discriminator}',
                                  timestamp=datetime.utcnow())
            embed.set_thumbnail(url=after.avatar_url)
            for server in servers_with_user:
                if server.channel_id_log is not None:
                    channel = self.bot.get_channel(server.channel_id_log)
                    if (channel is not None) and server.tag_alterado:
                        await channel.send(embed=embed)
        if before.avatar_url != after.avatar_url:
            url_antigo = str(before.avatar_url_as(format='webp'))
            if url_antigo.find('?size=') != -1:
                url_antigo = url_antigo[:url_antigo.rfind('?size=')]
            url_novo = str(after.avatar_url_as(format='webp'))
            async with aiohttp.ClientSession() as session:
                async with session.get(url_antigo) as resp:
                    if resp.status == 200:
                        response_antigo = BytesIO(await resp.read())
                    else:
                        return
                async with session.get(url_novo) as resp:
                    if resp.status == 200:
                        response_novo = BytesIO(await resp.read())
                    else:
                        return
                avatar_antigo = Image.open(response_antigo).resize((512, 512), Image.ANTIALIAS)
                avatar_novo = Image.open(response_novo).resize((512, 512), Image.ANTIALIAS)
                base = Image.new('RGBA', (1024, 512), (0, 0, 0, 0))
                base.paste(avatar_antigo, (0, 0))
                base.paste(avatar_novo, (512, 0))
                arr = BytesIO()
                base.save(arr, format='PNG')
                arr.seek(0)
                file = discord.File(arr, filename='avatar.png')
                embed = discord.Embed(title='Avatar alterado',
                                      colour=discord.Colour(random_color()),
                                      description=f'O(A) {after.name} mudou o avatar!\n'
                                                  f'User: {after.mention}\n'
                                                  f'Id: {after.id}\n'
                                                  f'[Avatar antigo]({before.avatar_url})'
                                                  f' → [avatar novo]({after.avatar_url})',
                                      timestamp=datetime.utcnow())
                embed.set_image(url='attachment://avatar.png')
                for server in servers_with_user:
                    if server.channel_id_log is not None:
                        channel = self.bot.get_channel(server.channel_id_log)
                        if (channel is not None) and server.avatar_alterado:
                            await channel.send(file=file, embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot: return
        if not self.bot.is_ready(): return
        if self.bot.maintenance_mode: return
        if before.content == after.content: return
        if after.is_system(): return
        if (after.guild is None) or (before.guild is None): return
        conexao = Conexao()
        server = ServidorRepository().get_servidor(conexao, after.guild.id)
        conexao.fechar()
        if server.channel_id_log is not None:
            channel = self.bot.get_channel(server.channel_id_log)
            if channel is not None:
                if server.mensagem_editada:
                    msg_antiga = discord.utils.escape_markdown(before.content)
                    msg_nova = discord.utils.escape_markdown(after.content)
                    embed = discord.Embed(title='Mensagem editada',
                                          colour=discord.Colour(random_color()),
                                          description=f'Autor: {after.author.name}\n'
                                                      f'Menção: {after.author.mention}\n'
                                                      f'Id: {after.author.id}\n'
                                                      f'Chat: <#{after.channel.id}>\n'
                                                      f'Mensagem antiga:```{msg_antiga}```'
                                                      f'[Mensagem nova]({after.jump_url}):'
                                                      f'```{msg_nova}```',
                                          timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=after.author.avatar_url)
                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot: return
        if not self.bot.is_ready(): return
        if self.bot.maintenance_mode: return
        if message.is_system(): return
        if message.guild is None: return
        conexao = Conexao()
        server = ServidorRepository().get_servidor(conexao, message.guild.id)
        conexao.fechar()
        if server.channel_id_log is not None:
            channel = self.bot.get_channel(server.channel_id_log)
            if channel is not None:
                if server.mensagem_deletada:
                    msg_escaped = discord.utils.escape_markdown(message.content)
                    embed = discord.Embed(
                        title=f'Mensagem deletada',
                        colour=discord.Colour(random_color()),
                        description=f'Autor: {message.author.name}\n'
                                    f'Menção: {message.author.mention}\n'
                                    f'Id: {message.author.id}\n'
                                    f'Chat: <#{message.channel.id}>\n'
                                    f'Mensagem deletada:```{msg_escaped}```',
                        timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=message.author.avatar_url)
                    await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(OnUpdateEvent(bot))
