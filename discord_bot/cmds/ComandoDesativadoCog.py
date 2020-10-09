# coding=utf-8
# Androxus bot
# ComandoDesativadoCog.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.ext import commands

from discord_bot.Classes import Androxus
from discord_bot.database.ComandoDesativado import ComandoDesativado
from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from discord_bot.database.Repositories.ServidorRepository import ServidorRepository
from discord_bot.utils import permissions
from discord_bot.utils.Utils import random_color


class ComandoDesativadoCog(commands.Cog, command_attrs=dict(category='administração')):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='desativar_comando',
                      aliases=['disable_command', 'dc'],
                      description='Desativa algum comando que eu tenho!',
                      parameters=['<comando>'],
                      examples=['``{prefix}desativar_comando`` ``say``'],
                      perm_user='administrador',
                      cls=Androxus.Command)
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
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
            return await ctx.send('Você não pode desativar este comando! <a:no_no:755774680325029889>')
        conexao = Conexao()
        servidor = ServidorRepository().get_servidor(conexao, ctx.guild.id)
        comando_desativado = ComandoDesativado(servidor, comando)
        try:
            ComandoDesativadoRepository().create(conexao, comando_desativado)
            embed = discord.Embed(title=f'Comando desativado com sucesso!', colour=discord.Colour(random_color()),
                                  description=f'Comando desativado: {comando}',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            return await ctx.send(content='<a:off:755774680660574268>', embed=embed)
        except Exception as e:
            raise e
        finally:
            conexao.fechar()

    @commands.command(name='reativar_comando',
                      aliases=['reactivate_command'],
                      description='Reativa algum comando que eu tenho!',
                      parameters=['<comando>'],
                      examples=['``{prefix}reativar_comando`` ``say``'],
                      perm_user='administrador',
                      cls=Androxus.Command)
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    async def _reativar_comando(self, ctx, comando=None):
        if comando is None:
            return await self.bot.send_help(ctx)

        conexao = Conexao()
        servidor = ServidorRepository().get_servidor(conexao, ctx.guild.id)
        comando_desativado = ComandoDesativado(servidor, comando)
        # verificação para saber se o comando existe no banco
        comandos_desativados = ComandoDesativadoRepository().get_commands(conexao, servidor)
        # se não tiver o comando no banco:
        if not comando_desativado in [cmd for cmd in comandos_desativados]:
            conexao.fechar()
            return await ctx.send('<a:atencao:755844029333110815> Este comando já está ativo!')
        try:
            ComandoDesativadoRepository().delete(conexao, comando_desativado)
            embed = discord.Embed(title=f'Comando reativado com sucesso!', colour=discord.Colour(random_color()),
                                  description=f'Comando reativado: {comando}',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            return await ctx.send(content='<a:on:755774680580882562>', embed=embed)
        except Exception as e:
            raise e
        finally:
            conexao.fechar()


def setup(bot):
    bot.add_cog(ComandoDesativadoCog(bot))
