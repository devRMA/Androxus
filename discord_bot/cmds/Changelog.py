# coding=utf-8
# Androxus bot
# Changelog.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.ext import commands

from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.utils.Utils import random_color, get_last_commit, get_last_update, datetime_format


class Changelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_ultima_att', 'help_última_att', 'help_att_log'])
    async def help_changelog(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.changelog.name,
                          descricao='Mostra quando foi a minha última atualização e ainda mostra o que foi alterado.',
                          exemplos=['``{pref}changelog``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.changelog.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['ultima_att', 'última_att', 'att_log'],
                      description='Mostra qual foi a última atualização que eu tive!')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def changelog(self, ctx):
        async with ctx.channel.typing():  # vai aparecer "bot está digitando"
            embed = discord.Embed(title=f'Ultima atualização que eu tive:',
                                  colour=discord.Colour(random_color()),
                                  description=f'```{get_last_commit()}```',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}',
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name='Atualização feita em:',
                            value=f'{datetime_format(get_last_update())}',
                            inline=True)
        await ctx.send(content=ctx.author.mention, embed=embed)


def setup(bot):
    bot.add_cog(Changelog(bot))
