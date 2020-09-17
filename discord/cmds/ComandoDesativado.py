# coding=utf-8
# Androxus bot
# ComandoDesativado.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord.dao.ComandoDesativadoDao import ComandoDesativadoDao
from discord.modelos.EmbedHelp import embedHelp


class ComandoDesativado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_disable_command', 'help_dc'])
    async def help_desativar_comando(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando='desativar_comando',
                          descricao=self.desativar_comando.description,
                          parametros=['<"comando">'],
                          exemplos=['``{pref}desativar_comando`` ``"say"``'],
                          aliases=self.desativar_comando.aliases.copy(),  # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          perm_pessoa='administrador')
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['disable_command', 'dc'], description='Desativa comandos!')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def desativar_comando(self, ctx, comando=None):
        #if not ctx.author.permissions_in(ctx.message.channel).administrator:  # se o usuário não tiver permissão de adm
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
        if ComandoDesativadoDao().create(ctx.guild.id, comando):
            embed = discord.Embed(title=f'Comando desativado com sucesso!', colour=discord.Colour(random_color()),
                                  description='<a:off:755774680660574268>',
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            embed.add_field(name=f"Comando desativado: {comando}",
                            value="\uFEFF",
                            inline=False)
            await ctx.send(embed=embed)

    @commands.command(hidden=True, aliases=['help_reactivate_command'])
    async def help_reativar_comando(self, ctx):
        prefixo = pegar_o_prefixo(None, ctx)
        embed = discord.Embed(title=f"``{prefixo}reativar_comando``", colour=discord.Colour(random_color()),
                              description="Desativa um comando!",
                              timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
        embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="**Como usar?**",
                        value=f"``{prefixo}reativar_comando`` ``\"<comando>\"``",
                        inline=False)
        embed.add_field(
            name="Tudo que estiver entre **<>** são obrigatorio, e tudo que estiver entre **[]** são opcionais.",
            value=get_emoji_dance(), inline=False)
        embed.add_field(name="Exemplo:",
                        value=f"``{prefixo}reativar_comando`` ``\"say\"``\n(Esse comando reativa o comando \"say\" no seu servidor!)",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}reactivate_command``", inline=False)
        embed.add_field(name="<a:atencao:755844029333110815> Requisitos:",
                        value="Você precisa ter permissão de administrador para usar esse comando!", inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    #@commands.has_permissions(administrator=True)
    @commands.command(aliases=['reactivate_command'], description='Reativa comando!')
    @commands.guild_only()
    async def reativar_comando(self, ctx, comando=None):
        if (comando is None):
            await self.help_desativar_comando(ctx)
            return
        if ComandoDesativadoDao().delete(ctx.guild.id, comando):
            embed = discord.Embed(title=f'Comando reativado com sucesso!', colour=discord.Colour(random_color()),
                                  description='<a:on:755774680580882562>',
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.add_field(name=f"Comando reativado: {comando}",
                            value="\uFEFF",
                            inline=False)
            embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ComandoDesativado(bot))
