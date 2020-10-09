# coding=utf-8
# Androxus bot
# Admin.py

__author__ = 'Rafael'

import asyncio
from datetime import datetime

import discord
from discord.ext import commands

from discord_bot.Classes import Androxus
from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.ServidorRepository import ServidorRepository
from discord_bot.database.Servidor import Servidor
from discord_bot.utils import permissions
from discord_bot.utils.Utils import random_color, get_emoji_dance, get_configs, pegar_o_prefixo, convert_to_string, \
    convert_to_bool


# font: https://github.com/Rapptz/RoboDanny
class BannedMember(commands.Converter):
    async def convert(self, ctx, argument):
        if argument:
            if ctx.message.mentions:
                try:
                    return await ctx.guild.fetch_ban(discord.Object(id=ctx.message.mentions[0].id))
                except discord.NotFound:
                    erro = commands.BadArgument('Membro mencionado não está banido!')
                    erro.user = ctx.message.mentions[0]
                    raise erro
            if argument.isdigit():
                member_id = int(argument, base=10)
                try:
                    return await ctx.guild.fetch_ban(discord.Object(id=member_id))
                except discord.NotFound:
                    erro = commands.BadArgument('Esse id não está banido!')
                    erro.id = member_id
                    raise erro

            ban_list = await ctx.guild.bans()
            entity = discord.utils.find(lambda u: str(u.user) == argument, ban_list)

            if entity is None:
                erro = commands.BadArgument('Esse membro não está banido!')
                erro.member = argument
                raise erro
            return entity
        else:
            return None


class Admin(commands.Cog, command_attrs=dict(category='administração')):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ban',
                      aliases=['banir'],
                      description='Vou banir algum membro.',
                      parameters=['<membro do servidor>', '[motivo (padrão: Nulo)]'],
                      examples=['``{prefix}ban`` ``@membro#1234`` ``ofendeu membro``',
                                '``{prefix}banir`` {author_mention}'],
                      perm_user='banir membros',
                      perm_bot='banir membros',
                      cls=Androxus.Command)
    @permissions.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def _ban(self, ctx, member: discord.Member = None, *args):
        async with ctx.typing():  # vai aparecer "bot está digitando"
            if isinstance(args, tuple):
                # se chegar como tupla, vai transformar em lista
                args = list(args)
            # se a pessoa passou pelo menos o membro, ou algum argumento
            if args or member:
                if not member:  # se o membro não foi marcado
                    # vai ver se a pessoa passou um id
                    try:
                        # vai tentar converter para int, o primeiro valor que a pessoa passou
                        id = int(args[0])
                    except ValueError:
                        # se não conseguir:
                        return await self.bot.send_help(ctx)
                    else:
                        # se não entrou no except
                        args.pop(0)
                    # vai tentar achar o membro com esse id
                    try:
                        member = await ctx.guild.fetch_member(id)
                    except:
                        member = None
                    if member is None:  # se não achou o membro:
                        return await ctx.send(f'Não consegui encontrar o membro com id `{id}`!')
                # vai verificar se a pessoa pode usar o comando
                if ctx.guild.owner == member:
                    return await ctx.send(f'{ctx.author.mention} você não pode banir o dono do servidor! ' +
                                          '<:ah_nao:758003636822474887>')
                elif member == ctx.author:
                    return await ctx.send(f'{ctx.author.mention} você não pode se banir! ' +
                                          '<:ah_nao:758003636822474887>')
                elif member == self.bot.user:
                    return await ctx.send(f'{ctx.author.mention} eu não posso me banir! ' +
                                          '<:ah_nao:758003636822474887>')
                elif ctx.author.id in get_configs()['owners'] or ctx.author == ctx.guild.owner:
                    pass  # se for o dono do bot, ou dono do servidor, vai ignorar as próxima verificação
                elif ctx.author.top_role <= member.top_role:
                    return await ctx.send(f'{ctx.author.mention} você só pode banir pessoas que tenham cargo mais ' +
                                          'baixo que o seu!')
                # se sobrou algum argumento, é porque a pessoa passou um motivo
                reason = None
                if args:
                    reason = ' '.join(args)
            else:
                # se a pessoa não passou nada:
                return await self.bot.send_help(ctx)
            embed = discord.Embed(title=f'<a:banned:756138595882107002> Usuário banido!',
                                  colour=discord.Colour(random_color()),
                                  description=f'Usuário: {member}\nId: {member.id}\nMotivo: ' +
                                              f'{str(reason).replace("None", "nulo")}',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=str(ctx.author),
                             icon_url=ctx.author.avatar_url)
            msg_ban = f'{ctx.author.mention} Você foi banido do servidor {ctx.guild}!'
            if reason:
                msg_ban += f'\nPelo motivo: {reason}'
        try:
            if not member.bot:
                msg = await member.send(msg_ban)
        except:
            pass
        reason = f'Banido por: {ctx.author} —— Motivo: {str(reason).replace("None", "nulo")}'
        try:
            await ctx.guild.ban(member, reason=reason)
        except discord.errors.Forbidden:
            try:
                await msg.delete()
            except:
                pass
            await ctx.send('Eu não tenho permissão para banir este usuário. <a:sad:755774681008832623>')
        else:
            await ctx.send(embed=embed)

    @commands.command(name='kick',
                      aliases=['expulsar'],
                      description='Vou expulsar algum membro.',
                      parameters=['<membro do servidor>', '[motivo (padrão: Nulo)]'],
                      examples=['``{prefix}kick`` ``@membro#1234`` ``não quero você aqui!``',
                                '``{prefix}expulsar`` {author_mention}'],
                      perm_user='expulsar membros',
                      perm_bot='expulsar membros',
                      cls=Androxus.Command)
    @permissions.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.guild_only()
    async def _kick(self, ctx, member: discord.Member = None, *args):
        async with ctx.typing():  # vai aparecer "bot está digitando"
            if isinstance(args, tuple):
                # se chegar como tupla, vai transformar em lista
                args = list(args)
            # se a pessoa passou pelo menos o membro, ou algum argumento
            if args or member:
                if not member:  # se o membro não foi marcado
                    # vai ver se a pessoa passou um id
                    try:
                        # vai tentar converter para int, o primeiro valor que a pessoa passou
                        id = int(args[0])
                    except ValueError:
                        # se não conseguir:
                        return await self.bot.send_help(ctx)
                    else:
                        # se não entrou no except
                        args.pop(0)
                    # vai tentar achar o membro com esse id
                    member = ctx.guild.get_member(id)
                    if not member:  # se não achou o membro:
                        return await ctx.send(f'Não consegui encontrar o membro com id `{id}`!')
                # vai verificar se a pessoa pode usar o comando
                if ctx.guild.owner == member:
                    return await ctx.send(f'{ctx.author.mention} você não pode expulsar o dono do servidor! ' +
                                          '<:ah_nao:758003636822474887>')
                elif member == ctx.author:
                    return await ctx.send(f'{ctx.author.mention} você não pode se expulsar! ' +
                                          '<:ah_nao:758003636822474887>')
                elif member == self.bot.user:
                    return await ctx.send(f'{ctx.author.mention} eu não posso me expulsar! ' +
                                          '<:ah_nao:758003636822474887>')
                elif ctx.author.id in get_configs()['owners'] or ctx.author == ctx.guild.owner:
                    pass  # se for o dono do bot, ou dono do servidor, vai ignorar as próxima verificação
                elif ctx.author.top_role <= member.top_role:
                    return await ctx.send(f'{ctx.author.mention} você só pode expulsar pessoas que tenham cargo mais ' +
                                          'baixo que o seu!')
                # se sobrou algum argumento, é porque a pessoa passou um motivo
                reason = None
                if args:
                    reason = ' '.join(args)
            else:
                # se a pessoa não passou nada:
                return await self.bot.send_help(ctx)
            embed = discord.Embed(title=f'Usuário expulso!',
                                  colour=discord.Colour(random_color()),
                                  description=f'Usuário: {member}\nId: {member.id}\nMotivo: ' +
                                              f'{str(reason).replace("None", "nulo")}',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=str(ctx.author),
                             icon_url=ctx.author.avatar_url)
            msg_kick = f'{ctx.author.mention} Você foi expulso do servidor {ctx.guild}!'
            if reason:
                msg_kick += f'\nPelo motivo: {reason}'
        try:
            if not member.bot:
                msg = await member.send(msg_kick)
        except:
            pass
        reason = f'Expulso por: {ctx.author} —— Motivo: {str(reason).replace("None", "nulo")}'
        try:
            await ctx.guild.kick(member, reason=reason)
        except discord.errors.Forbidden:
            await msg.delete()
            await ctx.send('Eu não tenho permissão para expulsar esse usuário. <a:sad:755774681008832623>')
        else:
            await ctx.send(content=get_emoji_dance(), embed=embed)

    @commands.command(name='unban',
                      aliases=['desbanir', 'revogar_ban'],
                      description='Revoga o banimento de algum membro!',
                      parameters=['<membro>', '[motivo (padrão: Nulo)]'],
                      examples=['``{prefix}unban`` ``"membro#1234"`` ``pode voltar``\n**(Observer que para usar ' +
                                'o comando unban, passando o nome e a tag da pessoa, é necessário usar "")**',
                                '``{prefix}revogar_ban`` ``123456789``'],
                      perm_user='banir membros',
                      perm_bot='banir membros',
                      cls=Androxus.Command)
    @permissions.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def _unban(self, ctx, member: BannedMember = None, *args):
        async with ctx.typing():  # vai aparecer "bot está digitando"
            if member is None:
                return await self.bot.send_help(ctx)
            reason = None
            if args:
                reason = ' '.join(args)
            embed = discord.Embed(title=f'Ban revogado!',
                                  colour=discord.Colour(random_color()),
                                  description=f'Usuário: {member.user}\nId: {member.user.id}\nMotivo: ' +
                                              f'{str(reason).replace("None", "nulo")}',
                                  timestamp=datetime.utcnow())
            if member.reason:
                embed.add_field(name='Antigo ban:',
                                value=f'{member.reason}',
                                inline=False)
            embed.set_footer(text=str(ctx.author),
                             icon_url=ctx.author.avatar_url)
            reason = f'Ban revogado por: {ctx.author} —— Motivo: {str(reason).replace("None", "nulo")}'
        try:
            await ctx.guild.unban(member.user, reason=reason)
        except discord.Forbidden:
            await ctx.send('Não tenho permissão para revogar banimentos!')
        except discord.HTTPException:
            await ctx.send('Desculpe, mas ocorreu um erro na hora de executar o comando, tente novamente mais tarde.')
        else:
            await ctx.send(content=get_emoji_dance(), embed=embed)

    @commands.command(name='change_prefix',
                      aliases=['prefixo', 'prefix'],
                      description='Comando que é usado para mudar o meu prefixo',
                      parameters=['``[prefixo (padrão: "--")]``'],
                      examples=['``{prefix}change_prefix`` ``!!``',
                                '``{prefix}prefixo``'],
                      perm_user='administrador',
                      cls=Androxus.Command)
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    async def _change_prefix(self, ctx, prefixo_novo=get_configs()['default_prefix']):
        conexao = Conexao()
        if ctx.prefix.replace("!", "").replace(" ", "") == self.bot.user.mention:
            # vai pegar o prefixo que está no banco
            prefixo_antigo = pegar_o_prefixo(self.bot, ctx, False, conexao)
        else:
            # se a pessoa não marcou o bot:
            prefixo_antigo = ctx.prefix
        servidor = Servidor(ctx.guild.id, prefixo_novo)
        ServidorRepository().update(conexao, servidor)
        if prefixo_novo != get_configs()['default_prefix']:
            embed = discord.Embed(title=f'Prefixo alterado com sucesso!', colour=discord.Colour(random_color()),
                                  description=f'Prefixo antigo: {prefixo_antigo}\n' +
                                              f'Prefixo novo: {prefixo_novo}',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.add_field(name=f'Caso queria voltar para o prefixo padrão, basta digitar ``{prefixo_novo}prefixo``!'
                                 f'\n{get_emoji_dance()}',
                            value='** **',
                            inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Agora estou com o prefixo padrão! {get_emoji_dance()}')
        conexao.fechar()

    @commands.command(name='desativar_sugestão',
                      aliases=['ds', 'desativar_sugestao'],
                      description='Comando que é usado para desativar as sugestões, quando a pessoa usar meu prefixo, '
                                  'com um comando que não existe',
                      examples=['``{prefix}desativar_sugestão``',
                                '``{prefix}ds``'],
                      perm_user='administrador',
                      cls=Androxus.Command)
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    async def _desativar_sugestao(self, ctx):
        conexao = Conexao()
        servidor = ServidorRepository().get_servidor(conexao, ctx.guild.id)
        if servidor.sugestao_de_comando:
            servidor.sugestao_de_comando = False
            ServidorRepository().update(conexao, servidor)
            conexao.fechar()
            return await ctx.send('Sugestões desativadas!')
        else:
            conexao.fechar()
            return await ctx.send('As sugestões já estavam desativadas!')

    @commands.command(name='reativar_sugestão',
                      aliases=['rs', 'reativar_sugestao'],
                      description='Comando que é usado para reativar as sugestões, quando a pessoa usar meu prefixo, '
                                  'com um comando que não existe',
                      examples=['``{prefix}reativar_sugestão``',
                                '``{prefix}rs``'],
                      perm_user='administrador',
                      cls=Androxus.Command)
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    async def _reativar_sugestao(self, ctx):
        conexao = Conexao()
        servidor = ServidorRepository().get_servidor(conexao, ctx.guild.id)
        if not servidor.sugestao_de_comando:
            servidor.sugestao_de_comando = True
            ServidorRepository().update(conexao, servidor)
            conexao.fechar()
            return await ctx.send('Sugestões reativadas!')
        else:
            conexao.fechar()
            return await ctx.send('As sugestões já estavam ativadas!')

    @commands.command(name='channel_log',
                      aliases=['chat_log', 'cl'],
                      description='Comando que é usado para configurar onde que o bot vai mandar os logs. Se não for'
                                  ' passado nada, vai desativar os logs.',
                      parameters=['[channel (padrão: nulo)]'],
                      examples=['``{prefix}chat_log`` {this_channel}',
                                '``{prefix}cl``'],
                      perm_user='administrador',
                      cls=Androxus.Command)
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    async def _channel_log(self, ctx, channel: discord.TextChannel = None):
        if channel is not None:
            conexao = Conexao()
            servidor = ServidorRepository().get_servidor(conexao, ctx.guild.id)
            if servidor.channel_id_log is None:
                servidor.channel_id_log = channel.id
                ServidorRepository().update(conexao, servidor)
                conexao.fechar()
                return await ctx.send(f'{ctx.author.mention} Log ativado com sucesso em <#{channel.id}>!')
            else:
                log_antigo = servidor.channel_id_log
                servidor.channel_id_log = channel.id
                ServidorRepository().update(conexao, servidor)
                conexao.fechar()
                return await ctx.send(f'{ctx.author.mention} Chat de logs alterado com sucesso!\n'
                                      f'Antigo: <#{log_antigo}>\nNovo: <#{channel.id}>')
        else:
            conexao = Conexao()
            servidor = ServidorRepository().get_servidor(conexao, ctx.guild.id)
            if servidor.channel_id_log is not None:
                servidor.channel_id_log = None
                ServidorRepository().update(conexao, servidor)
                conexao.fechar()
                return await ctx.send(f'{ctx.author.mention} Log desativado!')
            else:
                await self.bot.send_help(ctx)

    @_channel_log.error
    async def _channel_log_error(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.errors.ChannelNotFound):
            await ctx.send(f'{ctx.author.mention} Não consegui encontrar este channel.')
        else:
            raise error

    @commands.command(name='setup_logs',
                      aliases=['logs', 'sl'],
                      description='Comando que é usado para configurar os logs.',
                      examples=['``{prefix}setup_logs``',
                                '``{prefix}sl``'],
                      perm_user='administrador',
                      cls=Androxus.Command)
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    async def _setup_logs(self, ctx):
        conexao = Conexao()
        sr = ServidorRepository()
        servidor = sr.get_servidor(conexao, ctx.guild.id)
        if servidor.channel_id_log is None:
            conexao.fechar()
            return await ctx.send(f'{ctx.author.mention} Você precisa configurar um chat para os logs primeiro!'
                                  ' Use o comando ``channel_log``')

        def check(message):
            return message.author == ctx.author

        await ctx.send(f'{ctx.author.mention} Você quer que eu envie as mensagem deleta? (atual: '
                       f'{convert_to_string(servidor.mensagem_deletada)})(sim/não)')
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send('Tempo esgotado!')
        value = convert_to_bool(msg.content)
        if value is None:
            conexao.fechar()
            return await ctx.send(
                f'{ctx.author.mention} Eu não sei o que é {msg.content}. Eu só aceito ``sim`` ou ``não``')
        servidor.mensagem_deletada = value

        await ctx.send(f'{ctx.author.mention} Você quer que eu envie as mensagem editadas? (atual: '
                       f'{convert_to_string(servidor.mensagem_editada)})(sim/não)')
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send('Tempo esgotado!')
        value = convert_to_bool(msg.content)
        if value is None:
            conexao.fechar()
            return await ctx.send(
                f'{ctx.author.mention} Eu não sei o que é {msg.content}. Eu só aceito ``sim`` ou ``não``')
        servidor.mensagem_editada = value

        await ctx.send(f'{ctx.author.mention} Você quer que eu envie quando algum membro mudar o avatar? (atual: '
                       f'{convert_to_string(servidor.avatar_alterado)})(sim/não)')
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send('Tempo esgotado!')
        value = convert_to_bool(msg.content)
        if value is None:
            conexao.fechar()
            return await ctx.send(
                f'{ctx.author.mention} Eu não sei o que é {msg.content}. Eu só aceito ``sim`` ou ``não``')
        servidor.avatar_alterado = value

        await ctx.send(f'{ctx.author.mention} Você quer que eu envie quando algum membro mudar o nome? (atual: '
                       f'{convert_to_string(servidor.nome_alterado)})(sim/não)')
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send('Tempo esgotado!')
        value = convert_to_bool(msg.content)
        if value is None:
            conexao.fechar()
            return await ctx.send(
                f'{ctx.author.mention} Eu não sei o que é {msg.content}. Eu só aceito ``sim`` ou ``não``')
        servidor.nome_alterado = value

        await ctx.send(f'{ctx.author.mention} Você quer que eu envie quando algum membro mudar a tag? (atual: '
                       f'{convert_to_string(servidor.tag_alterado)})(sim/não)')
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send('Tempo esgotado!')
        value = convert_to_bool(msg.content)
        if value is None:
            conexao.fechar()
            return await ctx.send(
                f'{ctx.author.mention} Eu não sei o que é {msg.content}. Eu só aceito ``sim`` ou ``não``')
        servidor.tag_alterado = value

        await ctx.send(f'{ctx.author.mention} Você quer que eu envie quando algum membro de nick? (atual: '
                       f'{convert_to_string(servidor.nick_alterado)})(sim/não)')
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send('Tempo esgotado!')
        value = convert_to_bool(msg.content)
        if value is None:
            conexao.fechar()
            return await ctx.send(
                f'{ctx.author.mention} Eu não sei o que é {msg.content}. Eu só aceito ``sim`` ou ``não``')
        servidor.nick_alterado = value

        await ctx.send(
            f'{ctx.author.mention} Você quer que eu envie quando algum cargo, de algum membro, for alterado? (atual: '
            f'{convert_to_string(servidor.role_alterado)})(sim/não)')
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send('Tempo esgotado!')
        value = convert_to_bool(msg.content)
        if value is None:
            conexao.fechar()
            return await ctx.send(
                f'{ctx.author.mention} Eu não sei o que é {msg.content}. Eu só aceito ``sim`` ou ``não``')
        servidor.role_alterado = value
        sr.update(conexao, servidor)
        conexao.fechar()
        return await ctx.send(f'{ctx.author.mention} configurações feitas com sucesso! Para você ver todas as'
                              ' configurações, digite "configs"')


def setup(bot):
    bot.add_cog(Admin(bot))
