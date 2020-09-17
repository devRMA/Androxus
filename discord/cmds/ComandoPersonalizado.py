# coding=utf-8
# Androxus bot
# ComandoPersonalizado.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord.dao.ComandoPersonalizadoDao import ComandoPersonalizadoDao
from discord.Utils import random_color, pegar_o_prefixo, get_emoji_dance
from discord.dao.ComandoDesativadoDao import ComandoDesativadoDao


class ComandoPersonalizado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_add_command', 'help_ac'])
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
            value=get_emoji_dance(), inline=False)
        embed.add_field(name="Exemplo:",
                        value=f"``{prefixo}adicionar_comando`` ``\"oi\"`` ``\"oi!\"`` ``True``\n(Se você digitar esse comando, toda vez que alguém digitar \"oi\", o bot vai responder \"oi!\", independete de em qual lugar o \"oi\" estiver)",
                        inline=False)
        embed.add_field(name="Outro exemplo:",
                        value=f"``{prefixo}adicionar_comando`` ``\"bom dia\"`` ``\"Bom dia!!!\"``\nAqui, o bot só vai responder, caso a mensagem inicie com \"bom dia\"",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}add_command``, ``{prefixo}ac``", inline=False)
        embed.add_field(name="<a:atencao:755844029333110815> Requisitos:",
                        value="Você precisa ter permissão de administrador para usar esse comando!", inline=False)
        if not (ctx.guild is None):  # se a mensagem foi enviar num server
            for comando_desativado in ComandoDesativadoDao().get_comandos(ctx.guild.id):
                if ('adicionar_comando' in comando_desativado) or ('add_command' in comando_desativado) or \
                        ('ac' in comando_desativado):  # verifica se o comando está desativado
                    embed.add_field(name="**O comando foi desativado por algum administrador do server!**",
                                    value="**Se você usar este comando, eu não irei responder!**",
                                    inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    #@commands.has_permissions(administrator=True)
    @commands.command(aliases=['add_command', 'ac'], description='Adiciona comandos personalizados')
    @commands.guild_only()
    async def adicionar_comando(self, ctx, comando=None, resposta=None, inText='t'):
        inText = inText.lower()
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
                                  description=get_emoji_dance(),
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            embed.add_field(name=f"Informações",
                            value=f"Comando: {comando}\nResposta: {resposta}\nIgnorar a posição do comando: {inText}",
                            inline=False)
            await ctx.send(embed=embed)

    @commands.command(hidden=True, aliases=['help_remove_command', 'help_rc'])
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
            value=get_emoji_dance(), inline=False)
        embed.add_field(name="Exemplos:",
                        value=f"``{prefixo}remover_comando`` ``\"teste\"``\n(Vai tirar o comando personalizado \"teste\")",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}remove_command``, ``{prefixo}rc``", inline=False)
        embed.add_field(name="<a:atencao:755844029333110815> Requisitos:",
                        value="Você precisa ter permissão de administrador para usar esse comando!", inline=False)
        if not (ctx.guild is None):  # se a mensagem foi enviar num server
            for comando_desativado in ComandoDesativadoDao().get_comandos(ctx.guild.id):
                if ('remover_comando' in comando_desativado) or ('remove_command' in comando_desativado) or \
                        ('rc' in comando_desativado):  # verifica se o comando está desativado
                    embed.add_field(name="**O comando foi desativado por algum administrador do server!**",
                                    value="**Se você usar este comando, eu não irei responder!**",
                                    inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    #@commands.has_permissions(administrator=True)
    @commands.command(aliases=['remove_command', 'rc'], description='Remove um comando personalizado')
    @commands.guild_only()
    async def remover_comando(self, ctx, comando=None):
        if comando is None:
            await self.help_remover_comando(ctx)
            return
        if ComandoPersonalizadoDao().delete(ctx.guild.id, comando):
            embed = discord.Embed(title=f'Comando removido com sucesso!', colour=discord.Colour(random_color()),
                                  description=get_emoji_dance(),
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=embed)

    @commands.command(hidden=True, aliases=['help_update_command', 'help_mc'])
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
            value=get_emoji_dance(), inline=False)
        embed.add_field(name="Exemplos:",
                        value=f"``{prefixo}modificar_comando`` ``\"oi\"`` ``\"oi!\"`` ``True``\n(Modifica o comando que já existe)",
                        inline=False)
        embed.add_field(name="Outro exemplo:",
                        value=f"``{prefixo}modificar_comando`` ``\"bom dia\"`` ``\"Bom dia!!!\"``\n(Modifica o comando que já existe)",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}update_command``, ``{prefixo}mc``", inline=False)
        embed.add_field(name="<a:atencao:755844029333110815> Requisitos:",
                        value="Você precisa ter permissão de administrador para usar esse comando!", inline=False)
        if not (ctx.guild is None):  # se a mensagem foi enviar num server
            for comando_desativado in ComandoDesativadoDao().get_comandos(ctx.guild.id):
                if ('modificar_comando' in comando_desativado) or ('update_command' in comando_desativado) or \
                        ('mc' in comando_desativado):  # verifica se o comando está desativado
                    embed.add_field(name="**O comando foi desativado por algum administrador do server!**",
                                    value="**Se você usar este comando, eu não irei responder!**",
                                    inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    #@commands.has_permissions(administrator=True)
    @commands.command(aliases=['update_command', 'mc'], description='Modifica um comando personalizado')
    @commands.guild_only()
    async def modificar_comando(self, ctx, comando=None, resposta=None, inText='t'):
        inText = inText.lower()
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
                                  description=f"{get_emoji_dance()}\nComando: {comando}\nResposta: {resposta}\n" +
                                              f"Ignorar a posição do comando: {inText}",
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ComandoPersonalizado(bot))
