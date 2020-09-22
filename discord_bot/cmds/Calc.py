# coding=utf-8
# Androxus bot
# Calc.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.Utils import random_color, get_emoji_dance
from py_expression_eval import Parser


class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_operações'])
    async def help_operators(self, ctx):
        operators = {
            'Operador: ``+``': 'Adição\nEx: ``2 + 2``\nVou responder: ``4``',
            'Operador: ``-``': 'Subtração\nEx: ``3 - 1``\nVou responder: ``2``',
            'Operador: ``*``': 'Multiplicação\nEx: ``2 * 3``\nVou responder: ``6``',
            'Operador: ``/``': 'Divisão\nEx: ``5 / 2``\nVou responder: ``2.5``',
            'Operador: ``%``': 'Resto da divisão\nEx: ``5 % 2``\nVou responder: ``1``',
            'Operador: ``^``': 'Exponenciação\nEx: ``5 ^ 2``\nVou responder: ``25``',
            'Constante: ``PI``': 'Exponenciação\nEx: ``PI``\nVou responder: ``3.1415``',
            'Constante: ``E``': 'Exponenciação\nEx: ``E``\nVou responder: ``2.7182``',
            'Função: ``sin(x)``': 'Seno\nEx: ``sin(0)``\nVou responder: ``0.0``',
            'Função: ``cos(x)``': 'Cosseno\nEx: ``cos(PI)``\nVou responder: ``-1.0``',
            'Função: ``tan(x)``': 'Tangente\nEx: ``tan(0)``\nVou responder: ``0.0``',
            'Função: ``asin(x)``': 'Arco seno\nEx: ``asin(0)``\nVou responder: ``0.0``',
            'Função: ``acos(x)``': 'Arco cosseno\nEx: ``acos(-1)``\nVou responder: ``3.1415``',
            'Função: ``atan(x)``': 'Arco tangente\nEx: ``atan(PI)``\nVou responder: ``1.2626``',
            'Função: ``log(x)``': 'Logaritmo, para a base E\nEx: ``log(1)``\nVou responder: ``0``',
            'Função: ``log(x, base)``': 'Logaritmo\nEx: ``log(16, 2)``\nVou responder: ``4.0``',
            'Função: ``abs(x)``': 'Valor absoluto\nEx: ``abs(-1)``\nVou responder: ``1``',
            'Função: ``ceil(x)``': 'Menor número inteiro maior ou igual a x\nEx: ``ceil(2.7)``\nVou responder: ``3.0``',
            'Função: ``floor(x)``': 'Maio número inteiro menor ou igual a x\nEx: ``floor(2.7)``\nVou responder: ``2.0``',
            'Função: ``round(x)``': 'Arredonda um número\nEx: ``round(2.7)``\nVou responder: ``3.0``',
            'Função: ``exp(x)``': 'Expoente de x,\nEx: ``exp(2)``\nVou responder: ``7.3890``'
        }
        embed = discord.Embed(title=f'Operações',
                              colour=discord.Colour(random_color()),
                              description='Todas as operações que eu suporto no comando ``calc``!',
                              timestamp=datetime.utcnow())
        embed.set_author(name='Androxus',
                         icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=f'{ctx.author}',
                         icon_url=ctx.author.avatar_url)
        for ope_ex in operators.items():  # vai transformar de dicionario para lista
            embed.add_field(name=ope_ex[0],
                            value=ope_ex[-1],
                            inline=True)
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(hidden=True, aliases=['help_calcular'])
    async def help_calc(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.calc.name,
                          descricao='Eu vou virar uma calculadora! (Caso você queira saber quais operações eu aceito' +
                                    ', use o comando ``help operações``)',
                          parametros=['<Operação(ões)>'],
                          exemplos=['``{pref}calc`` ``2 + 5 * 2``',
                                    '``{pref}calcular`` ``(2 + 5) * 2``',
                                    '``{pref}calc`` ``5 ^ 5``',
                                    '``{pref}calc`` ``2.5 * 4``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.calc.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['calcular'], description='Vou virar uma calculadora xD')
    async def calc(self, ctx, *args):
        if len(args) == 0:
            await self.help_calc(ctx)
            return
        args = ' '.join(args)
        resultado = 0
        try:
            parser = Parser()
            resultado = parser.parse(args).evaluate({})
            if isinstance(resultado, bool):  # se o resultado veio como True ou False
                resultado = str(resultado).replace('True', 'Sim').replace('False', 'Não')
        except OverflowError:
            await ctx.send(f'Está equação é muito grande para mim! <a:sad:755774681008832623>')
            return
        except Exception as exception:
            if 'unexpected' in exception.args[0]:
                # aqui, vai pegar o que estiver entre aspas
                erro = exception.args[0][exception.args[0].find('"')+1:exception.args[0].rfind('"')]
                onde_deu_erro = ' ' * exception.args[0].find(erro) + '👆'
                await ctx.send(f'Parece que há um erro de digitação!\n```{args}\n{onde_deu_erro}```')
                return
            elif 'undefined variable' in exception.args[0]:
                variavel_desconhecida = exception.args[0][exception.args[0].find(':') + 2:]
                await ctx.send(f'Desculpe, mas eu não sei o que é ``{variavel_desconhecida}`` <a:sad:755774681008832623>')
                return
            else:
                await ctx.send('<a:sad:755774681008832623> Ocorreu um erro na hora de executar este comando,' +
                               f' por favor informe este erro ao meu criador\n```{exception.args[0]}```')
                return
        except ZeroDivisionError:
            await ctx.send(
                'Equação inválida! Ainda não sou capaz de resolver divisões por 0!\n<a:sad:755774681008832623>')
            return
        if len(str(resultado)) >= 200:
            await ctx.send('O resultado desta equação é tão grande que não consigo enviar a resposta!' +
                           '\n<a:sad:755774681008832623>')
            return
        embed = discord.Embed(title=f'<:calculator:757079712077053982> Resultado:',
                              colour=discord.Colour(random_color()),
                              description=f'{resultado}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Calc(bot))
