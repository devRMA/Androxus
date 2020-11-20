# -*- coding: utf-8 -*-
# Androxus bot
# ComandoPersonalizadoCog.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.ext import commands

from Classes import Androxus
from database.Models.ComandoPersonalizado import ComandoPersonalizado
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils import permissions
from utils.Utils import random_color, get_emoji_dance, convert_to_bool, capitalize, convert_to_string


class ComandoPersonalizadoCog(commands.Cog, command_attrs=dict(category='administração')):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.Androxus.Androxus): Instância do bot

        """
        self.bot = bot

    @Androxus.comando(name='adicionar_comando',
                      aliases=['add_command', 'ac'],
                      description='Adiciona um comando personalizado!',
                      parameters=['"<comando>"', '"<resposta>"',
                                  '[ignorar a posição do comando (sim/nao) (padrão: sim)]'],
                      examples=['``{prefix}adicionar_comando`` ``"bom dia"`` ``"{author_nametag} bom dia!"``\n'
                                '** Para saber mais sobre esse {author_nametag} acesse a [documentação]'
                                '(https://devrma.github.io/Androxus/) **',
                                '``{prefix}ac`` ``"hello world!"`` ``"olá mundo!"`` ``não``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _adicionar_comando(self, ctx, comando='', resposta='', in_text='t'):
        in_text = convert_to_bool(in_text)
        if in_text is None:
            return await ctx.send(
                f'Valor ``{in_text}`` inválido! Os valores que eu aceito são: sim, não, yes, no, 0, 1')
        if ctx.message.content.count('"') < 4:
            return await ctx.send('Parece que você digitou o comando errado!\nVocê deve usar o comando assim:\n' +
                                  f'{ctx.prefix}adicionar_comando **"**comando**"** **"**resposta**"**')
        if (comando.replace(' ', '') == '') or (resposta.replace(' ', '') == ''):
            return await self.bot.send_help(ctx)
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        comando_personalizado = ComandoPersonalizado(servidor,
                                                     comando.lower(),
                                                     resposta,
                                                     in_text)
        await ComandoPersonalizadoRepository().create(self.bot.db_connection, comando_personalizado)
        in_text_str = capitalize(convert_to_string(in_text))
        embed = discord.Embed(title=f'Comando adicionado com sucesso!', colour=discord.Colour(random_color()),
                              description='** **',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        embed.add_field(
            name=f'Comando: {comando.lower()}\nResposta: {resposta}\nIgnorar a posição do comando: {in_text_str}',
            value=f'** **',
            inline=False)
        await ctx.send(content=get_emoji_dance(), embed=embed)

    @Androxus.comando(name='remover_comando',
                      aliases=['remove_command', 'rc'],
                      description='Remove um comando personalizado!',
                      parameters=['"<comando>"'],
                      examples=['``{prefix}remover_comando`` ``"bom dia"``',
                                '``{prefix}rc`` ``"hello world!"``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _remover_comando(self, ctx, *, comando: str = None):
        if comando is None:
            return await self.bot.send_help(ctx)
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        # vai verificar se o comando está no banco
        # aliás, pra remover o comando, ele precisa existir no banco
        comando_personalizado = ComandoPersonalizado(servidor, comando.lower(), '', False)
        if comando_personalizado not in [cmd for cmd in
                                         await ComandoPersonalizadoRepository().get_commands(self.bot.db_connection,
                                                                                             servidor)]:
            return await ctx.send(f'{self.bot.emoji("atencao")} Este comando não existe!')
        await ComandoPersonalizadoRepository().delete(self.bot.db_connection, comando_personalizado)
        embed = discord.Embed(title=f'Comando removido com sucesso!',
                              colour=discord.Colour(random_color()),
                              description=f'Comando: {comando}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        return await ctx.send(content=get_emoji_dance(), embed=embed)

    @Androxus.comando(name='modificar_comando',
                      aliases=['update_command', 'mc'],
                      description='Modifica um comando personalizado',
                      parameters=['<"comando">', '<"resposta">',
                                  '[ignorar a posição do comando (sim/nao)(padrão: sim)]'],
                      examples=['``{prefix}modificar_comando`` ``"bom dia"`` ``"boa noite!"``',
                                '``{prefix}mc`` ``"olá mundo!"`` ``"hello world!"`` ``não``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _modificar_comando(self, ctx, comando='', resposta='', in_text='t'):
        in_text = convert_to_bool(in_text)
        if in_text is None:
            await ctx.send(f'Valor ``{in_text}`` inválido! Os valores que eu aceito são: sim, não, yes, no, 0, 1')
            return
        if ctx.message.content.count('"') != 4:
            return await ctx.send('Parece que você digitou o comando errado!\nVocê deve usar o comando assim:\n' +
                                  f'{ctx.prefix}modificar_comando **"**comando**"** **"**resposta**"**')
        if (comando.replace(' ', '') == '') or (resposta.replace(' ', '') == ''):
            return await self.bot.send_help(ctx)
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        comando_personalizado = ComandoPersonalizado(servidor,
                                                     comando.lower(),
                                                     resposta,
                                                     in_text)
        # vai verificar se o comando está no banco
        # aliás, pra modificar o comando, ele precisa existir no banco
        if comando_personalizado not in [cmd for cmd in
                                         await ComandoPersonalizadoRepository().get_commands(self.bot.db_connection,
                                                                                             servidor)]:
            return await ctx.send(f'{self.bot.emoji("atencao")} Este comando não existe!')
        await ComandoPersonalizadoRepository().update(self.bot.db_connection, comando_personalizado)
        in_text_str = capitalize(convert_to_string(in_text))
        embed = discord.Embed(title=f'Comando modificado com sucesso!', colour=discord.Colour(random_color()),
                              description=f'Comando: {comando}\nResposta: {resposta}\n'
                                          f'Ignorar a posição do comando: {in_text_str}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(content=get_emoji_dance(), embed=embed)


def setup(bot):
    bot.add_cog(ComandoPersonalizadoCog(bot))
