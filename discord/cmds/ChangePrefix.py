# coding=utf-8
# Androxus bot
# ChangePrefix.py

__author__ = 'Rafael'

from discord.ext import commands
import discord
from discord.dao.ServidorDao import ServidorDao
from discord.Utils import pegar_o_prefixo, random_color
from datetime import datetime


class ChangePrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_prefixo', 'help_prefix'])
    async def help_change_prefix(self, ctx):
        prefixo = pegar_o_prefixo(None, ctx)
        embed = discord.Embed(title=f"``{prefixo}change_prefix``", colour=discord.Colour(random_color()),
                              description="Muda o meu prefixo!",
                              timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
        embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="**Como usar?**",
                        value=f"``{prefixo}change_prefix`` ``<prefixo>``",
                        inline=False)
        embed.add_field(
            name="Tudo que estiver entre **<>** são obrigatorio, e tudo que estiver entre **[]** são opcionais.",
            value="<a:jotarodance:754702437901664338>", inline=False)
        embed.add_field(name="Exemplo:",
                        value=f"``{prefixo}change_prefix`` ``!!``\n(Muda o prefixo para \"!!\")",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}prefixo``, ``{prefixo}prefix``", inline=False)
        embed.add_field(name=":exclamation:Requisitos:",
                        value="Você precisa ter permissão de administrador para usar esse comando!", inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    # @commands.has_permissions(administrator=True)
    @commands.command(aliases=['prefixo', 'prefix'], description='Comando que é usado para mudar o meu prefixo')
    @commands.guild_only()
    async def change_prefix(self, ctx, prefixo_novo='--'):
        ServidorDao().update(ctx.guild.id, prefixo_novo)
        if prefixo_novo != '--':
            await ctx.send(
                f'Agora o meu  prefixo é ``{prefixo_novo}``\nCaso queria voltar para o prefixo padrão, basta digitar ``{prefixo_novo}prefixo``')
        else:
            await ctx.send(f'Agora estou com o prefixo padrão!')


def setup(bot):
    bot.add_cog(ChangePrefix(bot))
