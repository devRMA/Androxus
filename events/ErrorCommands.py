# coding=utf-8
# Androxus bot
# ErrorCommands.py

__author__ = 'Rafael'

from string import ascii_letters

from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands import errors

from database.Conexao import Conexao
from database.Repositories.ServidorRepository import ServidorRepository
from modelos.embedHelpCategory import embedHelpCategory
from utils import permissions
from utils.Utils import string_similarity, get_most_similar_item


class ErrorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # source: https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = ()

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            # Anything in ignored will return and prevent anything happening.
            return
        elif isinstance(error, errors.CommandNotFound):
            # vai pegar toda a mensagem, depois do prefixo
            comando = ctx.message.content.lower()[len(ctx.prefix):]
            # se o primeiro caracter da mensagem, não for uma letra
            if comando[0] not in ascii_letters:
                # não vai fazer nada
                return
            comando = comando.split(' ')[0]
            mostrar_erro = False
            if ctx.guild:
                conexao = Conexao()
                servidor = ServidorRepository().get_servidor(conexao, ctx.guild.id)
                conexao.fechar()
                if servidor.sugestao_de_comando:
                    mostrar_erro = True
                else:
                    mostrar_erro = False
            commands = []
            for command in self.bot.get_all_commands():
                if comando.lower() == command.category:
                    e = embedHelpCategory(self.bot, ctx, comando)
                    return await ctx.send(embed=e)
                commands.append(command.name)
                commands.append(command.category)
                for alias in command.aliases:
                    commands.append(alias)
            if mostrar_erro:
                msg = f'{ctx.author.mention} {self.bot.configs["emojis"]["sad"]} eu não achei consegui ' \
                      f'achar o comando "{comando}".'
                sugestao = get_most_similar_item(comando, commands)
                if sugestao:
                    # se a sugestão for pelo menos 50% semelhante ao comando
                    if string_similarity(comando, sugestao) >= 0.6:
                        msg += f'\nVocê quis dizer ``{sugestao}``?'
                msg += f'\nPara desativar esta mensagem, use o comando ``desativar_sugestão``'
                return await ctx.send(msg, delete_after=10)
        elif isinstance(error, errors.NotOwner):
            return await ctx.send(f'{ctx.author.mention} você não é meu criador {self.bot.configs["emojis"]["no_no"]}')
        elif isinstance(error, errors.MissingRequiredArgument):
            return await self.bot.send_help(ctx)
        elif isinstance(error, errors.MaxConcurrencyReached):
            return await ctx.send(f'Calma lá {ctx.author.mention}! Você só pode usar 1 comando por vez!')
        elif isinstance(error, errors.NoPrivateMessage):
            return await ctx.send(
                f'{ctx.author.mention} Este comando só pode ser usado num servidor! {self.bot.configs["emojis"]["atencao"]}')
        elif isinstance(error, errors.MissingPermissions):
            if len(error.missing_perms) == 1:
                permissoes = error.missing_perms[0]
            else:
                permissoes = ', '.join(error.missing_perms)
            return await ctx.send(
                f'{ctx.author.mention} Você precisa ter permissão de ``{permissoes}`` para usar este comando!')
        elif isinstance(error, errors.BotMissingPermissions):
            if len(error.missing_perms) == 1:
                permissoes = error.missing_perms[0]
            else:
                permissoes = ', '.join(error.missing_perms)
            return await ctx.send(
                f'{ctx.author.mention} Eu não posso executar este comando, pois não tenho permissão de ' +
                f'``{permissoes}`` neste servidor! {self.bot.configs["emojis"]["sad"]}')
        elif isinstance(error, errors.CheckFailure):
            return await ctx.send(f'{ctx.author.mention} você não tem permissão para usar este comando!\nDigite ' +
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
                return await ctx.send(f'{ctx.author.mention} não consegui encontrar esse membro.')
            elif str(error) == 'Esse id não está banido!':
                return await ctx.send(
                    f'{ctx.author.mention} não consegui encontrar um membro banido, com este id: `{error.id}`.')
            elif str(error) == 'Esse membro não está banido!':
                return await ctx.send(f'{ctx.author.mention} não consegui encontrar o membro banido `{error.member}`.')
            elif str(error) == 'Membro mencionado não está banido!':
                return await ctx.send(
                    f'{ctx.author.mention} não consegui encontrar o membro {error.user.mention} na lista de bans.')
        elif isinstance(error, errors.CommandOnCooldown):
            await ctx.send(f'Calma lá {ctx.author.mention}, você está usando meus comandos muito rápido!\n' +
                           f'Tente novamente em {error.retry_after:.2f} segundos.')
        else:
            if str(error).startswith('duplicate servidor'):
                pass
            elif str(error).startswith('duplicate comando desativado'):
                return await ctx.send(
                    f'{self.bot.configs["emojis"]["atencao"]} {ctx.author.mention} Esse comando já está desativado!')
            elif str(error).startswith('Este comando já está ativo!'):
                return await ctx.send(
                    f'{self.bot.configs["emojis"]["atencao"]} {ctx.author.mention} Esse comando já está ativado!')
            elif str(error).startswith('blacklisted'):
                return await ctx.send(
                    f'{self.bot.configs["emojis"]["atencao"]} {ctx.author.mention} Essa pessoa já está na blacklist!')
            elif str(error).startswith('comando personalizado duplicado'):
                return await ctx.send(
                    f'{self.bot.configs["emojis"]["atencao"]} {ctx.author.mention} Esse comando já está cadastrado!')
            else:
                try:
                    return await ctx.send(
                        f'Ocorreu o erro:```py\n{error}```Na execução do comando ```{ctx.message.content}```'
                        f'{self.bot.configs["emojis"]["sad"]}')
                except:
                    print(f'Ocorreu o erro: {error}\nNa execução do comando {ctx.message.content}')


def setup(bot):
    bot.add_cog(ErrorCommands(bot))
