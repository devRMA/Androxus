# -*- coding: utf-8 -*-
# Androxus bot
# OwnerOnly.py

__author__ = 'Rafael'

import ast
import asyncio
from datetime import datetime
from traceback import format_exc

import asyncpg
import discord
from discord.ext import commands
from stopwatch import Stopwatch

from Classes import Androxus
from database.Models.ComandoDesativado import ComandoDesativado
from database.Models.ComandoPersonalizado import ComandoPersonalizado
from database.Models.Servidor import Servidor
from database.Repositories.BlacklistRepository import BlacklistRepository
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.InformacoesRepository import InformacoesRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils import Utils as u
from utils import permissions
from utils.Utils import get_emoji_dance, random_color, datetime_format


class OwnerOnly(commands.Cog, command_attrs=dict(category='owner')):
    # algumas outras funções que só o dono do bot pode usar
    def __init__(self, bot):
        """

        Args:
            bot (Classes.Androxus.Androxus): Instância do bot

        """
        self.bot = bot

    @Androxus.comando(name='desativar_erros',
                      aliases=['desativar_tratamento_de_erro', 'erros_off'],
                      description='Vou desativar o tratamento de erros.',
                      examples=['``{prefix}erros_off``'],
                      perm_user='administrar a conta do bot',
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _desativar_erros(self, ctx):
        self.bot.unload_extension('events.ErrorCommands')
        await ctx.send('Tratamento de erro desativado!')

    @Androxus.comando(name='ativar_erros',
                      aliases=['ativar_tratamento_de_erro', 'erros_on'],
                      description='Vou reativar o tratamento de erros.',
                      examples=['``{prefix}erros_on``'],
                      perm_user='administrar a conta do bot',
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _ativar_erros(self, ctx):
        self.bot.load_extension('events.ErrorCommands')
        await ctx.send('Tratamento de erro ativado!')

    @Androxus.comando(name='game',
                      aliases=['jogar', 'status'],
                      description='Muda o meu status.',
                      parameters=['<frase>'],
                      examples=['``{prefix}game`` ``olá mundo!``', '``{prefix}game`` ``-1``'],
                      perm_user='administrar a conta do bot',
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _game(self, ctx, *args):
        if (len(args) == 1) and (args[0] == '-1'):  # se só tiver um item, e for -1
            self.bot.mudar_status = True
            embed = discord.Embed(title=f'Agora meus status vão ficar alterado!',
                                  colour=discord.Colour(random_color()),
                                  description=get_emoji_dance(),
                                  timestamp=datetime.utcnow())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        else:
            self.bot.mudar_status = False
            await self.bot.change_presence(activity=discord.Game(name=' '.join(args)))
            embed = discord.Embed(title=f'Status alterado!',
                                  colour=discord.Colour(random_color()),
                                  description=f'Agora eu estou jogando ``{" ".join(args)}``',
                                  timestamp=datetime.utcnow())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @Androxus.comando(name='dm',
                      aliases=['pv'],
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _dm(self, ctx, user_id: int, *, args):
        user = self.bot.get_user(user_id)
        if user is not None:
            foi = False
            if ctx.guild.id != 405826835793051649:
                try:
                    await ctx.message.delete()
                except discord.errors.Forbidden:
                    pass
            try:
                msg = await user.send(args)
                foi = True
            except discord.errors.Forbidden:
                pass
            try:
                if foi and (ctx.guild.id == 405826835793051649):
                    embed = discord.Embed(title=f'Mensagem enviada no privado do(a) {str(user)}!',
                                          colour=discord.Colour(random_color()),
                                          description=f'{args}\nId da mensagem: ``{msg.id}``',
                                          timestamp=datetime.utcnow())
                    embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                    embed.set_thumbnail(url=user.avatar_url)
                    await ctx.send(embed=embed)
                elif not foi and (ctx.guild.id == 405826835793051649):
                    embed = discord.Embed(title=f'O(A) {str(user)} está com o dm privado!',
                                          colour=discord.Colour(random_color()),
                                          timestamp=datetime.utcnow())
                    embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                    embed.set_thumbnail(url=user.avatar_url)
                    await ctx.send(embed=embed)
            except:
                pass
        else:
            if ctx.guild.id == 405826835793051649:
                await ctx.send('Não achei o usuário')

    @Androxus.comando(name='kill',
                      aliases=['reboot', 'reiniciar'],
                      description='Reinicia o bot.',
                      examples=['``{prefix}reboot``'],
                      perm_user='administrar a conta do bot',
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _kill(self, ctx):
        await ctx.send(f'Reiniciando {self.bot.emoji("loading")}')
        await self.bot.logout()
        raise SystemExit('Rebooting...')

    @Androxus.comando(name='sql',
                      aliases=['query', 'query_sql'],
                      description='Executa uma query sql no banco de dados.',
                      parameters=['<query sql>'],
                      examples=['``{prefix}sql`` ``select version();``'],
                      perm_user='administrar a conta do bot',
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _sql(self, ctx, *, query=''):
        msg_bot = None

        def check(reaction, user):
            author = user.id == ctx.author.id
            reactions = (str(reaction.emoji) == self.bot.emoji('cadeado')) or (
                    str(reaction.emoji) == self.bot.emoji('desativado'))
            message_check = reaction.message == msg_bot
            return author and reactions and message_check

        if query != '':
            if not query.endswith(';'):
                query += ';'
            modo = 'i'
            closed = discord.Embed(title=f'Query fechada {self.bot.emoji("check_verde")}',
                                   colour=discord.Colour(0xff6961),
                                   timestamp=datetime.utcnow())
            closed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            try:
                async with self.bot.db_connection.acquire() as conn:
                    conn.execute(query)
            except:
                erro = discord.Embed(title=f'{self.bot.emoji("atencao")} Erro ao executar query',
                                     colour=discord.Colour(0xff6961),
                                     timestamp=datetime.utcnow())
                erro.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                erro.add_field(name='📥 Input',
                               value=f'```sql\n{query}```',
                               inline=False)
                e = [f'- {c}' for c in format_exc().splitlines()]
                e = '\n'.join(e)
                erro.add_field(name=f'{self.bot.emoji("warning_flag")} Erro',
                               value=f'```diff\n{e}```',
                               inline=False)
                msg_bot = await ctx.send(embed=erro)
                await msg_bot.add_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["ativado"]))
                try:
                    await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                except asyncio.TimeoutError:
                    pass
                await msg_bot.remove_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["ativado"]), ctx.me)
                return await msg_bot.edit(embed=closed)
            e = discord.Embed(title=f'Query executada com sucesso!',
                              colour=discord.Colour(0xbdecb6),
                              timestamp=datetime.utcnow())
            e.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            e.add_field(name='📥 Input',
                        value=f'```sql\n{query}```',
                        inline=False)
            if 'select' in query.lower():
                modo = 's'
            if modo == 's':
                async with self.bot.db_connection.acquire() as conn:
                    e.add_field(name='📤 Output',
                                value=f'```py\n'
                                      f'{tuple(tuple(record) for record in await conn.fetch(query))}```',
                                inline=False)
            e.add_field(name='** **',
                        value=f'Essa mensagem será fechada em 2 minutos 🙂',
                        inline=False)
            msg_bot = await ctx.send(embed=e)
            await msg_bot.add_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["desativado"]))
            await msg_bot.add_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["cadeado"]))
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                if str(reaction.emoji) == self.bot.emoji("desativado"):
                    await msg_bot.edit(embed=closed)
                elif str(reaction.emoji) == self.bot.emoji("cadeado"):
                    e.remove_field(-1)
                    await msg_bot.edit(embed=e)
            except asyncio.TimeoutError:
                await msg_bot.edit(embed=closed)
            await msg_bot.remove_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["desativado"]), ctx.me)
            await msg_bot.remove_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["cadeado"]), ctx.me)
        else:
            return await self.bot.send_help(ctx)

    # font: https://gist.github.com/nitros12/2c3c265813121492655bc95aa54da6b9
    def __insert_returns(self, body):
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])
        if isinstance(body[-1], ast.If):
            self.__insert_returns(body[-1].body)
            self.__insert_returns(body[-1].orelse)
        if isinstance(body[-1], ast.With):
            self.__insert_returns(body[-1].body)

    @Androxus.comando(name='eval',
                      aliases=['ev', 'e'],
                      description='Executa um script em python.',
                      parameters=['<script>'],
                      examples=['``{prefix}eval`` ``return \'opa\'``'],
                      perm_user='administrar a conta do bot',
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _eval(self, ctx, *, cmd):
        msg_bot = None
        result_hastebin = None
        erro_hastebin = None

        def check(reaction, user):
            author = user.id == ctx.author.id
            reactions = (str(reaction.emoji) == self.bot.emoji("cadeado")) or (
                    str(reaction.emoji) == self.bot.emoji("desativado")) or (
                                str(reaction.emoji) == self.bot.emoji("ativado"))
            message_check = reaction.message == msg_bot
            return author and reactions and message_check

        closed = discord.Embed(title=f'Eval fechada {self.bot.emoji("check_verde")}',
                               colour=discord.Colour(0xff6961),
                               timestamp=datetime.utcnow())
        closed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        try:
            fn_name = '_eval_function'
            if cmd.startswith('```py'):
                cmd = cmd[5:]
            elif cmd.startswith('```'):
                cmd = cmd[3:]
            if cmd.endswith('```'):
                cmd = cmd[:-3]
            if cmd.endswith('\n'):
                cmd = cmd[1:]
            if not cmd.startswith('#nd'):
                # add a layer of indentation
                cmd = '\n'.join(f'    {i}' for i in cmd.splitlines())
                # wrap in async def body
                body = f'async def {fn_name}():\n{cmd}'
                retornar_algo = True
            else:
                body = f'{cmd}'
                retornar_algo = False
            execute_cmd = body
            if len(execute_cmd) > 1000:
                execute_cmd = f'{execute_cmd[:1000]}\n...'
            parsed = ast.parse(body)
            body = parsed.body[0].body

            self.__insert_returns(body)

            env = {
                'self': self,
                'discord': discord,
                'asyncpg': asyncpg,
                'asyncio': asyncio,
                'commands': commands,
                'datetime': datetime,
                'BlacklistRepository': BlacklistRepository,
                'ComandoDesativadoRepository': ComandoDesativadoRepository,
                'ComandoPersonalizadoRepository': ComandoPersonalizadoRepository,
                'InformacoesRepository': InformacoesRepository,
                'ServidorRepository': ServidorRepository,
                'ComandoDesativado': ComandoDesativado,
                'ComandoPersonalizado': ComandoPersonalizado,
                'Servidor': Servidor,
                'pegar_o_prefixo': u.pegar_o_prefixo,
                'random_color': u.random_color,
                'get_emoji_dance': u.get_emoji_dance,
                'get_last_update': u.get_last_update,
                'get_last_commit': u.get_last_commit,
                'get_configs': u.get_configs,
                'capitalize': u.capitalize,
                'datetime_format': u.datetime_format,
                'inverter_string': u.inverter_string,
                'is_number': u.is_number,
                'convert_to_bool': u.convert_to_bool,
                'convert_to_string': u.convert_to_string,
                'string_similarity': u.string_similarity,
                'get_most_similar_item': u.get_most_similar_item,
                'get_most_similar_items': u.get_most_similar_items,
                'difference_between_lists': u.difference_between_lists,
                'get_most_similar_items_with_similarity': u.get_most_similar_items_with_similarity,
                'prettify_number': u.prettify_number,
                'get_path_from_file': u.get_path_from_file,
                'hastebin_post': u.hastebin_post,
                'permissions': permissions,
                'Stopwatch': Stopwatch,
                'ctx': ctx,
                '__import__': __import__
            }
            exec(compile(parsed, filename='<ast>', mode='exec'), env)
            if retornar_algo:
                execution_time = Stopwatch()
                result = await eval(f'{fn_name}()', env)
                execution_time.stop()
                if result in ['nada', 'nda', 'null']:
                    retornar_algo = False
        except:
            erro = discord.Embed(title=f'{self.bot.emoji("atencao")} Erro no comando eval',
                                 colour=discord.Colour(0xff6961),
                                 timestamp=datetime.utcnow())
            erro.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            erro.add_field(name='📥 Input',
                           value=f'```py\n{execute_cmd}```',
                           inline=False)
            e = '\n'.join(f'- {c}' for c in format_exc().splitlines())
            if len(e) >= 500:
                e = f'{e[:500]}\n...'
                erro_hastebin = await u.hastebin_post(format_exc())
            erro.add_field(name=f'{self.bot.emoji("warning_flag")} Erro',
                           value=f'```diff\n{e}```',
                           inline=False)
            if erro_hastebin is not None:
                erro.add_field(name='** **',
                               value=f'😅 infelizmente o erro foi muito grande, clique [aqui]({erro_hastebin})'
                                     ' para ver o erro completo.',
                               inline=False)
            msg_bot = await ctx.send(embed=erro)
            await msg_bot.add_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["ativado"]))
            try:
                await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
            except asyncio.TimeoutError:
                pass
            await msg_bot.remove_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["ativado"]), ctx.me)
            return await msg_bot.edit(embed=closed)
        e = discord.Embed(title=f'Comando eval executado com sucesso!',
                          colour=discord.Colour(0xbdecb6),
                          timestamp=datetime.utcnow())
        e.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        e.add_field(name='📥 Input',
                    value=f'```py\n{execute_cmd}```',
                    inline=False)
        if retornar_algo:
            result_type = type(result)
            result_str = str(result)
            if u.is_number(result_str):
                result_str = u.prettify_number(result_str)
            if len(result_str) > 1000:
                result_hastebin = await u.hastebin_post(result)
                result_str = f'{result_str[:1000]}\n...'
            e.add_field(name='📤 Output',
                        value=f'```py\n{result_str}```',
                        inline=False)
            if result_hastebin is not None:
                e.add_field(name='** **',
                            value=f'😅 infelizmente o resultado ficou muito grande, clique [aqui]({result_hastebin})'
                                  ' para ver o resultado completo.',
                            inline=False)
            e.add_field(name='🤔 Tipo do return',
                        value=f'```py\n{result_type}```',
                        inline=False)
        e.add_field(name='⌚ Tempo de execução',
                    value=f'```md\n{str(execution_time)}\n====```',
                    inline=False)
        e.add_field(name='** **',
                    value=f'Essa mensagem será fechada em 2 minutos 🙂',
                    inline=False)
        msg_bot = await ctx.send(embed=e)
        await msg_bot.add_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["desativado"]))
        await msg_bot.add_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["cadeado"]))
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
            if str(reaction.emoji) == self.bot.emoji("desativado"):
                await msg_bot.edit(embed=closed)
            elif str(reaction.emoji) == self.bot.emoji("cadeado"):
                e.remove_field(-1)
                await msg_bot.edit(embed=e)
        except asyncio.TimeoutError:
            await msg_bot.edit(embed=closed)
        await msg_bot.remove_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["desativado"]), ctx.me)
        await msg_bot.remove_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["cadeado"]), ctx.me)

    @Androxus.comando(name='blacklist',
                      aliases=['blacklisted', 'banido'],
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _blacklist(self, ctx, *args):
        if ctx.prefix.replace('!', '').replace(' ', '') == self.bot.user.mention:
            # se a pessoa marcou o bot apenas 1 vez
            if ctx.message.content.replace('!', '').count(self.bot.user.mention) == 1:
                # vai tirar a menção da mensagem
                ctx.message.mentions.pop(0)
        if ctx.message.mentions:
            user_id = ctx.message.mentions[-1].id
        else:
            user_id = int(args[0])
        blacklisted = await BlacklistRepository().get_pessoa(self.bot.db_connection, user_id)
        if not blacklisted[0]:
            msg = f'O usuário <@!{user_id}> pode usar meus comandos! {get_emoji_dance()}'
        else:
            msg = f'{self.bot.emoji("no_no")} O usuário <@!{user_id}> foi banido de me usar!' + \
                  f'\nMotivo: `{blacklisted[1]}`\nQuando: `{datetime_format(blacklisted[-1])}`'
        return await ctx.send(msg)

    @Androxus.comando(name='add_blacklist',
                      aliases=['ab'],
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _add_blacklist(self, ctx, *args):
        if ctx.prefix.replace('!', '').replace(' ', '') == self.bot.user.mention:
            # se a pessoa marcou o bot apenas 1 vez
            if ctx.message.content.replace('!', '').count(self.bot.user.mention) == 1:
                # vai tirar a menção da mensagem
                ctx.message.mentions.pop(0)
        if ctx.message.mentions:
            user_id = ctx.message.mentions[-1].id
            args = ctx.message.content.split(' ')
            args.pop(0)
        else:
            user_id = int(args[0])
            args = list(args)
        args.pop(0)
        arg = args
        if args:
            motivo = ' '.join(arg)
        else:
            motivo = 'nulo'
        await BlacklistRepository().create(self.bot.db_connection, user_id, motivo)
        return await ctx.send(f'O usuário <@!{user_id}> não vai poder usar meus comandos! {self.bot.emoji("banido")}'
                              f'\nCom o motivo: {motivo}')

    @Androxus.comando(name='remove_blacklist',
                      aliases=['rb', 'whitelist'],
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _remove_blacklist(self, ctx, *args):
        if ctx.prefix.replace('!', '').replace(' ', '') == self.bot.user.mention:
            # se a pessoa marcou o bot apenas 1 vez
            if ctx.message.content.replace('!', '').count(self.bot.user.mention) == 1:
                # vai tirar a menção da mensagem
                ctx.message.mentions.pop(0)
        if ctx.message.mentions:
            user_id = ctx.message.mentions[-1].id
        else:
            user_id = int(args[0])
        await BlacklistRepository().delete(self.bot.db_connection, user_id)
        return await ctx.send(f'Usuário <@!{user_id}> perdoado! {get_emoji_dance()}')

    @Androxus.comando(name='manutenção_on',
                      aliases=['ativar_manutenção', 'man_on'],
                      description='Ativa o modo "em manutenção" do bot.',
                      examples=['``{prefix}manutenção_on``',
                                '``{prefix}ativar_manutenção``'],
                      perm_user='administrar a conta do bot',
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _manutencao_on(self, ctx):
        if not self.bot.maintenance_mode:
            self.bot.maintenance_mode = True
            self.bot.mudar_status = False
            await self.bot.change_presence(activity=discord.Game(name='Em manutenção!'))
            self.bot.unload_extension('events.ErrorCommands')
        await ctx.send(f'Modo manutenção:\n{self.bot.emoji("on")}')

    @Androxus.comando(name='manutenção_off',
                      aliases=['desativar_manutenção', 'man_off'],
                      description='Desativa o modo "em manutenção" do bot.',
                      examples=['``{prefix}manutenção_off``',
                                '``{prefix}desativar_manutenção``'],
                      perm_user='administrar a conta do bot',
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _manutencao_off(self, ctx):
        if self.bot.maintenance_mode:
            self.bot.maintenance_mode = False
            self.bot.mudar_status = True
            self.bot.load_extension('events.ErrorCommands')
        await ctx.send(f'Modo manutenção:\n{self.bot.emoji("off")}')

    @Androxus.comando(name='jsk_docs',
                      aliases=['docs_jsk', 'help_jsk', 'jsk_help', 'jh', 'dj'],
                      description='Mostra a documentação do jsk',
                      examples=['``{prefix}jsk_help``',
                                '``{prefix}jh``'],
                      perm_user='administrar a conta do bot',
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _jsk_docs(self, ctx):
        await ctx.send('Docs do jsk:\nhttps://jishaku.readthedocs.io/en/latest/cog.html')


def setup(bot):
    bot.add_cog(OwnerOnly(bot))
