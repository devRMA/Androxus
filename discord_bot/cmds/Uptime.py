# coding=utf-8
# Androxus bot
# Uptime.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.utils.Utils import random_color, datetime_format


class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_tempo_on'])
    async def help_uptime(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.uptime.name,
                          descricao=self.uptime.description,
                          exemplos=['``{pref}uptime``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.uptime.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['tempo_on'], description='Mostra a quanto tempo eu estou online!')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def uptime(self, ctx):
        embed = discord.Embed(title=f':timer: Quando eu liguei:',
                              description=f'``{datetime_format(self.bot.uptime)}``',
                              colour=discord.Colour(random_color()),
                              timestamp=datetime.utcnow())
        embed.set_author(name='Androxus', icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Uptime(bot))
