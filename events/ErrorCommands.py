# -*- coding: utf-8 -*-
# Androxus bot
# ErrorCommands.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands import errors

from Classes.erros import *
from utils import permissions


class ErrorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # source: https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612

        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = ()

        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return
        elif isinstance(error, errors.NotOwner):
            return await ctx.send(f'{ctx.author.mention} você não é meu criador {self.bot.emoji("no_no")}')
        elif isinstance(error, errors.MissingRequiredArgument):
            return await self.bot.send_help(ctx)
        elif isinstance(error, MultipleResults):
            embed = discord.Embed(title='Encontrei mais de um resultado!',
                                  colour=discord.Colour.random(),
                                  timestamp=datetime.utcnow())
            results = error.results
            if len(results) >= 5:
                msg = '\n'.join(f'{u} (ID: {u.id})' for u in results[:5])
                msg += f'\nE outro(s) {len(results) - 5} resultado(s)...'
            else:
                msg = '\n'.join(f'{u} (ID: {u.id})' for u in results)
            embed.add_field(name=msg,
                            value='** **')
            return await ctx.send(embed=embed)
        elif isinstance(error, errors.MaxConcurrencyReached):
            try:
                # vai ver se é o dono
                permissions.is_owner(ctx)
                # se for, usa o comando
                await ctx.command.reinvoke(ctx)
            except errors.NotOwner:  # se não for, dispara o erro
                return await ctx.send(f'Calma lá {ctx.author.mention}! Você só pode usar 1 comando por vez! Se o '
                                      'comando possuir páginas, pare o sistema de paginação, antes de usar o '
                                      'comando de novo!')
        elif isinstance(error, errors.NoPrivateMessage):
            return await ctx.send(
                f'{ctx.author.mention} Este comando só pode ser usado num servidor! {self.bot.emoji("atencao")}')
        elif isinstance(error, errors.BotMissingPermissions):
            if len(error.missing_perms) == 1:
                permissoes = error.missing_perms[0]
            else:
                permissoes = ', '.join(error.missing_perms)
            return await ctx.send(
                f'{ctx.author.mention} Eu não posso executar este comando, pois não tenho permissão de ' +
                f'``{permissoes}`` neste servidor! {self.bot.emoji("sad")}')
        elif isinstance(error, errors.CheckFailure):
            return await ctx.send(f'{ctx.author.mention} Você precisa ter permissão de `{ctx.command.perm_user}`'
                                  ' para usar este comando! ')
        elif isinstance(error, Forbidden):
            if not permissions.can_embed(ctx):
                if ctx.author.permissions_in(ctx.message.channel).administrator:
                    msg = 'Por favor, me dê permissão de "inserir links", para que eu possa mostrar minhas mensagens.'
                else:
                    msg = 'Por favor, peça para um administrador do servidor me dar permissão de "inserir links",' \
                          ' para que eu possa mostrar minhas mensagens.'
                return await ctx.send(msg)
            if not permissions.can_upload(ctx):
                if ctx.author.permissions_in(ctx.message.channel).administrator:
                    msg = 'Por favor, me dê permissão de "anexar arquivos", para que eu possa funcionar corretamente.'
                else:
                    msg = 'Por favor, peça para um administrador do servidor me dar permissão de "anexar arquivos",' \
                          ' para que eu possa funcionar corretamente.'
                return await ctx.send(msg)
            if not permissions.can_react(ctx):
                if ctx.author.permissions_in(ctx.message.channel).administrator:
                    msg = 'Por favor, me dê permissão de "adicionar reações", para que eu possa funcionar corretamente.'
                else:
                    msg = 'Por favor, peça para um administrador do servidor me dar permissão de "adicionar reações",' \
                          ' para que eu possa funcionar corretamente.'
                return await ctx.send(msg)
            await ctx.send(f'{ctx.author.mention} eu não tenho permissão para executar esse comando, acho que algum' +
                           ' administrador deve ter tirado minhas permissões! Com o comando ``invite``você consegue ' +
                           'ter o link para me adicionar com todas as permissões.')
        elif isinstance(error, errors.BadArgument):
            if str(error).startswith('Member') and str(error).endswith('not found'):
                return await ctx.send(f'{ctx.author.mention} não consegui encontrar esse membro.')
            elif str(error) == 'Esse id não está banido!':
                return await ctx.send(
                    f'{ctx.author.mention} não consegui encontrar um membro banido, com este id: `{error.id}`.')
            elif str(error) == 'Esse membro não está banido!':
                return await ctx.send(f'{ctx.author.mention} não consegui encontrar o usuário `{error.member}` na lista'
                                      f' de banidos. Teste usar o comando com aspas entre o nome do usuário caso ele'
                                      f' tenha um nome com espaços, assim:\n'
                                      f'`unban "{error.member} nome legal que o cara tem"`')
            elif str(error) == 'Membro mencionado não está banido!':
                return await ctx.send(
                    f'{ctx.author.mention} não consegui encontrar o membro {error.user.mention} na lista de bans.')
        elif isinstance(error, errors.CommandOnCooldown):
            try:
                # vai ver se é o dono
                permissions.is_owner(ctx)
                # se for, usa o comando
                await ctx.command.reinvoke(ctx)
            except errors.NotOwner:  # se não for, dispara o erro
                await ctx.send(f'Calma lá {ctx.author.mention}, você está usando meus comandos muito rápido!\n' +
                               f'Tente novamente em {error.retry_after:.2f} segundos.')
        elif isinstance(error, DuplicateBlacklist):
            await ctx.send(
                f'{self.bot.emoji("atencao")} {ctx.author.mention} Essa pessoa já está na blacklist!')
        elif isinstance(error, DuplicateComandoDesativado):
            await ctx.send(
                f'{self.bot.emoji("atencao")} {ctx.author.mention} Esse comando já está desativado!')
        elif isinstance(error, ComandoDesativadoNotFound):
            await ctx.send(
                f'{self.bot.emoji("atencao")} {ctx.author.mention} Esse comando já está ativado!')
        elif isinstance(error, DuplicateComandoPersonalizado):
            await ctx.send(
                f'{self.bot.emoji("atencao")} {ctx.author.mention} Esse comando já está cadastrado!')
        elif isinstance(error, DuplicateServidor):
            pass
        else:
            try:
                return await ctx.send(
                    f'Ocorreu o erro:```py\n{error}```Na execução do comando ```{ctx.message.content}```'
                    f'{self.bot.emoji("sad")}')
            except:
                print(f'Ocorreu o erro: {error}\nNa execução do comando {ctx.message.content}')


def setup(bot):
    """

    Args:
        bot (Classes.Androxus.Androxus): Instância do bot

    """
    bot.add_cog(ErrorCommands(bot))
