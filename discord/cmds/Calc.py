# coding=utf-8
# Androxus bot
# Calc.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord.modelos.EmbedHelp import embedHelp
from discord.Utils import random_color


class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_calcular'])
    async def help_calc(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando='calc',
                          descricao='Para multiplicar, use ``*``. Para dividir use ``/``. Para usar potência, ' +
                                    'use ``**``. Use () para dar preferencia na hora de fazer os calculos!',
                          parametros=['<Operação(ões)>'],
                          exemplos=['``{pref}calc`` ``2 + 5 * 2``',
                                    '{pref}calcular ``(2 + 5) * 2``',
                                    '{pref}calc ``5 ** 5``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.calc.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['calcular'], description='Vou virar uma calculadora xD')
    async def calc(self, ctx, *args):
        chars_aceitaveis = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '+', '/', '%', '*', '-']
        if len(args) == 0:
            await self.help_calc(ctx)
            return
        for char in args:
            if not (char in chars_aceitaveis):
                await ctx.send(f'O caracter ``{char}`` não é nem um número, nem uma operação!')
                return
        embed = discord.Embed(title=f'<:calculator:757079712077053982> Resultado:',
                              colour=discord.Colour(random_color()),
                              description=f'{eval(" ".join(args))}',
                              timestamp=datetime.utcnow())
        embed.set_author(name='Androxus', icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Calc(bot))
