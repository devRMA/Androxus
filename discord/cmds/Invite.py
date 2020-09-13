# coding=utf-8
# Androxus bot
# Invite.py

__author__ = 'Rafael'

from discord.ext import commands


class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Mostra o link que você usa para me adicionar em servidores')
    async def invite(self, ctx):
        await ctx.send(f'https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8')


def setup(bot):
    bot.add_cog(Invite(bot))
