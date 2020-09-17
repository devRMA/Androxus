# coding=utf-8
# Androxus bot
# Say.py

__author__ = 'Rafael'

from discord.ext import commands
import discord
from discord.Utils import pegar_o_prefixo, random_color, get_emoji_dance
from datetime import datetime
from discord.dao.ComandoDesativadoDao import ComandoDesativadoDao


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_fale', 'help_falar'])
    async def help_say(self, ctx):
        prefixo = pegar_o_prefixo(None, ctx)
        embed = discord.Embed(title=f"``{prefixo}say``", colour=discord.Colour(random_color()),
                              description="Eu vou repetir o que você falar!",
                              timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
        embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="**Como usar?**",
                        value=f"``{prefixo}say`` ``<frase>``",
                        inline=False)
        embed.add_field(
            name="Tudo que estiver entre **<>** são obrigatorio, e tudo que estiver entre **[]** são opcionais.",
            value=get_emoji_dance(), inline=False)
        embed.add_field(name="Exemplos:",
                        value=f"``{prefixo}say`` ``Olá Mundo!``\n(Eu vou falar \"Olá Mundo!\")",
                        inline=False)
        embed.add_field(name="Outro exemplo:",
                        value=f"``{prefixo}fale`` ``Oi``\n(Eu vou falar \"Oi\")",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}fale``, ``{prefixo}falar``", inline=False)
        embed.add_field(name="<a:atencao:755844029333110815> Requisitos:",
                        value="Caso você não tenha permissão para gerenciar mensagens" +
                              ", eu vou dizer que foi você que mandou eu falar a frase!", inline=False)
        if not (ctx.guild is None):  # se a mensagem foi enviar num server
            for comando_desativado in ComandoDesativadoDao().get_comandos(ctx.guild.id):
                if ('say' in comando_desativado) or ('fale' in comando_desativado) or \
                        ('falar' in comando_desativado):  # verifica se o comando está desativado
                    embed.add_field(name="**O comando foi desativado por algum administrador do server!**",
                                    value="**Se você usar este comando, eu não irei responder!**",
                                    inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['fale', 'falar'], description='Eu vou repetir o que você falar!')
    async def say(self, ctx, *, frase: str):
        try:
            if ctx.guild.me.guild_permissions.manage_messages:
                await ctx.message.delete()
            if not ctx.author.permissions_in(ctx.message.channel).manage_messages:
                frase += f'\n\n- {ctx.author}'
        except:  # se der algum erro, provavelmente é porque o comando foi usado no dm
            pass
        await ctx.send(frase)


def setup(bot):
    bot.add_cog(Say(bot))
