# coding=utf-8
# Androxus bot
# Converter.py

__author__ = 'Rafael'

import asyncio
from datetime import datetime

import currency_exchange
import discord
from discord.ext import commands
from googletrans import Translator

from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.InformacoesRepository import InformacoesRepository
from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.utils.Utils import isnumber, random_color


class Converter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_money_converter',
                                            'help_currency_exchange',
                                            'help_ce',
                                            'help_mon'])
    async def help_money(self, ctx):
        embed1 = embedHelp(self.bot,
                           ctx,
                           comando=self.money.name,
                           descricao=self.money.description,
                           parametros=['[moeda base (padrão=USD)]',
                                       '[moeda final (padrão=BRL)]',
                                       '[quantidade (padrão=1)]'],
                           exemplos=['``{pref}money``\n(Vou mostrar quanto vale 1 dólar em reais)',
                                     '``{pref}currency_exchange`` ``10``\n(Vou mostrar quanto vale 10 '
                                     'dólares em reais)',
                                     '``{pref}ce`` ``eur``\n(Vou mostrar quanto vale 1 euro em reais)',
                                     '``{pref}mo`` ``eur`` ``20``\n(Vou mostrar quanto vale 20 euros em reais)',
                                     '``{pref}money`` ``usd`` ``eur`` ``50``\n(Vou mostrar quanto vale 50 dólares em '
                                     'euros)'],
                           # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                           aliases=self.money.aliases.copy())
        embed1.add_field(name=f'Para saber todas as abreviações das moedas que eu aceito, clique em ➕',
                         value=f'** **',
                         inline=True)
        embed2 = discord.Embed(title=f'Todas as moedas que eu aceito no comando "{ctx.prefix}money"',
                               colour=discord.Colour(random_color()),
                               description='** **',
                               timestamp=datetime.utcnow())
        translator = Translator()
        moedas = ''
        for c in currency_exchange.currencies():
            moedas += f'{c}\n'
        moedas = translator.translate(moedas, dest='pt').text
        for c in moedas.splitlines():
            abreviacao, moeda = c.split(' - ')
            embed2.add_field(name=f'**{abreviacao}**',
                             value=f'{moeda}',
                             inline=True)

        async def menu_help(ctx, msg):
            def check_page1(reaction, user):  # fica verificando a pagina 1, para ver se é para ir para a pagina 2
                return (user.id == ctx.author.id) and (str(reaction.emoji) == '➕')

            def check_page2(reaction, user):  # fica verificando a pagina 2, para ver se é para ir para a pagina 1
                return (user.id == ctx.author.id) and (str(reaction.emoji) == '➖')

            async def check_reactions_without_perm(ctx, msg, bot):
                # mudas as páginas, se o bot não tiver perm pra apagar reações
                while True:
                    await bot.wait_for('reaction_add', timeout=900.0, check=check_page1)
                    await msg.delete()
                    msg = await ctx.send(embed=embed2)
                    await msg.add_reaction('➖')
                    await bot.wait_for('reaction_add', timeout=900.0, check=check_page2)
                    await msg.delete()
                    msg = await ctx.send(embed=embed1)
                    await msg.add_reaction('➕')

            async def check_reactions_with_perm(msg, bot):
                # mudas as páginas, se o bot tiver perm pra apagar reações
                while True:
                    await bot.wait_for('reaction_add', timeout=900.0, check=check_page1)
                    await msg.clear_reactions()
                    await msg.add_reaction('➖')
                    await msg.edit(embed=embed2)
                    await bot.wait_for('reaction_add', timeout=900.0, check=check_page2)
                    await msg.clear_reactions()
                    await msg.add_reaction('➕')
                    await msg.edit(embed=embed1)

            # se foi usado num servidor:
            if ctx.guild:
                # se o bot tiver perm pra usar o "clear_reactions"
                if ctx.guild.me.guild_permissions.manage_messages:
                    await check_reactions_with_perm(msg, self.bot)
                else:  # se o bot não tiver permissão:
                    await check_reactions_without_perm(ctx, msg, self.bot)
            else:  # se não for usado no servidor:
                await check_reactions_without_perm(ctx, msg, self.bot)

        msg_bot = await ctx.send(embed=embed1)
        await msg_bot.add_reaction('➕')
        try:
            # vai fica 1 minuto e meio esperando o usuário apertas nas reações
            await asyncio.wait_for(menu_help(ctx, msg_bot), timeout=90.0)
        except asyncio.TimeoutError:  # se acabar o tempo
            pass

    @commands.command(aliases=['money_converter', 'currency_exchange', 'ce', 'mon'],
                      description='Eu vou converter moedas, com a cotação atual!')
    async def money(self, ctx, *args):
        """
        possibilidades de uso do comando:
        money → vai responder 1 dólar em reais
        money 10 → vai responder 10 dólares em reais
        money eur → vai responder 1 euro em reais
        money aud 5 → vai responder 5 dólares australianos em reais
        money eur aud 1 → vai responder 1 euro em dólares australianos
        """
        async with ctx.channel.typing():  # vai aparecer "bot está digitando"
            m_from = 'USD'
            m_to = 'BRL'
            m_qtd = 1
            # se a pessoa não passou nada, vai continuar com esses valores padrões
            if args:  # se a pessoa passou pelo menos 1 argumento:
                # se a pessoa digitou "money 2" ou "mon 10.57"
                if isnumber(args[0]):
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
                            return await self.help_money(ctx)
                    # se a pessoa usou o comando assim: "money aud 5"
                    elif len(args) == 2:
                        if is_valid(args[0].upper()):
                            m_from = args[0].upper()
                            if isnumber(args[-1]):
                                m_qtd = float(args[-1])
                            else:
                                return await self.help_money(ctx)
                        else:
                            return await self.help_money(ctx)
                    # se a pessoa usou o comando assim: "money eur aud 1"
                    elif len(args) == 3:
                        if is_valid(args[0].upper()):
                            m_from = args[0].upper()
                            if is_valid((args[1].upper())):
                                m_to = args[1].upper()
                                if isnumber(args[-1]):
                                    m_qtd = float(args[-1])
                                else:
                                    return await self.help_money(ctx)
                            else:
                                return await self.help_money(ctx)
                        else:
                            return await self.help_money(ctx)
                    else:
                        # se a pessoa passou mais de 3 parâmetros:
                        return await self.help_money(ctx)
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


def setup(bot):
    bot.add_cog(Converter(bot))
