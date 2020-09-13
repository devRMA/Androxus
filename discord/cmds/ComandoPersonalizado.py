# coding=utf-8
# Androxus bot
# ComandoPersonalizado.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord.dao.ComandoPersonalizadoDao import ComandoPersonalizadoDao
from discord.Utils import random_color, pegar_o_prefixo
from discord.dao.ComandoDesativadoDao import ComandoDesativadoDao


class ComandoPersonalizado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def help_adicionar_comando(self, ctx):
        prefixo = pegar_o_prefixo(None, ctx)
        embed = discord.Embed(title=f"``{prefixo}adicionar_comando``", colour=discord.Colour(random_color()),
                              description="Adiciona comandos personalizados!",
                              timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
        embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="**Como usar?**",
                        value=f"``{prefixo}adicionar_comando`` ``\"<comando>\"`` ``\"<resposta>\"`` ``[ignorar_posição]``",
                        inline=False)
        embed.add_field(
            name="Tudo que estiver entre **<>** são obrigatorio, e tudo que estiver entre **[]** são opcionais.",
            value="<a:jotarodance:754702437901664338>", inline=False)
        embed.add_field(name="Exemplo:",
                        value=f"``{prefixo}adicionar_comando`` ``\"oi\"`` ``\"oi!\"`` ``True``\n(Se você digitar esse comando, toda vez que alguém digitar \"oi\", o bot vai responder \"oi!\", independete de em qual lugar o \"oi\" estiver)",
                        inline=False)
        embed.add_field(name="Outro exemplo:",
                        value=f"``{prefixo}adicionar_comando`` ``\"bom dia\"`` ``\"Bom dia!!!\"``\nAqui, o bot só vai responder, caso a mensagem inicie com \"bom dia\"",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}add_command``, ``{prefixo}ac``", inline=False)
        embed.add_field(name=":exclamation:Requisitos:",
                        value="Você precisa ter permissão de administrador para usar esse comando!", inline=False)
        if not (ctx.guild is None):  # se a mensagem foi enviar num server
            if 'adicionar_comando' in ComandoDesativadoDao().get_comandos(
                    ctx.guild.id):  # verifica se o comando está ativo
                embed.add_field(name="**O comando foi desativado por algum administrador do server!**",
                                value="**Se você usar este comando, o bot não ira responder!**",
                                inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['add_command', 'ac'], description='Adiciona comandos personalizados')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def adicionar_comando(self, ctx, comando=None, resposta=None, inText='t'):
        if inText != None:
            if inText in ['t', 'true', 's', 'sim', '1', 'y', 'yes']:
                inText = True
            elif inText in ['f', 'false', 'n', 'não', 'nao', '0', 'n', 'no']:
                inText = False
            else:
                await ctx.send(f'Valor ``{inText}`` inválido! Os valores que eu aceito são: sim, não, yes, no, 0, 1')
                return
        if (comando is None) or (resposta is None):
            await self.help_adicionar_comando(ctx)
            return
        if ComandoPersonalizadoDao().create(ctx.guild.id, comando, resposta, inText):
            embed = discord.Embed(title=f'Comando adicionado com sucesso!', colour=discord.Colour(random_color()),
                                  description="<a:aeeee:754779905782448258>",
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            embed.add_field(name=f"Informações",
                            value=f"Comando: {comando}\nResposta: {resposta}\nIgnorar a posição do comando: {inText}",
                            inline=False)
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def help_remover_comando(self, ctx):
        prefixo = pegar_o_prefixo(None, ctx)
        embed = discord.Embed(title=f"``{prefixo}remover_comando``", colour=discord.Colour(random_color()),
                              description="Remove um comando personalizado!",
                              timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
        embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="**Como usar?**",
                        value=f"``{prefixo}remover_comando`` ``\"<comando>\"``",
                        inline=False)
        embed.add_field(
            name="Tudo que estiver entre **<>** são obrigatorio, e tudo que estiver entre **[]** são opcionais.",
            value="<a:jotarodance:754702437901664338>", inline=False)
        embed.add_field(name="Exemplos:",
                        value=f"``{prefixo}remover_comando`` ``\"teste\"``\n(Vai tirar o comando personalizado \"teste\")",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}remove_command``, ``{prefixo}rc``", inline=False)
        embed.add_field(name=":exclamation:Requisitos:",
                        value="Você precisa ter permissão de administrador para usar esse comando!", inline=False)
        if not (ctx.guild is None):  # se a mensagem foi enviar num server
            if 'adicionar_comando' in ComandoDesativadoDao().get_comandos(
                    ctx.guild.id):  # verifica se o comando está ativo
                embed.add_field(name="**O comando foi desativado por algum administrador do server!**",
                                value="**Se você usar este comando, o bot não ira responder!**",
                                inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['remove_command', 'rc'], description='Remove um comando personalizado')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def remover_comando(self, ctx, comando=None):
        if comando is None:
            await self.help_remover_comando(ctx)
            return
        if ComandoPersonalizadoDao().delete(ctx.guild.id, comando):
            embed = discord.Embed(title=f'Comando removido com sucesso!', colour=discord.Colour(random_color()),
                                  description="<a:aeeee:754779905782448258>",
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=embed)

    @commands.command(hidden=True,)
    async def help_modificar_comando(self, ctx):
        prefixo = pegar_o_prefixo(None, ctx)
        embed = discord.Embed(title=f"``{prefixo}modificar_comando``", colour=discord.Colour(random_color()),
                              description="Modifica um comando personalizado!",
                              timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
        embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="**Como usar?**",
                        value=f"``{prefixo}modificar_comando`` ``\"<comando>\"`` ``\"<resposta>\"`` ``[ignorar_posição]``",
                        inline=False)
        embed.add_field(
            name="Tudo que estiver entre **<>** são obrigatorio, e tudo que estiver entre **[]** são opcionais.",
            value="<a:jotarodance:754702437901664338>", inline=False)
        embed.add_field(name="Exemplos:",
                        value=f"``{prefixo}modificar_comando`` ``\"oi\"`` ``\"oi!\"`` ``True``\n(Modifica o comando que já existe)",
                        inline=False)
        embed.add_field(name="Outro exemplo:",
                        value=f"``{prefixo}modificar_comando`` ``\"bom dia\"`` ``\"Bom dia!!!\"``\n(Modifica o comando que já existe)",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}update_command``, ``{prefixo}mc``", inline=False)
        embed.add_field(name=":exclamation:Requisitos:",
                        value="Você precisa ter permissão de administrador para usar esse comando!", inline=False)
        if not (ctx.guild is None):  # se a mensagem foi enviar num server
            if 'adicionar_comando' in ComandoDesativadoDao().get_comandos(
                    ctx.guild.id):  # verifica se o comando está ativo
                embed.add_field(name="**O comando foi desativado por algum administrador do server!**",
                                value="**Se você usar este comando, o bot não ira responder!**",
                                inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['update_command', 'mc'], description='Modifica um comando personalizado')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def modificar_comando(self, ctx, comando=None, resposta=None, inText='t'):
        if inText != None:
            if inText in ['t', 'true', 's', 'sim', '1', 'y', 'yes']:
                inText = True
            elif inText in ['f', 'false', 'n', 'não', 'nao', '0', 'n', 'no']:
                inText = False
            else:
                await ctx.send(f'Valor ``{inText}`` inválido! Os valores que eu aceito são: sim, não, yes, no, 0, 1')
                return
        if (comando is None) or (resposta is None):
            await self.help_modificar_comando(ctx)
            return
        if ComandoPersonalizadoDao().update(ctx.guild.id, comando, resposta, inText):
            embed = discord.Embed(title=f'Comando modificado com sucesso!', colour=discord.Colour(random_color()),
                                  description=f"<a:aeeee:754779905782448258>\nComando: {comando}\nResposta: {resposta}\nIgnorar a posição do comando: {inText}",
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ComandoPersonalizado(bot))
