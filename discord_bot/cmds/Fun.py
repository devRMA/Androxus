# coding=utf-8
# Androxus bot
# Fun.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord_bot.modelos.EmbedHelp import embedHelp
from random import choice, seed


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_8ball'])
    async def help_eightball(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.eightball.name,
                          descricao=self.eightball.description,
                          parametros=['<Pergunta>'],
                          exemplos=['``{pref}eightball`` ``Existe alguém mais lindo do que eu?``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.eightball.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['8ball'], description='8ball tem a resposta para tudo!')
    async def eightball(self, ctx, *args):
        if len(args) == 0:
            await self.help_eightball(ctx)
            return
        args = ' '.join(args)
        respostas = ['Sim!', 'Não!', 'Acho que sim.',
                     'Acho que não.', 'Claro!', 'Claro que não!',
                     'Talvez sim.', 'Talvez não.']
        asci_value = 0  # vai transformar a pergunta em asci, e usar este número como seed para pegar a resposta
        for c in args:
            try:
                asci_value += ord(c)
            except:
                pass
        seed(asci_value)
        await ctx.send(f'🎱{choice(respostas)}')

    @commands.command(hidden=True, aliases=['help_cc', 'help_coinflip'])
    async def help_cara_coroa(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.cara_coroa.name,
                          descricao=self.cara_coroa.description,
                          exemplos=['``{pref}cara_coroa``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.cara_coroa.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['cc', 'coinflip'], description='Cara ou coroa?')
    async def cara_coroa(self, ctx):
        respostas = ['Cara.', 'Coroa.']
        await ctx.send(f'🎱{choice(respostas)}')


def setup(bot):
    bot.add_cog(Fun(bot))
