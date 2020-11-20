# -*- coding: utf-8 -*-
# Androxus bot
# ComandoDesativadoCog.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.ext import commands

from Classes import Androxus
from database.Models.ComandoDesativado import ComandoDesativado
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils import permissions
from utils.Utils import random_color


class ComandoDesativadoCog(commands.Cog, command_attrs=dict(category='administração')):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.Androxus.Androxus): Instância do bot

        """
        self.bot = bot

    @Androxus.comando(name='desativar_comando',
                      aliases=['disable_command', 'dc'],
                      description='Desativa algum comando que eu tenho!',
                      parameters=['<comando>'],
                      examples=['``{prefix}desativar_comando`` ``say``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _desativar_comando(self, ctx, *, comando: str = None):
        if comando is None:
            await self.bot.send_help(ctx)
            return
        comandos_que_nao_podem_ser_desativados = ['desativar_comando',
                                                  'disable_command',
                                                  'dc',
                                                  'reativar_comando',
                                                  'reactivate_command',
                                                  'change_prefix',
                                                  'prefixo',
                                                  'prefix'
                                                  'help',
                                                  'ajuda']
        if comando.lower() in comandos_que_nao_podem_ser_desativados:
            return await ctx.send(f'Você não pode desativar este comando! {self.bot.emoji("no_no")}')
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        comando_desativado = ComandoDesativado(servidor, comando)
        await ComandoDesativadoRepository().create(self.bot.db_connection, comando_desativado)
        embed = discord.Embed(title=f'Comando desativado com sucesso!', colour=discord.Colour(random_color()),
                              description=f'Comando desativado: {comando}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        return await ctx.send(content=f'{self.bot.emoji("off")}', embed=embed)

    @Androxus.comando(name='reativar_comando',
                      aliases=['reactivate_command'],
                      description='Reativa algum comando que eu tenho!',
                      parameters=['<comando>'],
                      examples=['``{prefix}reativar_comando`` ``say``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _reativar_comando(self, ctx, comando=None):
        if comando is None:
            return await self.bot.send_help(ctx)

        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        comando_desativado = ComandoDesativado(servidor, comando)
        # verificação para saber se o comando existe no banco
        comandos_desativados = await ComandoDesativadoRepository().get_commands(self.bot.db_connection, servidor)
        # se não tiver o comando no banco:
        if not comando_desativado in [cmd for cmd in comandos_desativados]:
            return await ctx.send(f'{self.bot.emoji("atencao")} Este comando já está ativo!')
        await ComandoDesativadoRepository().delete(self.bot.db_connection, comando_desativado)
        embed = discord.Embed(title=f'Comando reativado com sucesso!', colour=discord.Colour(random_color()),
                              description=f'Comando reativado: {comando}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        return await ctx.send(content=self.bot.emoji('on'), embed=embed)


def setup(bot):
    bot.add_cog(ComandoDesativadoCog(bot))
