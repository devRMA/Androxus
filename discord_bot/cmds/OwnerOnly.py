# coding=utf-8
# Androxus bot
# OwnerOnly.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.ext import commands

from discord_bot.database.Conexao import Conexao
from discord_bot.utils import permissions
from discord_bot.utils.Utils import get_emoji_dance, random_color


class OwnerOnly(commands.Cog):
    # algumas outras funções que só o dono do bot pode usar
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['desativar_tratamento_de_erro', 'erros_off'], hidden=True)
    @commands.check(permissions.is_owner)
    async def desativar_erros(self, ctx):
        self.bot.unload_extension('events.ErrorCommands')
        await ctx.send('Tratamento de erro desativado!')

    @commands.command(aliases=['ativar_tratamento_de_erro', 'erros_on'], hidden=True)
    @commands.check(permissions.is_owner)
    async def ativar_erros(self, ctx):
        self.bot.load_extension('events.ErrorCommands')
        await ctx.send('Tratamento de erro ativado!')

    @commands.command(aliases=['jogar', 'status'], hidden=True)
    @commands.check(permissions.is_owner)
    async def game(self, ctx, *args):
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
            await self.bot.change_presence(activity=discord.Game(name=" ".join(args)))
            embed = discord.Embed(title=f'Status alterado!',
                                  colour=discord.Colour(random_color()),
                                  description=f'Agora eu estou jogando ``{" ".join(args)}``',
                                  timestamp=datetime.utcnow())
            embed.set_author(name='Androxus', icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pv'], hidden=True)
    @commands.check(permissions.is_owner)
    async def dm(self, ctx, id: int, *args):
        user = self.bot.get_user(id)
        if user is not None:
            if ctx.guild.id != 405826835793051649:
                try:
                    await ctx.message.delete()
                except discord.errors.Forbidden:
                    pass
            user_dm_criado = user.dm_channel
            try:
                if user_dm_criado != None:
                    await user_dm_criado.send(" ".join(args))
                else:
                    await user.create_dm()
                    await user.dm_channel.send(" ".join(args))
                foi = True
            except discord.errors.Forbidden:
                foi = False
            try:
                if foi and ctx.guild.id == 405826835793051649:
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

    @commands.command(aliases=['reboot', 'reiniciar'], hidden=True)
    @commands.check(permissions.is_owner)
    async def kill(self, ctx):
        await ctx.send('Reiniciando <a:loading:756715436149702806>')
        raise SystemExit('Rebooting...')

    @commands.command(aliases=['query', 'query_sql'], hidden=True)
    @commands.check(permissions.is_owner)
    async def sql(self, ctx, *args):
        if args:
            query = ' '.join(args)
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



def setup(bot):
    bot.add_cog(OwnerOnly(bot))
