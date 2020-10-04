# coding=utf-8
# Androxus bot
# Fun.py

__author__ = 'Rafael'

from random import choice, seed

from discord.ext import commands

from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.utils.Utils import inverter_string


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
        await ctx.send(embed=embed)

    @commands.command(aliases=['8ball'], description='8ball tem a resposta para tudo!')
    async def eightball(self, ctx, *args):
        if len(args) == 0:
            await self.help_eightball(ctx)
            return
        args = ''.join(args).lower()
        respostas = ['Sim!', 'Não!', 'Acho que sim.',
                     'Acho que não.', 'Claro!', 'Claro que não!',
                     'Talvez sim.', 'Talvez não.',
                     'Eu responderia, mas não quero ferir seus sentimentos.',
                     'Se eu te responder, você não iria acreditar.',
                     '¯\_(ツ)_/¯',
                     'Hmmmm... :thinking:',
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
        asci_value = 0  # vai transformar a pergunta em asci, e usar este número como seed para pegar a resposta
        for c in args:
            try:
                asci_value += ord(c)
            except:
                pass
        seed(asci_value + ctx.author.id)
        await ctx.send(f'{choice(respostas)}')

    @commands.command(hidden=True, aliases=['help_cc', 'help_coinflip'])
    async def help_cara_coroa(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.cara_coroa.name,
                          descricao=self.cara_coroa.description,
                          exemplos=['``{pref}cara_coroa``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.cara_coroa.aliases.copy())
        await ctx.send(embed=embed)

    @commands.command(aliases=['cc', 'coinflip'], description='Cara ou coroa?')
    async def cara_coroa(self, ctx):
        respostas = ['🙂 Cara.', '👑 Coroa.']
        await ctx.send(f'{choice(respostas)}')

    @commands.command(hidden=True, aliases=['help_side-down', 'help_inverter'])
    async def help_girar(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.girar.name,
                          descricao=self.girar.description,
                          parametros=['<frase>'],
                          exemplos=['``{pref}girar`` ``muito show kkk``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.girar.aliases.copy())
        await ctx.send(embed=embed)

    @commands.command(aliases=['side-down', 'inverter'], description='Eu vou deixar a frase cabeça pra baixo.')
    async def girar(self, ctx, *args):
        if args:
            args = ' '.join(args)
            # anti mention
            args = args.replace(f'@', '@\uFEFF')
            args = args.replace(f'&', '&\uFEFF')
            if len(args) <= 600:
                await ctx.send(f'{ctx.author.mention} 🙃 {inverter_string(args)}')
            else:
                await ctx.send(f'{ctx.author.mention} você não acha que essa mensagem está grande não? \'-\'')
        else:
            await self.help_girar(ctx)


def setup(bot):
    bot.add_cog(Fun(bot))
