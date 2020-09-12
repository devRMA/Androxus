# coding=utf-8
# Androxus bot
# Help.py

__author__ = 'Rafael'

from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ajuda'])
    async def help(self, ctx):
        await ctx.send('https://androxus.herokuapp.com/')


def setup(bot):
    bot.add_cog(Help(bot))
