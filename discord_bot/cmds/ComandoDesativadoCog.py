# coding=utf-8
# Androxus bot
# ComandoDesativadoCog.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.ext import commands

from discord_bot.database.ComandoDesativado import ComandoDesativado
from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from discord_bot.database.Servidor import Servidor
from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.utils import permissions
from discord_bot.utils.Utils import random_color


class ComandoDesativadoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_disable_command', 'help_dc'])
    async def help_desativar_comando(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.desativar_comando.name,
                          descricao=self.desativar_comando.description,
                          parametros=['<"comando">'],
                          exemplos=['``{pref}desativar_comando`` ``"say"``'],
                          aliases=self.desativar_comando.aliases.copy(),
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          perm_pessoa='administrador')
        await ctx.send(embed=embed)

    @commands.command(aliases=['disable_command', 'dc'], description='Desativa comandos!')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    async def desativar_comando(self, ctx, comando=None):
        if comando is None:
            await self.help_desativar_comando(ctx)
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
            await ctx.send('Você não pode desativar este comando! <a:no_no:755774680325029889>')
            return
        conexao = Conexao()
        servidor = Servidor(ctx.guild.id, ctx.prefix)
        comandoDesativado = ComandoDesativado(servidor, comando)
        foi = False
        try:
            foi = ComandoDesativadoRepository().create(conexao, comandoDesativado)
        except Exception as e:
            raise e
        finally:
            conexao.fechar()
        if foi:
            embed = discord.Embed(title=f'Comando desativado com sucesso!', colour=discord.Colour(random_color()),
                                  description=f'Comando desativado: {comando}',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            await ctx.send(content='<a:off:755774680660574268>', embed=embed)

    @commands.command(hidden=True, aliases=['help_reactivate_command'])
    async def help_reativar_comando(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.reativar_comando.name,
                          descricao=self.reativar_comando.description,
                          parametros=['<"comando">'],
                          exemplos=['``{pref}reativar_comando`` ``"say"``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.reativar_comando.aliases.copy(),
                          perm_pessoa='administrador')
        await ctx.send(embed=embed)

    @commands.command(aliases=['reactivate_command'], description='Reativa comando!')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    async def reativar_comando(self, ctx, comando=None):
        if comando is None:
            await self.help_desativar_comando(ctx)
            return
        conexao = Conexao()
        servidor = Servidor(ctx.guild.id, ctx.prefix)
        comandoDesativado = ComandoDesativado(servidor, comando)
        foi = False
        try:
            foi = ComandoDesativadoRepository().delete(conexao, comandoDesativado)
        except Exception as e:
            raise e
        finally:
            conexao.fechar()
        if foi:
            embed = discord.Embed(title=f'Comando reativado com sucesso!', colour=discord.Colour(random_color()),
                                  description=f'Comando reativado: {comando}',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            await ctx.send(content='<a:on:755774680580882562>', embed=embed)


def setup(bot):
    bot.add_cog(ComandoDesativadoCog(bot))
