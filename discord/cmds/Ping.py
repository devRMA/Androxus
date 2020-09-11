# coding=utf-8
# Androxus bot
# Ping.py

__author__ = 'Rafael'

from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['latency', 'latência'])
    async def ping(self, ctx):
        await ctx.send(f'Minha latência atual é de {int(self.bot.latency * 1000)}ms !')


def setup(bot):
    bot.add_cog(Ping(bot))
