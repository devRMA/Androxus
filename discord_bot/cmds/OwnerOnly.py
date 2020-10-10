# coding=utf-8
# Androxus bot
# OwnerOnly.py

__author__ = 'Rafael'

import ast
from datetime import datetime

import discord
from discord.ext import commands
from stopwatch import Stopwatch

from discord_bot.Classes import Androxus
from discord_bot.database.ComandoDesativado import ComandoDesativado
from discord_bot.database.ComandoPersonalizado import ComandoPersonalizado
from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.BlacklistRepository import BlacklistRepository
from discord_bot.database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from discord_bot.database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from discord_bot.database.Repositories.InformacoesRepository import InformacoesRepository
from discord_bot.database.Repositories.ServidorRepository import ServidorRepository
from discord_bot.database.Servidor import Servidor
from discord_bot.utils import Utils as u
from discord_bot.utils import permissions
from discord_bot.utils.Utils import get_emoji_dance, random_color


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
    async def _dm(self, ctx, user_id: int, *args):
        user = self.bot.get_user(user_id)
        if user is not None:
            foi = False
            if ctx.guild.id != 405826835793051649:
                try:
                    await ctx.message.delete()
                except discord.errors.Forbidden:
                    pass
            try:
                await user.send(' '.join(args))
                foi = True
            except discord.errors.Forbidden:
                pass
            try:
                if foi and (ctx.guild.id == 405826835793051649):
                    embed = discord.Embed(title=f'Mensagem enviada no privado do(a) {str(user)}!',
                                          colour=discord.Colour(random_color()),
                                          description=f'{" ".join(args)}',
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
                      description='Executa um script em python (com retorno).',
                      parameters=['<script>'],
                      examples=['``{prefix}eval`` ``return \'opa\'``'],
                      perm_user='administrar a conta do bot',
                      cls=Androxus.Command)
    @commands.check(permissions.is_owner)
    async def _eval(self, ctx, *, cmd):
        execution_time = Stopwatch()
        fn_name = '_eval_expr'
        cmd = cmd.strip('` ')
        # add a layer of indentation
        cmd = '\n'.join(f'    {i}' for i in cmd.splitlines())
        # wrap in async def body
        body = f'async def {fn_name}():\n{cmd}'
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
            'Stopwatch': Stopwatch,
            'ctx': ctx,
            '__import__': __import__
        }
        try:
            exec(compile(parsed, filename='<ast>', mode='exec'), env)
            result = (await eval(f'{fn_name}()', env))
        except Exception as e:
            execution_time.stop()
            return await ctx.send(
                f'Ocorreu o erro ```{e}``` na hora de executar o comando ```py\nasync def {fn_name}():\n{cmd}```')
        if result != 'nada':
            execution_time.stop()
            return await ctx.send(f'Resultado:```{result}```Tipo do return:```{type(result)}```Tempo de execução: '
                                  f'``{str(execution_time)}``')

    @commands.command(name='exec',
                      aliases=['execute'],
                      description='Executa um script em python (sem retorno).',
                      parameters=['<script>'],
                      examples=['``{prefix}exec`` ``def opa():\\n\\tprint(\'opa\')``'],
                      perm_user='administrar a conta do bot',
                      cls=Androxus.Command)
    @commands.check(permissions.is_owner)
    async def _exec(self, ctx, *, cmd):
        env = {
            'discord': discord,
            'commands': commands,
            'permissions': permissions,
            'Androxus': Androxus
        }
        try:
            exec(cmd, env)
        except Exception as e:
            return await ctx.send(f'Ocorreu um erro na execução do comando```py\n{cmd}```Erro:```{e}```.')
        else:
            return await ctx.send(f'Comando```py\n{cmd}```executado com sucesso!')

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
        if not BlacklistRepository().get_pessoa(conexao, user_id):
            msg = f'A pessoa pode usar meus comandos! {get_emoji_dance()}'
        else:
            msg = f'<a:no_no:755774680325029889> Essa pessoa não usar meus comandos!'
        conexao.fechar()
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
        else:
            user_id = int(args[0])
        BlacklistRepository().create(conexao, user_id)
        conexao.fechar()
        return await ctx.send('Este usuário não vai poder usar meus comandos! <a:banned:756138595882107002>')

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
        await ctx.send('Modo manutenção:\n<a:off:755774680660574268>')


def setup(bot):
    bot.add_cog(OwnerOnly(bot))
