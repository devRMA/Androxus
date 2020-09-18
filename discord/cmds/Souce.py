# coding=utf-8
# Androxus bot
# Source.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord.dao.ComandoDesativadoDao import ComandoDesativadoDao
from discord.modelos.EmbedHelp import embedHelp
from discord.Utils import random_color


class Source(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_github', 'help_programação'])
    async def help_source(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando='source',
                          descricao=self.source.description,
                          exemplos=['``{pref}source``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.source.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['github', 'programação'], description='Mostra o meu código fonte!')
    async def source(self, ctx):
        embed = discord.Embed(title=f'Olá {ctx.author.name}, eu sou um bot, feito em python, usa' +
                                    'ndo a API do discord e banco de dados!',
                              colour=discord.Colour(random_color()),
                              description='Caso você queira ver o meu código fonte, clique [aqui]' +
                                          '(https://github.com/devRMA/Androxus/tree/master/discord)\n' +
                                          'Caso você queira ver a documentação da API do discord,' +
                                          ' clique [aqui](https://discordpy.readthedocs.io/en/late' +
                                          'st/index.html).',
                              timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
        embed.set_author(name='Androxus', icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Source(bot))
