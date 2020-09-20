# coding=utf-8
# Androxus bot
# Uptime.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord.modelos.EmbedHelp import embedHelp
from discord.Utils import random_color
from dateutil.relativedelta import relativedelta  # módulo que vai ser usado para subtrair datetime


class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_tempo_on'])
    async def help_uptime(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando='uptime',
                          descricao=self.uptime.description,
                          exemplos=['``{pref}uptime``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.uptime.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['tempo_on'], description='Mostra a quanto tempo eu estou online!')
    async def uptime(self, ctx):
        uptime = relativedelta(datetime.utcnow(), self.bot.uptime)
        seconds = uptime.seconds
        minutes = uptime.minutes
        hours = uptime.hours
        days = uptime.days
        dias_on = ''
        horas_on = ''
        minutos_on = ''
        # formatação da frase
        if days > 1:
            dias_on = f'{days} dias, '
        elif days == 1:
            dias_on = f'{days} dia, '
        if hours > 1:
            horas_on = f'{hours} horas, '
        elif hours == 1:
            horas_on = f'{hours} hora, '
        if minutes > 1:
            minutos_on = f'{minutes} minutos e '
        elif minutes == 1:
            minutos_on = f'{minutes} minuto e '
        embed = discord.Embed(title=f':timer:',
                              description=f'Estou on-line há {dias_on}{horas_on}{minutos_on}{seconds} segundos.',
                              colour=discord.Colour(random_color()),
                              timestamp=datetime.utcnow())
        embed.set_author(name='Androxus', icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Uptime(bot))
