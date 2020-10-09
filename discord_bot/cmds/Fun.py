# coding=utf-8
# Androxus bot
# Fun.py

__author__ = 'Rafael'

from random import choice, seed

from discord.ext import commands

from discord_bot.Classes import Androxus
from discord_bot.utils.Utils import inverter_string


class Fun(commands.Cog, command_attrs=dict(category='diversão')):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='eightball',
                      aliases=['8ball'],
                      description='8ball tem a resposta para tudo!',
                      parameters=['<pergunta>'],
                      examples=['``{prefix}eightball`` ``Existe alguém mais lindo do que eu?``'],
                      cls=Androxus.Command)
    async def _eightball(self, ctx, *args):
        if len(args) == 0:
            return await self.bot.send_help(ctx)
        args = ''.join(args).lower()
        respostas = ['Sim!', 'Não!', 'Acho que sim.',
                     'Acho que não.', 'Claro!', 'Claro que não!',
                     'Talvez sim.', 'Talvez não.',
                     'Eu responderia, mas não quero ferir seus sentimentos.',
                     'Se eu te responder, você não iria acreditar.',
                     '¯\_(ツ)_/¯',
                     'Hmmmm... 🤔',
                     'Minhas fontes dizem que sim.',
                     'Minhas fontes dizem que não.',
                     'Do jeito que eu vejo, não.',
                     'Do jeito que eu vejo, sim.',
                     'Não posso falar sobre isso.',
                     'Provavelmente sim.',
                     'Provavelmente não.',
                     'A resposta para isso é um grande mistério.',
                     'Apenas super xandão tem a resposta para isso.',
                     'Pergunta para o seu professor.',
                     'Eu tenho cara de google?']
        # vai transformar a pergunta em asci, e usar este número como seed para pegar a resposta
        # e a base, vai ser o id da pessoa
        asci_value = ctx.author.id
        for c in args:
            try:
                # aqui, vamos fazer uma divisão, com o valor de cada caracter, pois assim
                # a ordem das letras na mensagem, vai implicar na resposta
                # se fosse uma soma simples, o bot teria a mesma resposta para as frase "opa", "aop", "poa"...
                if ord(c) != 0:
                    asci_value /= ord(c)
            except:
                pass
        seed(asci_value)
        await ctx.send(f'{choice(respostas)}')

    @commands.command(name='cara_coroa',
                      aliases=['cc', 'coinflip'],
                      description='Cara ou coroa?',
                      examples=['``{prefix}cara_coroa``'],
                      cls=Androxus.Command)
    async def _cara_coroa(self, ctx):
        respostas = ['🙂 Cara.', '👑 Coroa.']
        await ctx.send(f'{choice(respostas)}')

    @commands.command(name='girar',
                      aliases=['side-down', 'inverter'],
                      description='Eu vou deixar a frase cabeça pra baixo.',
                      examples=['``{prefix}girar`` ``muito show kkk``'],
                      cls=Androxus.Command)
    async def _girar(self, ctx, *, args):
        if args:
            # anti mention
            args = args.replace(f'@', '@\uFEFF')
            args = args.replace(f'&', '&\uFEFF')
            if len(args) <= 200:
                await ctx.send(f'{ctx.author.mention} 🙃 {inverter_string(args)}')
            else:
                await ctx.send(f'{ctx.author.mention} você não acha que essa mensagem está grande não? \'-\'')
        else:
            await self.bot.send_help(ctx)


def setup(bot):
    bot.add_cog(Fun(bot))
