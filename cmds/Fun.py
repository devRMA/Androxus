# -*- coding: utf-8 -*-
# Androxus bot
# Fun.py

__author__ = 'Rafael'

from random import choice, seed

from colorama import Style, Fore
from discord import AllowedMentions
from discord.ext import commands

from EmbedGenerators.HelpGroup import embed_help_group
from utils.Utils import inverter_string


class Fun(commands.Cog):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.General.Androxus): Instância do bot

        """
        self.bot = bot

    @commands.group(name='diversão', case_insensitive=True, invoke_without_command=True, ignore_extra=False,
                    aliases=['fun', 'diversao', 'funny'])
    async def diversao_gp(self, ctx):
        await ctx.reply(embed=await embed_help_group(ctx), mention_author=False)

    @diversao_gp.command(name='eightball',
                         aliases=['8ball', 'magicball'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _eightball(self, ctx, *, args=None):
        if args is None:
            return await self.bot.send_help(ctx)
        others = await self.bot.translate(ctx, others_='eightball')
        answers = others.get('answers')
        # vai transformar a pergunta em asci, e usar este número como seed para pegar a resposta
        # e a base, vai ser o id da pessoa
        asci_value = ctx.author.id + ctx.channel.id
        for c in args:
            # aqui, vamos fazer uma divisão, com o valor de cada caracter, pois assim
            # a ordem das letras na mensagem, vai implicar na resposta
            # se fosse uma soma simples, o bot teria a mesma resposta para as frase "opa", "aop", "poa"...
            if ord(c) != 0:
                asci_value /= ord(c)
        seed(asci_value)
        await ctx.reply(f'{choice(answers)}', mention_author=False)

    @diversao_gp.command(name='cara_coroa',
                         aliases=['cc', 'coinflip', 'coin_flip', 'caracoroa'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _cara_coroa(self, ctx):
        others = await self.bot.translate(ctx, others_='cara_coroa')
        answers = others.get('answers')
        await ctx.reply(choice(answers), mention_author=False)

    @diversao_gp.command(name='girar',
                         aliases=['side_down', 'sidedown', 'inverter'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _girar(self, ctx, *, args=None):
        if args:
            if len(args) <= 200:
                await ctx.reply(inverter_string(args), allowed_mentions=AllowedMentions.none())
            else:
                erros = await self.bot.translate(ctx, error_='girar')
                await ctx.send(**erros[0])
        else:
            await self.bot.send_help(ctx)


def setup(bot):
    cog = Fun(bot)
    cmds = f'{Fore.BLUE}{len(list(cog.walk_commands()))}{Fore.LIGHTMAGENTA_EX}'
    print(f'{Style.BRIGHT}{Fore.GREEN}[{"COG LOADED":^16}]' +
          f'{Fore.LIGHTMAGENTA_EX}{cog.qualified_name}({cmds}){Style.RESET_ALL}'.rjust(60))
    bot.add_cog(cog)
