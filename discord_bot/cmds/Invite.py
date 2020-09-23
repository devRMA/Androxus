# coding=utf-8
# Androxus bot
# Invite.py

__author__ = 'Rafael'

from discord.ext import commands
from discord_bot.modelos.EmbedHelp import embedHelp


class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_convidar', 'help_convite'])
    async def help_invite(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.invite.name,
                          descricao=self.invite.description,
                          exemplos=['``{pref}invite``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.invite.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['convidar', 'convite'], description='Mostra o link que você usa para me adicionar em seu servidor')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def invite(self, ctx):
        await ctx.send(f'https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8')


def setup(bot):
    bot.add_cog(Invite(bot))
