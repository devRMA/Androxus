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

    @commands.command(name='desativar_erros',
                      aliases=['desativar_tratamento_de_erro', 'erros_off'],
                      description='Vou desativar o tratamento de erros.',
                      examples=['``{prefix}erros_off``'],
                      perm_user='administrar a conta do bot',
                      cls=Androxus.Command)
    @commands.check(permissions.is_owner)
    async def _desativar_erros(self, ctx):
        self.bot.unload_extension('events.ErrorCommands')
        await ctx.send('Tratamento de erro desativado!')

    @commands.command(name='ativar_erros',
                      aliases=['ativar_tratamento_de_erro', 'erros_on'],
                      description='Vou reativar o tratamento de erros.',
                      examples=['``{prefix}erros_on``'],
                      perm_user='administrar a conta do bot',
                      cls=Androxus.Command)
    @commands.check(permissions.is_owner)
    async def _ativar_erros(self, ctx):
        self.bot.load_extension('events.ErrorCommands')
        await ctx.send('Tratamento de erro ativado!')

    @commands.command(name='game',
                      aliases=['jogar', 'status'],
                      description='Muda o meu status.',
                      parameters=['<frase>'],
                      examples=['``{prefix}game`` ``olá mundo!``', '``{prefix}game`` ``-1``'],
                      perm_user='administrar a conta do bot',
                      cls=Androxus.Command)
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

    @commands.command(name='dm',
                      aliases=['pv'],
                      hidden=True,
                      cls=Androxus.Command)
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

    @commands.command(name='kill',
                      aliases=['reboot', 'reiniciar'],
                      description='Reinicia o bot.',
                      examples=['``{prefix}reboot``'],
                      perm_user='administrar a conta do bot',
                      cls=Androxus.Command)
    @commands.check(permissions.is_owner)
    async def _kill(self, ctx):
        await ctx.send('Reiniciando <a:loading:756715436149702806>')
        await self.bot.logout()
        raise SystemExit('Rebooting...')

    @commands.command(name='sql',
                      aliases=['query', 'query_sql'],
                      description='Executa uma query sql no banco de dados.',
                      parameters=['<query sql>'],
                      examples=['``{prefix}sql`` ``select version();``'],
                      perm_user='administrar a conta do bot',
                      cls=Androxus.Command)
    @commands.check(permissions.is_owner)
    async def _sql(self, ctx, *, query=''):
        if query:
            if query[-1] != ';':
                query += ';'
            conexao = Conexao()
            cursor = conexao.cursor()
            modo = 'i'
            try:
                cursor.execute(query)
            except Exception as e:
                conexao.fechar()
                return await ctx.send(f'Erro ```{str(e)}``` ao executar a query!')
            if 'select' in query.lower():
                modo = 's'
            if modo == 'i':
                conexao.salvar()
                await ctx.send(f'Query:```sql\n{query}```Executado com sucesso!')
            if modo == 's':
                await ctx.send(f'Query:```sql\n{query}```Resultado:```python\n{cursor.fetchall()}```')
            conexao.fechar()
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

    @commands.command(name='eval',
                      aliases=['ev'],
                      description='Executa um script em python.',
                      parameters=['<script>'],
                      examples=['``{prefix}eval`` ``return \'opa\'``'],
                      perm_user='administrar a conta do bot',
                      cls=Androxus.Command)
    @commands.check(permissions.is_owner)
    async def _eval(self, ctx, *, cmd):
        execution_time = Stopwatch()
        msg_bot = None

        def check(reaction, user):
            author = user.id == ctx.author.id
            reactions = (str(reaction.emoji) == '<a:desativado:755774682397147226>') or (
                    str(reaction.emoji) == '<a:ativado:755774682334101615>')
            message_check = reaction.message == msg_bot
            return author and reactions and message_check

        closed = discord.Embed(title=f'Eval fechada <a:check:755775267275931799>',
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
            erro = discord.Embed(title=f'<a:atencao:755844029333110815> Erro no comando eval',
                                 colour=discord.Colour(0xff6961),
                                 description='** **',
                                 timestamp=datetime.utcnow())
            erro.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            erro.add_field(name='📥 Input',
                           value=f'```py\n{execute_cmd}```',
                           inline=False)
            e = [f'- {c}' for c in str(e).splitlines()]
            e = '\n'.join(e)
            erro.add_field(name='<:warning:765612208629219358> Erro',
                           value=f'```diff\n{e}```',
                           inline=False)
            msg_bot = await ctx.send(embed=erro)
            await msg_bot.add_reaction(self.bot.get_emoji(755774682334101615))
            try:
                await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                pass
            except asyncio.TimeoutError:
                pass
            await msg_bot.remove_reaction(self.bot.get_emoji(755774682334101615), ctx.me)
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
        await msg_bot.add_reaction(self.bot.get_emoji(755774682397147226))
        await msg_bot.add_reaction(self.bot.get_emoji(755774682334101615))
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
            if str(reaction.emoji) == '<a:desativado:755774682397147226>':
                await msg_bot.edit(embed=closed)
            elif str(reaction.emoji) == '<a:ativado:755774682334101615>':
                e.remove_field(-1)
                await msg_bot.edit(embed=e)
        except asyncio.TimeoutError:
            await msg_bot.edit(embed=closed)
        await msg_bot.remove_reaction(self.bot.get_emoji(755774682397147226), ctx.me)
        await msg_bot.remove_reaction(self.bot.get_emoji(755774682334101615), ctx.me)

    @commands.command(name='blacklist',
                      aliases=['blacklisted', 'banido'],
                      hidden=True,
                      cls=Androxus.Command)
    @commands.check(permissions.is_owner)
    async def _blacklist(self, ctx, *args):
        conexao = Conexao()
        if ctx.message.mentions:
            user_id = ctx.message.mentions[0].id
        else:
            user_id = int(args[0])
        blacklisted = BlacklistRepository().get_pessoa(conexao, user_id)
        conexao.fechar()
        if not blacklisted[0]:
            msg = f'A pessoa pode usar meus comandos! {get_emoji_dance()}'
        else:
            msg = f'<a:no_no:755774680325029889> Esse usuário foi banido de me usar!' + \
                  f'\nMotivo: `{blacklisted[1]}`\nQuando: {datetime_format(blacklisted[-1])}'
        return await ctx.send(msg)

    @commands.command(name='add_blacklist',
                      aliases=['ab'],
                      hidden=True,
                      cls=Androxus.Command)
    @commands.check(permissions.is_owner)
    async def _add_blacklist(self, ctx, *args):
        conexao = Conexao()
        if ctx.message.mentions:
            user_id = ctx.message.mentions[0].id
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
        return await ctx.send('Este usuário não vai poder usar meus comandos! <a:banned:756138595882107002>'
                              f'\nCom o motivo: {motivo}')

    @commands.command(name='remove_blacklist',
                      aliases=['rb', 'whitelist'],
                      hidden=True,
                      cls=Androxus.Command)
    @commands.check(permissions.is_owner)
    async def _remove_blacklist(self, ctx, *args):
        conexao = Conexao()
        if ctx.message.mentions:
            user_id = ctx.message.mentions[0].id
        else:
            user_id = int(args[0])
        BlacklistRepository().delete(conexao, user_id)
        conexao.fechar()
        return await ctx.send(f'Usuário perdoado! {get_emoji_dance()}')

    @commands.command(name='manutenção_on',
                      aliases=['ativar_manutenção'],
                      description='Ativa o modo "em manutenção" do bot.',
                      examples=['``{prefix}manutenção_on``',
                                '``{prefix}ativar_manutenção``'],
                      perm_user='administrar a conta do bot',
                      cls=Androxus.Command)
    @commands.check(permissions.is_owner)
    async def _manutencao_on(self, ctx):
        self.bot.maintenance_mode = True
        self.bot.mudar_status = False
        await self.bot.change_presence(activity=discord.Game(name='Em manutenção!'))
        self.bot.unload_extension('events.ErrorCommands')
        await ctx.send('Modo manutenção:\n<a:on:755774680580882562>')

    @commands.command(name='manutenção_off',
                      aliases=['desativar_manutenção'],
                      description='Desativa o modo "em manutenção" do bot.',
                      examples=['``{prefix}manutenção_off``',
                                '``{prefix}desativar_manutenção``'],
                      perm_user='administrar a conta do bot',
                      cls=Androxus.Command)
    @commands.check(permissions.is_owner)
    async def _manutencao_off(self, ctx):
        self.bot.maintenance_mode = False
        self.bot.mudar_status = True
        self.bot.load_extension('events.ErrorCommands')
        await ctx.send('Modo manutenção:\n<a:off:755774680660574268>')


def setup(bot):
    bot.add_cog(OwnerOnly(bot))
