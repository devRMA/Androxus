# coding=utf-8
# Androxus bot
# Uteis.py

__author__ = 'Rafael'

from datetime import datetime

import currency_exchange
import discord
import googletrans
from discord.ext import commands

from discord_bot.Classes import Androxus
from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.InformacoesRepository import InformacoesRepository
from discord_bot.utils.Utils import is_number, random_color


class Uteis(commands.Cog, command_attrs=dict(category='úteis')):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='money',
                      aliases=['money_converter', 'currency_exchange', 'ce', 'mon'],
                      description='Eu vou converter moedas, com a cotação atual e ainda dizer se a moeda valorizou ou '
                                  'desvalorizou!',
                      parameters=['[moeda base (padrão=USD)]',
                                  '[moeda final (padrão=BRL)]',
                                  '[quantidade (padrão=1)]'],
                      examples=['``{prefix}money``\n(Vou mostrar quanto vale 1 dólar em reais)',
                                '``{prefix}currency_exchange`` ``10``\n(Vou mostrar quanto vale 10 '
                                'dólares em reais)',
                                '``{prefix}ce`` ``eur``\n(Vou mostrar quanto vale 1 euro em reais)',
                                '``{prefix}mo`` ``eur`` ``20``\n(Vou mostrar quanto vale 20 euros em reais)',
                                '``{prefix}money`` ``usd`` ``eur`` ``50``\n(Vou mostrar quanto vale 50 dólares em '
                                'euros)'],
                      cls=Androxus.Command)
    async def money(self, ctx, *args):
        """
        possibilidades de uso do comando:
        money → vai responder 1 dólar em reais
        money 10 → vai responder 10 dólares em reais
        money eur → vai responder 1 euro em reais
        money aud 5 → vai responder 5 dólares australianos em reais
        money eur aud 1 → vai responder 1 euro em dólares australianos
        """
        m_from = 'USD'
        m_to = 'BRL'
        m_qtd = 1
        # se a pessoa não passou nada, vai continuar com esses valores padrões
        if args:  # se a pessoa passou pelo menos 1 argumento:
            # se a pessoa digitou "money 2" ou "mon 10.57"
            if is_number(args[0]):
                m_qtd = float(args[0])
            else:  # se o primeiro valor não for número
                def is_valid(value):
                    # todas as moedas que aceita
                    currencies = [c.split(' - ')[0] for c in currency_exchange.currencies()]
                    for currency in currencies:
                        if value == currency:
                            return True
                    return False

                # se a pessoa usar o comando assim: "money eur"
                if len(args) == 1:
                    if is_valid(args[0].upper()):
                        m_from = args[0].upper()
                    else:
                        # se não achou o que a pessoa passou:
                        return await self.bot.send_help(ctx)
                # se a pessoa usou o comando assim: "money aud 5"
                elif len(args) == 2:
                    if is_valid(args[0].upper()):
                        m_from = args[0].upper()
                        if is_number(args[-1]):
                            m_qtd = float(args[-1])
                        else:
                            return await self.bot.send_help(ctx)
                    else:
                        return await self.bot.send_help(ctx)
                # se a pessoa usou o comando assim: "money eur aud 1"
                elif len(args) == 3:
                    if is_valid(args[0].upper()):
                        m_from = args[0].upper()
                        if is_valid((args[1].upper())):
                            m_to = args[1].upper()
                            if is_number(args[-1]):
                                m_qtd = float(args[-1])
                            else:
                                return await self.bot.send_help(ctx)
                        else:
                            return await self.bot.send_help(ctx)
                    else:
                        return await self.bot.send_help(ctx)
                else:
                    # se a pessoa passou mais de 3 parâmetros:
                    return await self.bot.send_help(ctx)
        result, _ = currency_exchange.exchange(m_from, m_to, m_qtd, False)[0].split(' ')
        um_valor, _ = currency_exchange.exchange(m_from, m_to, 1, False)[0].split(' ')
        result = float(f'{float(result):.2f}')
        um_valor = float(f'{float(um_valor):.2f}')
        embed = discord.Embed(title=f'{m_qtd:.2f} {m_from.lower()} = {result:.2f} {m_to.lower()}',
                              colour=discord.Colour(random_color()),
                              description='** **',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}',
                         icon_url=ctx.author.avatar_url)
        conexao = Conexao()
        info = InformacoesRepository()
        ultimo_valor = 0.00
        # se ainda não tiver essa conversão no banco:
        if info.get_dado(conexao, f'{m_from.upper()} to {m_to.upper()}') is None:
            # vai criar
            info.create(conexao, f'{m_from.upper()} to {m_to.upper()}', f'{um_valor:.2f}')
            ultimo_valor = um_valor
        else:
            ultimo_valor = float(info.get_dado(conexao, f'{m_from.upper()} to {m_to.upper()}'))
            info.update(conexao, f'{m_from.upper()} to {m_to.upper()}', f'{um_valor:.2f}')
        msg = ''
        if ultimo_valor > um_valor:
            msg = f'O valor diminuiu {(ultimo_valor - result):.2f}! <:diminuiu:730088971077681162>'
        elif ultimo_valor < um_valor:
            msg = f'O valor aumentou {(result - ultimo_valor):.2f}! <:aumentou:730088970779623524>'
        else:
            msg = 'Não teve alteração no valor.'
        embed.add_field(name=f'Com base na última vez que esse comando foi usado:\n{msg}',
                        value=f'Fonte: [x-rates](https://www.x-rates.com/calculator/?from={m_from}&to='
                              f'{m_to}&amount={m_qtd})',
                        inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='say',
                      aliases=['fale', 'falar'],
                      description='Eu vou repetir o que você falar!',
                      parameters=['<frase>'],
                      examples=['``{prefix}say`` ``Hello World!!``',
                                '``{prefix}fale`` ``Olá Mundo!``'],
                      perm_user='gerenciar mensagens',
                      cls=Androxus.Command)
    async def say(self, ctx, *, frase):
        if len(frase) == 0:
            await self.bot.send_help(ctx)
            return
        try:
            if ctx.guild.me.guild_permissions.manage_messages:
                await ctx.message.delete()
            if not ctx.author.permissions_in(ctx.message.channel).manage_messages:
                frase += f'\n\n- {ctx.author}'
            # se a pessoa não tiver perm de marca everyone
            if not ctx.author.permissions_in(ctx.message.channel).mention_everyone:
                if ctx.message.mentions:  # se tiver alguma menção na mensagem
                    for mention in ctx.message.mentions:
                        frase = frase.replace(f'<@{mention.id}>', '')
                        frase = frase.replace(f'<@!{mention.id}>', '')
                frase = frase.replace(f'@', '@\uFEFF')
                frase = frase.replace(f'&', '&\uFEFF')
        except:  # se der algum erro, provavelmente é porque o comando foi usado no dm
            pass
        if len(frase) == 0:  # se após os filtros, a mensagem ficou vazia
            frase = '.'
        await ctx.send(frase)

    @commands.command(name='traduzir',
                      aliases=['tradutor', 'traduza', 'translate', 'translator'],
                      description='Eu vou traduzir alguma frase!',
                      parameters=['<língua final>', '<frase>'],
                      examples=['``{pref}traduzir`` ``pt`` ``Hello world!``',
                                '``{pref}translate`` ``en`` ``Olá Mundo!``',
                                '``{pref}traduza`` ``pt`` ``Здравствуйте!``'],
                      cls=Androxus.Command)
    async def traduzir(self, ctx, dest=None, *, frase=''):
        if dest and frase:
            from googletrans.constants import LANGUAGES
            dests = []
            for lang in LANGUAGES.items():
                # vai pegar o dicionario de todas as linguas que o módulo aceita
                # e transformar em uma lista, apenas com a abreviação
                dests.append(lang[0])
            if not dest in dests:  # se o "dest" que a pessoa passou não for válido:
                return await ctx.send(f'Não encontrei nenhuma lingua chamada ``{dest}``!\n' +
                                      'Por favor, verifique se você digitou a abreviação certa!\n' +
                                      '<a:sad:755774681008832623>')
            # anti mention:
            if ctx.message.mentions:  # se tiver alguma menção na mensagem
                for mention in ctx.message.mentions:
                    frase = frase.replace(f'<@{mention.id}>', '')
                    frase = frase.replace(f'<@!{mention.id}>', '')
            frase = frase.replace(f'@', '@\uFEFF')  # quebra o @everyone e o @here
            # se após a remoção das menções, não sobrar nada, para a execução
            if len(frase.replace(' ', '')) == 0: return await self.help_traduzir(ctx)
            msg = googletrans.Translator().translate(frase, dest=dest).text.capitalize()
            await ctx.send(content=f'{ctx.author.mention} {msg}')
        else:
            await self.bot.send_help(ctx)


def setup(bot):
    bot.add_cog(Uteis(bot))
