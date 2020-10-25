# coding=utf-8
# Androxus bot
# OwnerOnly.py

__author__ = 'Rafael'

import ast
import asyncio
from datetime import datetime

import discord
from discord.ext import commands
from stopwatch import Stopwatch

from Classes import Androxus
from database.ComandoDesativado import ComandoDesativado
from database.ComandoPersonalizado import ComandoPersonalizado
from database.Conexao import Conexao
from database.Repositories.BlacklistRepository import BlacklistRepository
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.InformacoesRepository import InformacoesRepository
from database.Repositories.ServidorRepository import ServidorRepository
from database.Servidor import Servidor
from utils import Utils as u
from utils import permissions
from utils.Utils import get_emoji_dance, random_color, datetime_format


class OwnerOnly(commands.Cog, command_attrs=dict(category='owner')):
    # algumas outras funções que só o dono do bot pode usar
    def __init__(self, bot):
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
            embed.set_author(name='Androxus', icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        else:
            self.bot.mudar_status = False
            await self.bot.change_presence(activity=discord.Game(name=' '.join(args)))
            embed = discord.Embed(title=f'Status alterado!',
                                  colour=discord.Colour(random_color()),
                                  description=f'Agora eu estou jogando ``{" ".join(args)}``',
                                  timestamp=datetime.utcnow())
            embed.set_author(name='Androxus', icon_url=self.bot.user.avatar_url)
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
                    embed.set_author(name='Androxus', icon_url=self.bot.user.avatar_url)
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
        await ctx.send(f'Reiniciando {self.bot.configs["emojis"]["loading"]}')
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
            reactions = (str(reaction.emoji) == self.bot.configs['emoji']['cadeado']) or (
                    str(reaction.emoji) == self.bot.configs['emoji']['desativado'])
            message_check = reaction.message == msg_bot
            return author and reactions and message_check

        if query:
            if query[-1] != ';':
                query += ';'
            conexao = Conexao()
            cursor = conexao.cursor()
            modo = 'i'
            closed = discord.Embed(title=f'Query fechada {self.bot.configs["emojis"]["check_verde"]}',
                                   colour=discord.Colour(0xff6961),
                                   description='** **',
                                   timestamp=datetime.utcnow())
            closed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            try:
                cursor.execute(query)
            except Exception as e:
                conexao.fechar()
                erro = discord.Embed(title=f'{self.bot.configs["emojis"]["atencao"]} Erro ao executar query',
                                     colour=discord.Colour(0xff6961),
                                     description='** **',
                                     timestamp=datetime.utcnow())
                erro.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                erro.add_field(name='📥 Input',
                               value=f'```sql\n{query}```',
                               inline=False)
                e = [f'- {c}' for c in str(e).splitlines()]
                e = '\n'.join(e)
                erro.add_field(name=f'{self.bot.configs["emojis"]["warning_flag"]} Erro',
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
                              description='** **',
                              timestamp=datetime.utcnow())
            e.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            e.add_field(name='📥 Input',
                        value=f'```sql\n{query}```',
                        inline=False)
            if 'select' in query.lower():
                modo = 's'
            if modo == 'i':
                conexao.salvar()
            if modo == 's':
                e.add_field(name='📤 Output',
                            value=f'```py\n{cursor.fetchall()}```',
                            inline=False)
            conexao.fechar()
            e.add_field(name='** **',
                        value=f'Essa mensagem será fechada em 2 minutos 🙂',
                        inline=False)
            msg_bot = await ctx.send(embed=e)
            await msg_bot.add_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["desativado"]))
            await msg_bot.add_reaction(self.bot.get_emoji(self.bot.configs["emojis"]["ids"]["cadeado"]))
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                if str(reaction.emoji) == self.bot.configs["emojis"]["desativado"]:
                    await msg_bot.edit(embed=closed)
                elif str(reaction.emoji) == self.bot.configs["emojis"]["cadeado"]:
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
                      aliases=['ev'],
                      description='Executa um script em python.',
                      parameters=['<script>'],
                      examples=['``{prefix}eval`` ``return \'opa\'``'],
                      perm_user='administrar a conta do bot',
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _eval(self, ctx, *, cmd):
        execution_time = Stopwatch()
        msg_bot = None

        def check(reaction, user):
            author = user.id == ctx.author.id
            reactions = (str(reaction.emoji) == self.bot.configs["emojis"]["cadeado"]) or (
                    str(reaction.emoji) == self.bot.configs["emojis"]["desativado"]) or (
                    str(reaction.emoji) == self.bot.configs["emojis"]["ativado"])
            message_check = reaction.message == msg_bot
            return author and reactions and message_check

        closed = discord.Embed(title=f'Eval fechada {self.bot.configs["emojis"]["check_verde"]}',
                               colour=discord.Colour(0xff6961),
                               description='** **',
                               timestamp=datetime.utcnow())
        closed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        try:
            fn_name = '__eval_function'
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
                'commands': commands,
                'datetime': datetime,
                'Androxus': Androxus,
                'BlacklistRepository': BlacklistRepository,
                'ComandoDesativadoRepository': ComandoDesativadoRepository,
                'ComandoPersonalizadoRepository': ComandoPersonalizadoRepository,
                'InformacoesRepository': InformacoesRepository,
                'ServidorRepository': ServidorRepository,
                'ComandoDesativado': ComandoDesativado,
                'ComandoPersonalizado': ComandoPersonalizado,
                'Conexao': Conexao,
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
                'permissions': permissions,
                'Stopwatch': Stopwatch,
                'ctx': ctx,
                '__import__': __import__
            }
            exec(compile(parsed, filename='<ast>', mode='exec'), env)
            if retornar_algo:
                result = (await eval(f'{fn_name}()', env))
                if result in ['nada', 'nda', 'null']:
                    retornar_algo = False
        except Exception as e:
            execution_time.stop()
            erro = discord.Embed(title=f'{self.bot.configs["emojis"]["atencao"]} Erro no comando eval',
                                 colour=discord.Colour(0xff6961),
                                 description='** **',
                                 timestamp=datetime.utcnow())
            erro.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            erro.add_field(name='📥 Input',
                           value=f'```py\n{execute_cmd}```',
                           inline=False)
            e = [f'- {c}' for c in str(e).splitlines()]
            e = '\n'.join(e)
            erro.add_field(name=f'{self.bot.configs["emojis"]["warning_flag"]} Erro',
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
        execution_time.stop()
        e = discord.Embed(title=f'Comando eval executado com sucesso!',
                          colour=discord.Colour(0xbdecb6),
                          description='** **',
                          timestamp=datetime.utcnow())
        e.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        e.add_field(name='📥 Input',
                    value=f'```py\n{execute_cmd}```',
                    inline=False)
        if retornar_algo:
            result_type = type(result)
            result_str = str(result)
            if len(result_str) > 1000:
                result_str = f'{result_str[:1000]}\n...'
            e.add_field(name='📤 Output',
                        value=f'```py\n{result_str}```',
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
            if str(reaction.emoji) == self.bot.configs["emojis"]["desativado"]:
                await msg_bot.edit(embed=closed)
            elif str(reaction.emoji) == self.bot.configs["emojis"]["cadeado"]:
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
        conexao = Conexao()
        if ctx.prefix.replace('!', '').replace(' ', '') == self.bot.user.mention:
            # se a pessoa marcou o bot apenas 1 vez
            if ctx.message.content.replace('!', '').count(self.bot.user.mention) == 1:
                # vai tirar a menção da mensagem
                ctx.message.mentions.pop(0)
        if ctx.message.mentions:
            user_id = ctx.message.mentions[-1].id
        else:
            user_id = int(args[0])
        blacklisted = BlacklistRepository().get_pessoa(conexao, user_id)
        conexao.fechar()
        if not blacklisted[0]:
            msg = f'A pessoa pode usar meus comandos! {get_emoji_dance()}'
        else:
            msg = f'{self.bot.configs["emojis"]["no_no"]} Esse usuário foi banido de me usar!' + \
                  f'\nMotivo: `{blacklisted[1]}`\nQuando: {datetime_format(blacklisted[-1])}'
        return await ctx.send(msg)

    @Androxus.comando(name='add_blacklist',
                      aliases=['ab'],
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _add_blacklist(self, ctx, *args):
        conexao = Conexao()
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
        try:
            BlacklistRepository().create(conexao, user_id, motivo)
            conexao.fechar()
        except Exception as e:
            if str(e) == 'blacklisted':
                return await ctx.send('Essa pessoa já está na blacklist!')
        return await ctx.send(f'Este usuário não vai poder usar meus comandos! {self.bot.configs["emojis"]["banido"]}'
                              f'\nCom o motivo: {motivo}')

    @Androxus.comando(name='remove_blacklist',
                      aliases=['rb', 'whitelist'],
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _remove_blacklist(self, ctx, *args):
        conexao = Conexao()
        if ctx.prefix.replace('!', '').replace(' ', '') == self.bot.user.mention:
            # se a pessoa marcou o bot apenas 1 vez
            if ctx.message.content.replace('!', '').count(self.bot.user.mention) == 1:
                # vai tirar a menção da mensagem
                ctx.message.mentions.pop(0)
        if ctx.message.mentions:
            user_id = ctx.message.mentions[-1].id
        else:
            user_id = int(args[0])
        BlacklistRepository().delete(conexao, user_id)
        conexao.fechar()
        return await ctx.send(f'Usuário perdoado! {get_emoji_dance()}')

    @Androxus.comando(name='manutenção_on',
                      aliases=['ativar_manutenção'],
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
        await ctx.send(f'Modo manutenção:\n{self.bot.configs["emojis"]["on"]}')

    @Androxus.comando(name='manutenção_off',
                      aliases=['desativar_manutenção'],
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
        await ctx.send(f'Modo manutenção:\n{self.bot.configs["emojis"]["off"]}')

    @Androxus.comando(name='testes',
                      aliases=['rodar_testes', 'testar'],
                      description='Vai verificar se tudo está ok (banco de dados e funções do utils).',
                      examples=['``{prefix}testes``'],
                      perm_user='administrar a conta do bot',
                      hidden=True)
    @commands.check(permissions.is_owner)
    async def _testes(self, ctx):
        tempo_msg = Stopwatch()
        msg = await ctx.send(f'Realizando os testes {self.bot.configs["emojis"]["loading"]}')
        tempo_msg.stop()
        conexao_check = False
        banco_check = False
        testes_check = True
        testes_falhos = []
        try:
            tempo_conexao = Stopwatch()
            conexao = Conexao()
            cursor = conexao.cursor()
            tempo_conexao.stop()
            conexao_check = True
        except:
            tempo_conexao = None
            conexao = None
            cursor = None
        try:
            if conexao is not None:
                query = 'select serverId from servidor;'
                tempo_query = Stopwatch()
                cursor.execute(query)
                tempo_query.stop()
                result = [c[0] for c in cursor.fetchall()]
                conexao.fechar()
            else:
                raise Exception
        except:
            tempo_query = None
            result = None
        if result is not None:
            servers = [c.id for c in self.bot.guilds]
            if len(u.difference_between_lists(result, servers)) == 0:
                banco_check = True
        # testes das funções uteis
        # [(operação, resultado esperado)]
        testes = [
            (
                "u.capitalize(';;ABC')",
                ';;Abc'
            ),
            (
                "u.capitalize('´ABC')",
                '´Abc'
            ),
            (
                "u.capitalize('12345AB  __+=12llaksamC')",
                '12345Ab  __+=12llaksamc'
            ),
            (
                "u.capitalize('9Ç12Opa')",
                '9Ç12opa'
            ),
            (
                "u.capitalize('12É987G654U012A!')",
                '12É987g654u012a!'
            ),
            (
                "u.datetime_format(datetime(2020, 10, 21, 16, 43, 48), datetime(2020, 10, 21, 14, 42, 47))",
                'Hoje há 2 horas, 1 minuto e 1 segundo.'
            ),
            (
                "u.datetime_format(datetime(2020, 10, 21, 16, 43, 48), datetime(2020, 10, 20, 16, 23, 18))",
                'Ontem há 20 minutos e 30 segundos.'
            ),
            (
                "u.datetime_format(datetime(2020, 10, 21, 16, 43, 48), datetime(2020, 9, 10, 10, 59, 59))",
                '1 mês, 11 dias e 5 horas.'
            ),
            (
                "u.inverter_string('opa')",
                'ɐdo'
            ),
            (
                "u.inverter_string('teste1234abc')",
                'ɔqɐ4321ǝʇsǝʇ'
            ),
            (
                "u.inverter_string('áããçãóṕteste')",
                'ǝʇsǝʇṕóãçããá'
            ),
            (
                "u.is_number('123')",
                True
            ),
            (
                "u.is_number('99999a')",
                False
            ),
            (
                "u.is_number('3.1415')",
                True
            ),
            (
                "u.is_number('3.1415a')",
                False
            ),
            (
                "u.is_number('teste')",
                False
            ),
            (
                "u.convert_to_bool('SIm')",
                True
            ),
            (
                "u.convert_to_bool('sim')",
                True
            ),
            (
                "u.convert_to_bool('1')",
                True
            ),
            (
                "u.convert_to_bool('ye')",
                True
            ),
            (
                "u.convert_to_bool('aTIvo')",
                True
            ),
            (
                "u.convert_to_bool('on')",
                True
            ),
            (
                "u.convert_to_bool('yep')",
                None
            ),
            (
                "u.convert_to_bool('ava')",
                None
            ),
            (
                "u.convert_to_bool('teste')",
                None
            ),
            (
                "u.convert_to_bool('2')",
                None
            ),
            (
                "u.convert_to_bool('+-=')",
                None
            ),
            (
                "u.convert_to_bool('çç')",
                None
            ),
            (
                "u.convert_to_bool('abc')",
                None
            ),
            (
                "u.convert_to_bool('não')",
                False
            ),
            (
                "u.convert_to_bool('nao')",
                False
            ),
            (
                "u.convert_to_bool('No')",
                False
            ),
            (
                "u.convert_to_bool('0')",
                False
            ),
            (
                "u.convert_to_bool('faLse')",
                False
            ),
            (
                "u.convert_to_bool('FALSE')",
                False
            ),
            (
                "u.convert_to_bool('desaTIvo')",
                False
            ),
            (
                "u.convert_to_bool('off')",
                False
            ),
            (
                "u.convert_to_string(True)",
                'sim'
            ),
            (
                "u.convert_to_string(None)",
                'nulo'
            ),
            (
                "u.convert_to_string(False)",
                'não'
            ),
            (
                "u.string_similarity('a', 'a')",
                1.0
            ),
            (
                "u.string_similarity('a', 'ab')",
                0.5
            ),
            (
                "u.string_similarity('falei', 'falar')",
                0.6
            ),
            (
                "u.string_similarity('123', '456')",
                0.0
            ),
            (
                "u.get_most_similar_item('123', ['123', '234', '321', '679'])",
                '123'
            ),
            (
                "u.get_most_similar_item('234', ['123', '234', '321', '679'])",
                '234'
            ),
            (
                "u.get_most_similar_item('5679', ['1234', '2345', '3210', '5679'])",
                '5679'
            ),
            (
                "u.get_most_similar_item('9234', ['1234', '2345', '3210', '5679'])",
                '1234'
            ),
            (
                "u.get_most_similar_items('9234', ['1234', '2345', '3210', '5679'])",
                ['1234', '2345']
            ),
            (
                "u.get_most_similar_items('5678', ['1234', '2345', '3210', '5679'])",
                ['5679']
            ),
            (
                "u.get_most_similar_items_with_similarity('5678', ['1234', '2345', '3210', '5679'])",
                [['5679', 0.75]]
            ),
            (
                "u.get_most_similar_items_with_similarity('1243', ['1234', '2345', '3210', '5679'])",
                [['1234', 0.5]]
            ),
            (
                "u.get_most_similar_items_with_similarity('9234', ['1234', '2345', '3210', '5679'])",
                [['1234', 0.75], ['2345', 0.5]]
            ),
            (
                "u.difference_between_lists(list(range(0, 20)), list(range(0, 21)))",
                [20]
            ),
            (
                "u.difference_between_lists(['a', 'b'], ['b', 'c'])",
                ['a', 'c']
            ),
        ]

        for teste, resultado in testes:
            if eval(teste) != resultado:
                testes_check = False
                testes_falhos.append(f'Teste com erro: ```py\n{teste}```'
                                     f'Resultado esperado: `{resultado}`\n'
                                     f'Resultado obtido: `{eval(teste)}`')
        e = discord.Embed(title=f'Resultado dos testes!',
                          colour=discord.Colour(0xF5F5F5),
                          description='** **',
                          timestamp=datetime.utcnow())
        e.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        if conexao_check:
            con_emoji = self.bot.configs["emojis"]["ativado"]
            desc_con = f'Tempo para abrir conexão: `{str(tempo_conexao)}`'
        else:
            con_emoji = self.bot.configs["emojis"]["desativado"]
            desc_con = '** **'
        if banco_check:
            banco_emoji = self.bot.configs["emojis"]["ativado"]
            desc_banco = f'Tempo para executar a query: `{str(tempo_query)}`'
        else:
            banco_emoji = self.bot.configs["emojis"]["desativado"]
            desc_banco = '** **'
        if testes_check:
            testes_emoji = self.bot.configs["emojis"]["ativado"]
            desc_testes = 'Todas as funções estão retornando aquilo que deveriam estar retornando!'
        else:
            testes_emoji = self.bot.configs["emojis"]["desativado"]
            testes_falhos = '\n'.join(testes_falhos)
            desc_testes = f'{testes_falhos}'
        e.add_field(name=f'Conexão com o banco: {con_emoji}',
                    value=desc_con,
                    inline=False)
        e.add_field(name=f'Executar uma query no banco: {banco_emoji}',
                    value=desc_banco,
                    inline=False)
        e.add_field(name=f'Funções funcionando: {testes_emoji}',
                    value=desc_testes,
                    inline=False)
        e.add_field(name=f'Latências',
                    value=f'Tempo para enviar mensagem:\n'
                          f'`{str(tempo_msg)}`\n'
                          f'Ping do discord.py:\n'
                          f'`{int(self.bot.latency * 1000)}ms`',
                    inline=False)
        await msg.edit(content='', embed=e)


def setup(bot):
    bot.add_cog(OwnerOnly(bot))
