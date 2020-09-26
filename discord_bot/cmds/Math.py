# coding=utf-8
# Androxus bot
# Math.py

__author__ = 'Rafael'

from datetime import datetime
import asyncio
from discord.ext import commands
import discord
from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.utils.Utils import random_color
from py_expression_eval import Parser
from os.path import exists
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_operações', 'help_operacoes', 'help_ops'])
    async def help_operators(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.operators.name,
                          descricao=self.operators.description,
                          exemplos=['``{pref}operações``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.operators.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(name='operações', aliases=['operators', 'operacoes', 'ops'],
                      description='Todas as operações que eu suporto no comando ``calc``!')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def operators(self, ctx):
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
        for ope_ex in operators.items():  # vai converter de dicionario para lista
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
                                    ', use o comando ``operações``)',
                          parametros=['<Operação(ões)>'],
                          exemplos=['``{pref}calc`` ``2 + 5 * 2``',
                                    '``{pref}calcular`` ``(2 + 5) * 2``',
                                    '``{pref}calc`` ``5 ^ 5``',
                                    '``{pref}calc`` ``2.5 * 4``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.calc.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['calcular'], description='Vou virar uma calculadora xD')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def calc(self, ctx, *args):
        if len(args) == 0:
            await self.help_calc(ctx)
            return
        async with ctx.channel.typing():  # vai aparecer "bot está digitando"
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
            except ZeroDivisionError:
                await ctx.send(
                    'Equação inválida! Ainda não sou capaz de resolver divisões por 0!\n<a:sad:755774681008832623>')
                return
            except Exception as exception:
                if 'unexpected' in exception.args[0]:
                    await ctx.send(
                        f'Parece que há um erro de digitação!\n```{args}```<:ah_nao:758003636822474887>')
                    return
                elif 'undefined variable' in exception.args[0]:
                    variavel_desconhecida = exception.args[0][exception.args[0].find(':') + 2:]
                    await ctx.send(
                        f'Desculpe, mas eu não sei o que é ``{variavel_desconhecida}`` <a:sad:755774681008832623>')
                    return
                elif 'unknown character' in exception.args[0]:
                    await ctx.send(
                        f'Desculpe, mas você digitou algum caracter que eu não conheço. <a:sad:755774681008832623>')
                    return
                elif 'unmatched "()"' in exception.args[0]:
                    await ctx.send(
                        f'Pare que você esqueceu de abrir ou fechar algum parêntese! <:ah_nao:758003636822474887>')
                    return
                elif 'parity' in exception.args[0]:
                    await ctx.send('Não consigo resolver está equação, verifique se você digitou tudo certo!')
                    return
                else:
                    await ctx.send('<a:sad:755774681008832623> Ocorreu um erro na hora de executar este comando,' +
                                   f' por favor informe este erro ao meu criador\n```{exception.args[0]}```')
                    return
            if len(str(resultado)) >= 200:
                await ctx.send('O resultado desta equação é tão grande que não consigo enviar a resposta!' +
                               '\n<a:sad:755774681008832623>')
                return
            embed = discord.Embed(title=f'<:calculator:757079712077053982> Resultado:',
                                  colour=discord.Colour(random_color()),
                                  description='\uFEFF',
                                  timestamp=datetime.utcnow())
            embed.add_field(name=f'Calculo:',
                            value=f'```{args}```',
                            inline=False)
            embed.add_field(name=f'Resposta:',
                            value=f'```{resultado}```',
                            inline=False)
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

    @commands.command(hidden=True, aliases=['help_regra_de_3', 'help_r3'])
    async def help_regra_de_tres(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.regra_de_tres.name,
                          descricao='Eu vou virar realizar uma regra de 3 simples para você!',
                          exemplos=['``{pref}regra_de_tres``',
                                    '``{pref}r3``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.regra_de_tres.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['regra_de_3', 'r3'], description='Eu vou fazer uma regra de três simples!')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def regra_de_tres(self, ctx):
        # TODO
        await ctx.send(
            f'Olá {ctx.author.mention}!\nPrimeiro, qual regra de três você quer que eu faça? ' +
            '(``inversamente``/``diretamente``)'
        )

        def check(message):
            return message.author == ctx.author

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send('Tempo esgotado!')
        modo = None
        path = ''
        if 'inversamente'.startswith(msg.content.lower()):
            modo = 'i'
        elif 'diretamente'.startswith(msg.content.lower()):
            modo = 'd'
        if modo:
            await ctx.send('Modo selecionado: ``diretamente proporcional``!')
            if exists('discord_bot/'):
                path = 'discord_bot/'
            else:
                path = './'
            if modo == 'd':
                valores = [
                    ['primeiro', 'v1'],
                    ['segundo', 'v2'],
                    ['terceiro', 'v3']
                ]
                pos_text_list = [
                    [(115, 210), 'v1'],
                    [(352, 210), 'v2'],
                    [(115, 406), 'v3'],
                    [(363, 406), 'x']
                ]
                valores_user = []
                for valor in valores:
                    img = Image.open(f'{path}images/regra_de_tres_direta.png')
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype(f'{path}fonts/helvetica-normal.ttf', 25)
                    black = (0, 0, 0)  # rgb
                    red = (255, 0, 0)  # rgb
                    for pos_text in pos_text_list:
                        if pos_text[-1] == valor[-1]:
                            draw.text(pos_text[0], pos_text[-1], red, font=font)
                        else:
                            draw.text(pos_text[0], pos_text[-1], black, font=font)
                    img.save(f'{path}images/regra_de_tres_direta-edited.png')
                    img.close()
                    await ctx.send(f'Agora, eu preciso que você me fale o {valor[0]} valor (**{valor[-1]} na foto**).',
                                   file=discord.File(f'{path}images/regra_de_tres_direta-edited.png'))
                    try:
                        value = await self.bot.wait_for('message', check=check, timeout=30)
                        try:
                            value = int(value.content)
                        except ValueError:
                            value = float(value.content.replace(',', '.'))
                        except:
                            return await ctx.send(f'O valor ``{value.content}`` não é um número!')
                    except asyncio.TimeoutError:
                        return await ctx.send('Tempo esgotado!')
                    for c in range(0, len(pos_text_list)):
                        if pos_text_list[c][-1] == valor[-1]:
                            pos_text_list[c][-1] = f'{value}'
                    valores_user.append(value)
                mult = valores_user[-1] * valores_user[1]
                resp = mult / valores_user[0]
                embed = discord.Embed(title=f'Regra de 3!',
                                      colour=discord.Colour(random_color()),
                                      description='Passo a passo da resolução:\n' +
                                                  f'**{valores_user[0]}x = {valores_user[-1]}×{valores_user[1]}**\n' +
                                                  f'**{valores_user[0]}x = {mult}**\n' +
                                                  f'**x = {mult}/{valores_user[0]}**\n' +
                                                  f'**x = {resp}**',
                                      timestamp=datetime.utcnow())
                embed.set_author(name='Androxus',
                                 icon_url=self.bot.user.avatar_url)
                embed.set_footer(text=f'{ctx.author}',
                                 icon_url=ctx.author.avatar_url)
                img = Image.open(f'{path}images/regra_de_tres_direta.png')
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(f'{path}fonts/helvetica-normal.ttf', 25)
                cor = (255, 0, 0)  # rgb
                pos1 = (115, 210)  # x e y
                pos2 = (352, 210)  # x e y
                pos3 = (115, 406)  # x e y
                posx = (363, 406)  # x e y
                text1 = str(valores_user[0])
                text2 = str(valores_user[1])
                text3 = str(valores_user[2])
                x = str(resp)
                draw.text(pos1, text1, cor, font=font)
                draw.text(pos2, text2, cor, font=font)
                draw.text(pos3, text3, cor, font=font)
                draw.text(posx, x, cor, font=font)
                img.save(f'{path}images/regra_de_tres_direta-edited.png')
                img.close()
                await ctx.send(embed=embed,
                               file=discord.File(f'{path}images/regra_de_tres_direta-edited.png'))
            elif modo == 'i':
                pass
        else:
            await ctx.send(f'{ctx.author.mention} eu não sei o que é ' +
                           f'``{msg.content}``! Eu aceito apenas ``inversamente`` ou ``diretamente``')


def setup(bot):
    bot.add_cog(Math(bot))
