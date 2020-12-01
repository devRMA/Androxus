# -*- coding: utf-8 -*-
# Androxus bot
# Math.py

__author__ = 'Rafael'

import asyncio
from datetime import datetime
from os import remove
from os.path import exists

import discord
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from discord.ext import commands
from py_expression_eval import Parser

from Classes import Androxus
from utils.Utils import random_color, convert_to_string, prettify_number


class Math(commands.Cog, command_attrs=dict(category='matemática')):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.Androxus.Androxus): Instância do bot

        """
        self.bot = bot

    @Androxus.comando(name='operações',
                      aliases=['operators', 'operacoes', 'ops'],
                      description='Todas as operações que eu suporto no comando ``calc``!',
                      examples=['``{prefix}operações``', '{prefix}ops'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _operators(self, ctx):
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
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=f'{ctx.author}',
                         icon_url=ctx.author.avatar_url)
        for ope_ex in operators.items():  # vai converter de dicionario para lista
            embed.add_field(name=ope_ex[0],
                            value=ope_ex[-1],
                            inline=True)
        await ctx.send(embed=embed)

    @Androxus.comando(name='calc',
                      aliases=['calcular'],
                      descricao='Eu vou virar uma calculadora! (Caso você queira saber quais operações eu aceito'
                                ', use o comando ``operações``)',
                      parameters=['<operação(ões)>'],
                      examples=['``{prefix}calc`` ``2 + 5 * 2``',
                                '``{prefix}calcular`` ``(2 + 5) * 2``',
                                '``{prefix}calc`` ``5 ^ 5``',
                                '``{prefix}calc`` ``2.5 * 4``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _calc(self, ctx, *args):
        if len(args) == 0:
            await self.bot.send_help(ctx)
            return
        args = ' '.join(args)
        resultado = 0
        try:
            parser = Parser()
            resultado = parser.parse(args).evaluate({})
            if isinstance(resultado, bool):  # se o resultado veio como True ou False
                resultado = convert_to_string(resultado)
        except OverflowError:
            resultado = '∞'
        except ZeroDivisionError:
            resultado = '∞'
        except Exception as exception:
            if 'unexpected' in exception.args[0]:
                await ctx.send(
                    f'Parece que há um erro de digitação!\n```{args}```{self.bot.emoji("ah_nao")}')
                return
            elif 'undefined variable' in exception.args[0]:
                variavel_desconhecida = exception.args[0][exception.args[0].find(':') + 2:]
                await ctx.send(
                    f'Desculpe, mas eu não sei o que é ``{variavel_desconhecida}`` {self.bot.emoji("sad")}')
                return
            elif 'unknown character' in exception.args[0]:
                await ctx.send(
                    f'Desculpe, mas você digitou algum caracter que eu não conheço. {self.bot.emoji("sad")}')
                return
            elif 'unmatched "()"' in exception.args[0]:
                await ctx.send(
                    f'Pare que você esqueceu de abrir ou fechar algum parêntese! {self.bot.emoji("ah_nao")}')
                return
            elif 'parity' in exception.args[0]:
                await ctx.send('Não consigo resolver está operação, verifique se você digitou tudo certo!')
                return
            elif ('IndexError' in str(exception.__class__)) or ('math domain error' in exception.args[0]):
                await ctx.send(f'Estamos em {datetime.now().year}, mas ainda não sou capaz de resolver isso.')
                return
            else:
                await ctx.send(
                    f'{self.bot.emoji("sad")} Ocorreu um erro na hora de executar este comando,' +
                    f' por favor informe este erro ao meu criador\n```{exception.args[0]}```')
                return
        if len(str(resultado)) >= 400:
            await ctx.send('O resultado desta operação é tão grande que não consigo enviar a resposta!' +
                           f'\n{self.bot.emoji("sad")}')
            return
        embed = discord.Embed(title=f'{self.bot.emoji("calculator")} Resultado:',
                              colour=discord.Colour(random_color()),
                              timestamp=datetime.utcnow())
        embed.add_field(name=f'Calculo:',
                        value=f'```{args}```',
                        inline=False)
        embed.add_field(name=f'Resposta:',
                        value=f'```{prettify_number(resultado)}```',
                        inline=False)
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

    @Androxus.comando(name='regra_de_tres',
                      aliases=['regra_de_3', 'r3'],
                      description='Eu vou fazer uma regra de três simples!',
                      parameters=['<operação(ões)>'],
                      examples=['``{prefix}regra_de_tres``',
                                '``{prefix}r3``'])
    @discord.ext.commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _regra_de_tres(self, ctx):
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
            if exists('discord_bot/'):
                path = 'discord_bot/'
            else:
                path = './'
            if modo == 'd':
                await ctx.send('Modo selecionado: ``diretamente proporcional``!')
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
                        if not value.content.isdigit():
                            return await ctx.send(f'O valor ``{value.content}`` não é um número válido!')
                        try:
                            value = int(value.content)
                        except ValueError:
                            try:
                                value = float(value.content.replace(',', '.'))
                            except ValueError:
                                return await ctx.send(f'O valor ``{value.content}`` não é um número válido!')
                    except asyncio.TimeoutError:
                        return await ctx.send('Tempo esgotado!')
                    if value >= 5000:
                        return await ctx.send(
                            f'{ctx.author.mention} você não acha que ``{value}`` não é muito grande não?!')
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
                                                  f'**x = {prettify_number(resp)}**',
                                      timestamp=datetime.utcnow())
                embed.set_author(name=self.bot.user.name,
                                 icon_url=self.bot.user.avatar_url)
                embed.set_footer(text=f'{ctx.author}',
                                 icon_url=ctx.author.avatar_url)
                img = Image.open(f'{path}images/regra_de_tres_direta.png')
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(f'{path}fonts/helvetica-normal.ttf', 25)
                black = (0, 0, 0)  # rgb
                red = (255, 0, 0)  # rgb
                pos1 = (115, 210)  # x e y
                pos2 = (352, 210)  # x e y
                pos3 = (115, 406)  # x e y
                posx = (363, 406)  # x e y
                text1 = str(valores_user[0])
                text2 = str(valores_user[1])
                text3 = str(valores_user[2])
                x = f'{resp:.2f}'
                draw.text(pos1, text1, black, font=font)
                draw.text(pos2, text2, black, font=font)
                draw.text(pos3, text3, black, font=font)
                draw.text(posx, x, red, font=font)
                img.save(f'{path}images/regra_de_tres_direta-edited.png')
                img.close()
                await ctx.send(embed=embed,
                               file=discord.File(f'{path}images/regra_de_tres_direta-edited.png'))
                remove(f'{path}images/regra_de_tres_direta-edited.png')
            else:
                await ctx.send('Modo selecionado: ``inversamente proporcional``!')
                valores = [
                    ['primeiro', 'v1'],
                    ['segundo', 'v2'],
                    ['terceiro', 'v3']
                ]
                pos_text_list = [
                    [(60, 280), 'v1'],
                    [(400, 280), 'v2'],
                    [(60, 370), 'v3'],
                    [(400, 370), 'x']
                ]
                valores_user = []
                for valor in valores:
                    img = Image.open(f'{path}images/regra_de_tres_inversa.png')
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype(f'{path}fonts/helvetica-normal.ttf', 25)
                    black = (0, 0, 0)  # rgb
                    red = (255, 0, 0)  # rgb
                    for pos_text in pos_text_list:
                        if pos_text[-1] == valor[-1]:
                            draw.text(pos_text[0], pos_text[-1], red, font=font)
                        else:
                            draw.text(pos_text[0], pos_text[-1], black, font=font)
                    img.save(f'{path}images/regra_de_tres_inversa-edited.png')
                    img.close()
                    await ctx.send(f'Agora, eu preciso que você me fale o {valor[0]} valor (**{valor[-1]} na foto**).',
                                   file=discord.File(f'{path}images/regra_de_tres_inversa-edited.png'))
                    try:
                        value = await self.bot.wait_for('message', check=check, timeout=30)
                        if not value.content.isdigit():
                            return await ctx.send(f'O valor ``{value.content}`` não é um número válido!')
                        try:
                            value = int(value.content)
                        except ValueError:
                            try:
                                value = float(value.content.replace(',', '.'))
                            except ValueError:
                                return await ctx.send(f'O valor ``{value.content}`` não é um número válido!')
                    except asyncio.TimeoutError:
                        return await ctx.send('Tempo esgotado!')
                    if value >= 5000:
                        return await ctx.send(
                            f'{ctx.author.mention} você não acha que ``{value}`` não é muito grande não?!')
                    for c in range(0, len(pos_text_list)):
                        if pos_text_list[c][-1] == valor[-1]:
                            pos_text_list[c][-1] = f'{value}'
                    valores_user.append(value)
                mult = valores_user[0] * valores_user[1]
                resp = mult / valores_user[-1]
                embed = discord.Embed(title=f'Regra de 3!',
                                      colour=discord.Colour(random_color()),
                                      description='Passo a passo da resolução:\n' +
                                                  f'**{valores_user[-1]}x = {valores_user[0]}×{valores_user[1]}**\n' +
                                                  f'**{valores_user[-1]}x = {mult}**\n' +
                                                  f'**x = {mult}/{valores_user[-1]}**\n' +
                                                  f'**x = {prettify_number(resp)}**',
                                      timestamp=datetime.utcnow())
                embed.set_author(name=self.bot.user.name,
                                 icon_url=self.bot.user.avatar_url)
                embed.set_footer(text=f'{ctx.author}',
                                 icon_url=ctx.author.avatar_url)
                img = Image.open(f'{path}images/regra_de_tres_inversa.png')
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(f'{path}fonts/helvetica-normal.ttf', 25)
                black = (0, 0, 0)  # rgb
                red = (255, 0, 0)  # rgb
                pos1 = (60, 280)  # x e y
                pos2 = (400, 280)  # x e y
                pos3 = (60, 370)  # x e y
                posx = (400, 370)  # x e y
                text1 = str(valores_user[0])
                text2 = str(valores_user[1])
                text3 = str(valores_user[2])
                x = f'{resp:.2f}'
                draw.text(pos1, text1, black, font=font)
                draw.text(pos2, text2, black, font=font)
                draw.text(pos3, text3, black, font=font)
                draw.text(posx, x, red, font=font)
                img.save(f'{path}images/regra_de_tres_inversa-edited.png')
                img.close()
                await ctx.send(embed=embed,
                               file=discord.File(f'{path}images/regra_de_tres_inversa-edited.png'))
                remove(f'{path}images/regra_de_tres_inversa-edited.png')
        else:
            await ctx.send(f'{ctx.author.mention} eu não sei o que é ' +
                           f'``{msg.content}``! Eu aceito apenas ``inversamente`` ou ``diretamente``')


def setup(bot):
    bot.add_cog(Math(bot))
