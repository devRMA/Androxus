# -*- coding: utf-8 -*-
# Androxus bot
# Uteis.py

__author__ = 'Rafael'

from datetime import datetime
from re import compile

import discord
import emojis
import googletrans
from discord.ext import commands
from discord.ext.commands import BadArgument
from twemoji_parser import emoji_to_url

from Classes import Androxus
from database.Repositories.InformacoesRepository import InformacoesRepository
from dependencies import currency_exchange
from utils.Utils import is_number, prettify_number, datetime_format
from utils.permissions import check_permissions, bot_check_permissions

EMOJI_REGEX = compile(r'<a?:.+?:([0-9]{15,21})>')


class Uteis(commands.Cog, command_attrs=dict(category='úteis')):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.Androxus.Androxus): Instância do bot

        """
        self.bot = bot

    @Androxus.comando(name='money',
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
                                'euros)',
                                'Para saber todas as moedas que eu aceito, acesse [este link]'
                                '(https://github.com/tucnakomet1/Python-Currency-Exchange/blob/master/src/currency_'
                                'exchange.py#L62)'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _money(self, ctx, *args):
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
        result = float(f'{float(result.replace(",", "")):.2f}')
        um_valor = float(f'{float(um_valor):.2f}')
        embed = discord.Embed(title=f'🪙 {prettify_number(m_qtd)} {m_from.lower()} = {prettify_number(result)}'
                                    f' {m_to.lower()}',
                              colour=discord.Colour.random(),
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}',
                         icon_url=ctx.author.avatar_url)
        info = InformacoesRepository()
        # se ainda não tiver essa conversão no banco:
        if await info.get_dado(self.bot.db_connection, f'{m_from.upper()} to {m_to.upper()}') is None:
            # vai criar
            await info.create(self.bot.db_connection, f'{m_from.upper()} to {m_to.upper()}', f'{um_valor:.2f}')
            ultimo_valor = um_valor
        else:
            ultimo_valor = float(await info.get_dado(self.bot.db_connection, f'{m_from.upper()} to {m_to.upper()}'))
            await info.update(self.bot.db_connection, f'{m_from.upper()} to {m_to.upper()}', f'{um_valor:.2f}')
        if (ultimo_valor > um_valor) and (float(f'{(ultimo_valor - um_valor):.2f}') > 0.0):
            msg = f'O valor diminuiu {prettify_number((ultimo_valor - um_valor), truncate=True)}! ' \
                  f'{self.bot.emoji("diminuiu")}'
        elif (ultimo_valor < um_valor) and (float(f'{(um_valor - ultimo_valor):.2f}') > 0.0):
            msg = f'O valor aumentou {prettify_number((um_valor - ultimo_valor), truncate=True)}! ' \
                  f'{self.bot.emoji("aumentou")}'
        else:
            msg = 'Não teve alteração no valor.'
        embed.add_field(name=f'Com base na última vez que esse comando foi usado:\n{msg}',
                        value=f'Fonte: [x-rates](https://www.x-rates.com/calculator/?from={m_from}&to='
                              f'{m_to}&amount={m_qtd})',
                        inline=True)
        await ctx.reply(embed=embed, mention_author=False)

    @Androxus.comando(name='say',
                      aliases=['fale', 'falar'],
                      description='Eu vou repetir o que você falar!',
                      parameters=['[channel (padrão: o chat atual)]', '<frase>'],
                      examples=['``{prefix}say`` ``Hello World!!``',
                                '``{prefix}fale`` ``Olá Mundo!``'],
                      perm_user='gerenciar mensagens')
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _say(self, ctx, *, frase=''):
        if len(frase) == 0:
            await self.bot.send_help(ctx)
            return
        channel = ctx
        # se a pessoa tiver perm de gerenciar mensagens, vai ver se ela passou um chat
        # para o bot enviar a mensagem
        # se não entrar nesse if, o chat para enviar a mensagem vai ser o mesmo que o comando foi usado
        # e também vai ser adicionado quem mandou o bot falar aquilo, caso a pessoa não tenha permissão
        if await check_permissions(ctx, {'manage_messages': True}):
            channel_id = frase.split(' ')[0].replace('<#', '').replace('>', '')
            if is_number(channel_id) and (ctx.guild is not None):
                try:
                    channel = ctx.guild.get_channel(int(channel_id))
                except:
                    channel = ctx
                if channel is None:
                    return await ctx.send(f'{ctx.author.mention} Não consegui achar o chat que você me informou.'
                                          f' {self.bot.emoji("sad")}')
            else:
                channel = ctx
            if channel != ctx:
                frase = frase.replace(f'<#{channel_id}> ', '')
        else:
            frase += f'\n\n- {ctx.author}'
        # se a pessoa não tiver perm de marca everyone
        if await check_permissions(ctx, {'mention_everyone': False}):
            # vai tirar todas as menções da mensagem
            allowed_mentions = discord.AllowedMentions().none()
        else:
            # se a pessoa tiver perm, vai deixar marcar qualquer coisa
            allowed_mentions = discord.AllowedMentions().all()
        if len(frase) == 0:  # se após os filtros, a mensagem ficou vazia
            frase = '.'
        try:
            await channel.send(content=frase, allowed_mentions=allowed_mentions)
        except discord.Forbidden:
            return await ctx.send(
                f'{ctx.author.mention} eu não tenho permissão para enviar mensagem no chat {channel.mention}.'
                f' {self.bot.emoji("sad")}')
        if channel != ctx:
            await ctx.send(f'{ctx.author.mention} Mensagem enviada no chat {channel.mention} com sucesso!')
        else:  # se o channel for igual ao ctx
            # se o bot tiver perm de apagar mensagens:
            if await bot_check_permissions(ctx, manage_messages=True):
                await ctx.message.delete()

    @Androxus.comando(name='traduzir',
                      aliases=['tradutor', 'traduza', 'translate', 'translator'],
                      description='Eu vou traduzir alguma frase!',
                      parameters=['<língua final>', '<frase>'],
                      examples=['``{prefix}traduzir`` ``pt`` ``Hello world!``',
                                '``{prefix}translate`` ``en`` ``Olá Mundo!``',
                                '``{prefix}traduza`` ``pt`` ``Здравствуйте!``'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _traduzir(self, ctx, dest=None, *, frase=''):
        return await ctx.send('Comando em manutenção')
        # TODO
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
                                      f'{self.bot.emoji("sad")}')
            # anti mention:
            if ctx.message.mentions:  # se tiver alguma menção na mensagem
                for mention in ctx.message.mentions:
                    frase = frase.replace(f'<@{mention.id}>', '')
                    frase = frase.replace(f'<@!{mention.id}>', '')
            frase = frase.replace(f'@', '@\uFEFF')  # quebra o @everyone e o @here
            # se após a remoção das menções, não sobrar nada, para a execução
            if len(frase.replace(' ', '')) == 0: return await self.bot.send_help(ctx)
            msg = googletrans.Translator().translate(frase, dest=dest).text
            await ctx.send(content=f'{ctx.author.mention} {msg}')
        else:
            await self.bot.send_help(ctx)

    @Androxus.comando(name='emoji',
                      aliases=['emojiinfo', 'infoemoji'],
                      description='Eu vou mostrar alguns detalhes de algum emoji!',
                      parameters=['<emoji>'],
                      examples=['``{prefix}emoji`` ``Hello world!``',
                                '``{prefix}emoji`` ``Olá Mundo!``'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _emoji(self, ctx, *, args=None):
        if args is None:
            return await self.bot.send_help(ctx)
        try:
            emoji = await commands.EmojiConverter().convert(ctx, args)
        except BadArgument:
            try:
                regex_match = EMOJI_REGEX.match(args)
                emoji = await commands.PartialEmojiConverter().convert(ctx, regex_match.group())
            except:
                emoji = emojis.get(emojis.encode(args))
                if len(emoji) > 0:
                    emoji = list(emoji)[0]
                else:
                    return await ctx.send('Não encontrei este emoji!')
        if isinstance(emoji, discord.Emoji) or isinstance(emoji, discord.PartialEmoji):
            if hasattr(emoji, 'is_unicode_emoji') and emoji.is_unicode_emoji():
                return await ctx.reply('Não tenho suporte a esse tipo de emoji!', mention_author=False)
            embed = discord.Embed(title='Emoji personalizado',
                                  url=str(emoji.url),
                                  colour=discord.Colour.random(),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=str(emoji.url))
            embed.add_field(name='Tipo do emoji:',
                            value='`Animado`' if emoji.animated else '`Estático`',
                            inline=True)
            embed.add_field(name='Id:',
                            value=f'`{emoji.id}`',
                            inline=True)
            embed.add_field(name='Nome:',
                            value=f'`{emoji.name}`',
                            inline=True)
            embed.add_field(name='Uso:',
                            value='`<{}:{}:\u200b{}>`'.format('a' if emoji.animated else '',
                                                              emoji.name,
                                                              emoji.id),
                            inline=False)
            if isinstance(emoji, discord.Emoji):
                if emoji.guild == ctx.guild:
                    embed.add_field(name='E emoji é deste servidor!',
                                    value='** **',
                                    inline=True)
                embed.add_field(name='Criado em:',
                                value=f'`{emoji.created_at.strftime("%d/%m/%Y")}`({datetime_format(emoji.created_at)})',
                                inline=True)
        else:
            url = await emoji_to_url(emoji)
            if not url.startswith('https://twemoji.maxcdn.com/v/latest/72x72/'):
                return await ctx.reply('Não consegui achar este emoji!', mention_author=False)
            embed = discord.Embed(title=f'Detalhes sobre o emoji {emoji}',
                                  description='Infelizmente as informações estão em inglês.',
                                  url=url,
                                  colour=discord.Colour.random(),
                                  timestamp=datetime.utcnow())
            emoji = emojis.db.get_emoji_by_code(emoji)
            embed.set_thumbnail(url=url)
            if emoji is not None:
                embed.add_field(name='Emoji:',
                                value=f'\\{emoji.emoji}',
                                inline=False)
                if len(emoji.aliases) > 0:
                    embed.add_field(name='aliases:',
                                    value=f'`{", ".join(emoji.aliases)}`',
                                    inline=False)
                if len(emoji.tags) > 0:
                    embed.add_field(name='Tags:',
                                    value=f'`{", ".join(emoji.tags)}`',
                                    inline=False)
                if emoji.category != '':
                    embed.add_field(name='Category:',
                                    value=f'`{emoji.category}`',
                                    inline=False)
        return await ctx.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(Uteis(bot))
