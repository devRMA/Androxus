# coding=utf-8
# Androxus bot
# ComandoPersonalizado.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord.dao.ComandoPersonalizadoDao import ComandoPersonalizadoDao
from discord.Utils import pegar_o_prefixo, random_color
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
        embed.add_field(name="Exemplos:",
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
            if 'adicionar_comando' in ComandoDesativadoDao().get_comandos(ctx.guild.id):  # verifica se o comando está ativo
                embed.add_field(name="**O comando foi desativado por algum administrador do server!**",
                                value="**Se você usar este comando, o bot não ira responder!**",
                                inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['add_command', 'ac'], description='Adiciona comandos personalizados')
    @commands.guild_only()
    async def adicionar_comando(self, ctx, comando=None, resposta=None, inText=False):
        if (comando is None) or (resposta is None):
            await self.help_adicionar_comando(ctx)
            return
        if ComandoPersonalizadoDao().create(ctx.guild.id, comando, resposta, inText):
            await ctx.send(f'Comando adicionado com sucesso!\nComando: ``{comando}``\nResposta: ``{resposta}``')


def setup(bot):
    bot.add_cog(ComandoPersonalizado(bot))
