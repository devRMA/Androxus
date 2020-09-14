# coding=utf-8
# Androxus bot
# GetEmoji.py

__author__ = 'Rafael'

from discord.ext import commands
import discord
from discord.dao.ServidorDao import ServidorDao
from discord.Utils import pegar_o_prefixo, random_color
from datetime import datetime


class GetEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_emoji'])
    async def help_get_emoji(self, ctx):
        prefixo = pegar_o_prefixo(None, ctx)
        embed = discord.Embed(title=f"``{prefixo}emoji``", colour=discord.Colour(random_color()),
                              description="Pega o link de um emoji!",
                              timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
        embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="**Como usar?**",
                        value=f"``{prefixo}emoji`` ``<emoji>``",
                        inline=False)
        embed.add_field(
            name="Tudo que estiver entre **<>** são obrigatorio, e tudo que estiver entre **[]** são opcionais.",
            value="<a:jotarodance:754702437901664338>", inline=False)
        embed.add_field(name="Exemplo:",
                        value=f"``{prefixo}emoji`` ``<a:hello:754111280184295456>``\n(Eu vou enviar o link do emoji)",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}get_emoji``", inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['emoji'], description='Pega o link de um emoji.')
    async def get_emoji(self, ctx, emoji = None):
        if (emoji is None):
            await self.help_get_emoji(ctx)
            return
        if not isinstance(emoji, discord.Emoji):
            await ctx.send(f'Não consegui encontrar o emoji {emoji} ;-;')
            return
        ctx.send(emoji.url)

def setup(bot):
    bot.add_cog(GetEmoji(bot))
