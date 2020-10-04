# coding=utf-8
# Androxus bot
# ErrorCommands.py

__author__ = 'Rafael'

from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands import errors

from discord_bot.utils import permissions


class ErrorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # font: https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound,)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return
        elif isinstance(error, errors.NotOwner):
            await ctx.send(f'{ctx.author.mention} você não é meu criador <a:no_no:755774680325029889>')
        elif isinstance(error, errors.NoPrivateMessage):
            await ctx.send(
                f'{ctx.author.mention} Este comando só pode ser usado num servidor! <a:atencao:755844029333110815>')
        elif isinstance(error, errors.MissingPermissions):
            if len(error.missing_perms) == 1:
                permissoes = error.missing_perms[0]
            else:
                permissoes = ', '.join(error.missing_perms)
            await ctx.send(
                f'{ctx.author.mention} Você precisa ter permissão de ``{permissoes}`` para usar este comando!')
        elif isinstance(error, errors.BotMissingPermissions):
            if len(error.missing_perms) == 1:
                permissoes = error.missing_perms[0]
            else:
                permissoes = ', '.join(error.missing_perms)
            await ctx.send(f'{ctx.author.mention} Eu não posso executar este comando, pois não tenho permissão de ' +
                           f'``{permissoes}`` neste servidor! <a:sad:755774681008832623>')
        elif isinstance(error, errors.CheckFailure):
            await ctx.send(f'{ctx.author.mention} você não tem permissão para usar este comando!\nDigite ' +
                           f'`{ctx.prefix}help {ctx.command}` para ver quais permissões você precisa ter!')
        elif isinstance(error, Forbidden):
            if not permissions.can_embed(ctx):
                if ctx.author.permissions_in(ctx.message.channel).administrator:
                    msg = 'Por favor, me dê permissão de "inserir links", para que eu possa mostrar minhas mensagens ;-;'
                else:
                    msg = 'Por favor, peça para um administrador do servidor me dar permissão de "inserir links",' \
                          ' para que eu possa mostrar minhas mensagens ;-;'
                return await ctx.send(msg)
            if not permissions.can_upload(ctx):
                if ctx.author.permissions_in(ctx.message.channel).administrator:
                    msg = 'Por favor, me dê permissão de "anexar arquivos", para que eu possa funcionar corretamente ;-;'
                else:
                    msg = 'Por favor, peça para um administrador do servidor me dar permissão de "anexar arquivos",' \
                          ' para que eu possa funcionar corretamente ;-;'
                return await ctx.send(msg)
            if not permissions.can_react(ctx):
                if ctx.author.permissions_in(ctx.message.channel).administrator:
                    msg = 'Por favor, me dê permissão de "adicionar reações", para que eu possa funcionar corretamente ;-;'
                else:
                    msg = 'Por favor, peça para um administrador do servidor me dar permissão de "adicionar reações",' \
                          ' para que eu possa funcionar corretamente ;-;'
                return await ctx.send(msg)
            await ctx.send(f'{ctx.author.mention} eu não tenho permissão para executar esse comando, acho que algum' +
                           ' administrador deve ter tirado minhas permissões! Com o comando ``invite``você consegue ' +
                           'ter o link para me adicionar')
        elif isinstance(error, errors.BadArgument):
            if str(error).startswith('Member') and str(error).endswith('not found'):
                await ctx.send(f'{ctx.author.mention} não consegui encontrar esse membro.')
            elif str(error) == 'Esse id não está banido!':
                await ctx.send(
                    f'{ctx.author.mention} não consegui encontrar um membro banido, com este id: `{error.id}`.')
            elif str(error) == 'Esse membro não está banido!':
                await ctx.send(f'{ctx.author.mention} não consegui encontrar o membro banido `{error.member}`.')
            elif str(error) == 'Membro mencionado não está banido!':
                await ctx.send(
                    f'{ctx.author.mention} não consegui encontrar o membro {error.user.mention} na lista de bans.')
        else:
            if str(error).startswith('duplicate servidor'):
                pass
            elif str(error).startswith('duplicate comando desativado'):
                await ctx.send(f'<a:atencao:755844029333110815> {ctx.author.mention} Esse comando já está desativado!')
            elif str(error).startswith('Este comando já está ativo!'):
                await ctx.send(f'<a:atencao:755844029333110815> {ctx.author.mention} Esse comando já está ativado!')
            elif str(error).startswith('blacklisted'):
                await ctx.send(f'<a:atencao:755844029333110815> {ctx.author.mention} Essa pessoa já está na blacklist!')
            elif str(error).startswith('comando personalizado duplicado'):
                await ctx.send(f'<a:atencao:755844029333110815> {ctx.author.mention} Esse comando já está cadastrado!')
            else:
                try:
                    await ctx.send(
                        f'Ocorreu o erro:```{error}```\nNa execução do comando ```{ctx.message.content}```\n<a:sad:755774681008832623>')
                except:
                    print(f'Ocorreu o erro: {error}\nNa execução do comando {ctx.message.content}')


def setup(bot):
    bot.add_cog(ErrorCommands(bot))
