# coding=utf-8
# Androxus bot
# Invite.py

__author__ = 'Rafael'

from discord.ext import commands
import discord
from discord.Utils import pegar_o_prefixo, random_color
from datetime import datetime

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def help_invite(self, ctx):
        prefixo = pegar_o_prefixo(None, ctx)
        embed = discord.Embed(title=f"``{prefixo}invite``", colour=discord.Colour(random_color()),
                              description="Mostra o link que você usa para me adicionar em servidores!",
                              timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
        embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="**Como usar?**",
                        value=f"``{prefixo}invite``",
                        inline=False)
        embed.add_field(name="Exemplo:",
                        value=f"``{prefixo}invite``",
                        inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(description='Mostra o link que você usa para me adicionar em servidores')
    async def invite(self, ctx):
        await ctx.send(f'https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8')


def setup(bot):
    bot.add_cog(Invite(bot))
