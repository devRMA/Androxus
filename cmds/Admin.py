# -*- coding: utf-8 -*-
# Androxus bot
# Admin.py

__author__ = 'Rafael'

import asyncio
from datetime import datetime

import discord
from discord.ext import commands

from Classes import Androxus
from database.Repositories.ServidorRepository import ServidorRepository
from utils import permissions
from utils.Utils import get_emoji_dance, get_configs, pegar_o_prefixo, convert_to_string, \
    convert_to_bool, is_number
from utils.converters import BannedMember


class Admin(commands.Cog, command_attrs=dict(category='administração')):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.Androxus.Androxus): Instância do bot

        """
        self.bot = bot

    @Androxus.comando(name='ban',
                      aliases=['banir'],
                      description='Vou banir algum membro.',
                      parameters=['<membro do servidor>', '[motivo (padrão: Nulo)]'],
                      examples=['``{prefix}ban`` ``@membro#1234`` ``ofendeu membro``',
                                '``{prefix}banir`` {author_mention}'],
                      perm_user='banir membros',
                      perm_bot='banir membros')
    @permissions.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _ban(self, ctx, member: discord.Member = None, *args):
        if isinstance(args, tuple):
            # se chegar como tupla, vai transformar em lista
            args = list(args)
        # se a pessoa passou pelo menos o membro, ou algum argumento
        if args or member:
            if not member:
                try:
                    id = int(args[0])
                except ValueError:
                    return await self.bot.send_help(ctx)
                else:
                    args.pop(0)
                try:
                    member = await ctx.guild.fetch_member(id)
                except:
                    member = None
                if member is None:  # se não achou o membro:
                    return await ctx.reply(f'Não consegui encontrar o membro com id `{id}`!', mention_author=False)
            # vai verificar se a pessoa pode usar o comando
            if ctx.guild.owner == member:
                return await ctx.reply(f'Você não pode banir o dono do servidor! '
                                       f'{self.bot.get_emoji("ah_nao")}')
            elif member == ctx.author:
                return await ctx.reply(f'Você não pode se banir! '
                                       f'{self.bot.get_emoji("ah_nao")}')
            elif member == self.bot.user:
                return await ctx.reply(f'Eu não posso me banir! '
                                       f'{self.bot.get_emoji("ah_nao")}')
            elif ctx.author.id in self.bot.configs['owners'] or ctx.author == ctx.guild.owner:
                pass  # se for o dono do bot, ou dono do servidor, vai ignorar as próxima verificação
            elif ctx.author.top_role <= member.top_role:
                return await ctx.reply('Você só pode banir pessoas que tenham cargo mais '
                                       'baixo que o seu!')
            # se sobrou algum argumento, é porque a pessoa passou um motivo
            reason = None
            if args:
                reason = ' '.join(args)
        else:
            # se a pessoa não passou nada:
            return await self.bot.send_help(ctx)
        embed = discord.Embed(title=f'{self.bot.get_emoji("banned")} Usuário banido!',
                              colour=discord.Colour.random(),
                              description=f'Usuário: {member}\nId: {member.id}\nMotivo: ' +
                                          f'{str(reason).replace("None", "nulo")}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=str(ctx.author),
                         icon_url=ctx.author.avatar_url)
        msg_ban = f'{member.mention} Você foi banido do servidor {ctx.guild}!'
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
            await ctx.reply(f'Eu não tenho permissão para banir este usuário. {self.bot.get_emoji("sad")}',
                            mention_author=False)
        else:
            await ctx.reply(embed=embed,
                            mention_author=False)

    @Androxus.comando(name='kick',
                      aliases=['expulsar'],
                      description='Vou expulsar algum membro.',
                      parameters=['<membro do servidor>', '[motivo (padrão: Nulo)]'],
                      examples=['``{prefix}kick`` ``@membro#1234`` ``não quero você aqui!``',
                                '``{prefix}expulsar`` {author_mention}'],
                      perm_user='expulsar membros',
                      perm_bot='expulsar membros')
    @permissions.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _kick(self, ctx, member: discord.Member = None, *args):
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
                    return await ctx.reply(f'Não consegui encontrar o membro com id `{id}`!')
            # vai verificar se a pessoa pode usar o comando
            if ctx.guild.owner == member:
                return await ctx.reply(f'Você não pode expulsar o dono do servidor! '
                                       f'{self.bot.get_emoji("ah_nao")}')
            elif member == ctx.author:
                return await ctx.reply(f'Você não pode se expulsar! '
                                       f'{self.bot.get_emoji("ah_nao")}')
            elif member == self.bot.user:
                return await ctx.reply(f'Eu não posso me expulsar! '
                                       f'{self.bot.get_emoji("ah_nao")}')
            elif ctx.author.id in self.bot.configs['owners'] or ctx.author == ctx.guild.owner:
                pass  # se for o dono do bot, ou dono do servidor, vai ignorar as próxima verificação
            elif ctx.author.top_role <= member.top_role:
                return await ctx.reply(f'Você só pode expulsar pessoas que tenham cargo mais '
                                       'baixo que o seu!')
            # se sobrou algum argumento, é porque a pessoa passou um motivo
            reason = None
            if args:
                reason = ' '.join(args)
        else:
            # se a pessoa não passou nada:
            return await self.bot.send_help(ctx)
        embed = discord.Embed(title=f'Usuário expulso!',
                              colour=discord.Colour.random(),
                              description=f'Usuário: {member}\nId: {member.id}\nMotivo: ' +
                                          f'{str(reason).replace("None", "nulo")}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=str(ctx.author),
                         icon_url=ctx.author.avatar_url)
        msg_kick = f'{member.mention} Você foi expulso do servidor {ctx.guild}!'
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
            await ctx.reply(f'Eu não tenho permissão para expulsar esse usuário. {self.bot.get_emoji("sad")}',
                            mention_author=False)
        else:
            await ctx.reply(content=get_emoji_dance(), embed=embed,
                            mention_author=False)

    @Androxus.comando(name='unban',
                      aliases=['desbanir', 'revogar_ban'],
                      description='Revoga o banimento de algum membro!',
                      parameters=['<membro>', '[motivo (padrão: Nulo)]'],
                      examples=['``{prefix}unban`` ``"membro#1234"`` ``pode voltar``\n**(Observer que para usar ' +
                                'o comando unban, passando o nome e a tag da pessoa, é necessário usar "")**',
                                '``{prefix}revogar_ban`` ``123456789``'],
                      perm_user='banir membros',
                      perm_bot='banir membros')
    @permissions.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _unban(self, ctx, member: BannedMember = None, *args):
        if member is None:
            return await self.bot.send_help(ctx)
        reason = None
        if args:
            reason = ' '.join(args)
        embed = discord.Embed(title=f'Ban revogado!',
                              colour=discord.Colour.random(),
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
            await ctx.reply('Não tenho permissão para revogar banimentos!')
        except discord.HTTPException:
            await ctx.reply('Desculpe, mas ocorreu um erro na hora de executar o comando, tente novamente mais tarde.',
                            mention_author=False)
        else:
            await ctx.reply(content=get_emoji_dance(), embed=embed, mention_author=False)

    @Androxus.comando(name='change_prefix',
                      aliases=['prefixo', 'prefix'],
                      description='Comando que é usado para mudar o meu prefixo',
                      parameters=['``[prefixo (padrão: "--")]``'],
                      examples=['``{prefix}change_prefix`` ``!!``',
                                '``{prefix}prefixo``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _change_prefix(self, ctx, prefixo_novo=get_configs()['default_prefix']):
        if ctx.prefix.replace("!", "").replace(" ", "") == self.bot.user.mention:
            # vai pegar o prefixo que está no banco
            prefixo_antigo = await pegar_o_prefixo(self.bot, ctx)
        else:
            # se a pessoa não marcou o bot:
            prefixo_antigo = ctx.prefix
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        await ServidorRepository().update(self.bot.db_connection, servidor)
        if prefixo_novo != self.bot.configs['default_prefix']:
            embed = discord.Embed(title=f'Prefixo alterado com sucesso!', colour=discord.Colour.random(),
                                  description=f'Prefixo antigo: {prefixo_antigo}\n' +
                                              f'Prefixo novo: {prefixo_novo}',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.add_field(name=f'Caso queria voltar para o prefixo padrão, basta digitar ``{prefixo_novo}prefixo``!'
                                 f'\n{get_emoji_dance()}',
                            value='** **',
                            inline=False)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f'Agora estou com o prefixo padrão! {get_emoji_dance()}')

    @Androxus.comando(name='desativar_sugestão',
                      aliases=['ds', 'desativar_sugestao'],
                      description='Comando que é usado para desativar as sugestões, quando a pessoa usar meu prefixo, '
                                  'com um comando que não existe',
                      examples=['``{prefix}desativar_sugestão``',
                                '``{prefix}ds``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _desativar_sugestao(self, ctx):
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        if servidor.sugestao_de_comando:
            servidor.sugestao_de_comando = False
            await ServidorRepository().update(self.bot.db_connection, servidor)
            return await ctx.reply('Sugestões desativadas!')
        else:
            return await ctx.reply('As sugestões já estavam desativadas!')

    @Androxus.comando(name='reativar_sugestão',
                      aliases=['rs', 'reativar_sugestao'],
                      description='Comando que é usado para reativar as sugestões, quando a pessoa usar meu prefixo, '
                                  'com um comando que não existe',
                      examples=['``{prefix}reativar_sugestão``',
                                '``{prefix}rs``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _reativar_sugestao(self, ctx):
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        if not servidor.sugestao_de_comando:
            servidor.sugestao_de_comando = True
            await ServidorRepository().update(self.bot.db_connection, servidor)
            return await ctx.reply('Sugestões reativadas!')
        else:
            return await ctx.reply('As sugestões já estavam ativadas!')

    @Androxus.comando(name='channel_log',
                      aliases=['chat_log', 'cl'],
                      description='Comando que é usado para configurar onde que o bot vai mandar os logs. Se não for'
                                  ' passado nada, vai desativar os logs.',
                      parameters=['[channel (padrão: nulo)]'],
                      examples=['``{prefix}chat_log`` {this_channel}',
                                '``{prefix}cl``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _channel_log(self, ctx, channel: discord.TextChannel = None):
        if channel is not None:
            perms = channel.permissions_for(ctx.me)
            if not perms.send_messages:
                return await ctx.reply(f'Eu não tenho permissão para enviar mensagem neste chat.')
            elif not perms.embed_links:
                return await ctx.reply(f'Eu não tenho permissão de inserir links na '
                                       f'mensagem, neste chat.')
            elif not perms.attach_files:
                return await ctx.reply(f'Eu não tenho permissão enviar arquivos neste chat.')
            elif channel.guild.id != ctx.guild.id:
                return await ctx.reply(f'Você precisa me dizer um chat **deste** servidor')
            servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
            if servidor.channel_id_log is None:
                servidor.channel_id_log = channel.id
                await ServidorRepository().update(self.bot.db_connection, servidor)
                return await ctx.reply(f' Log ativado com sucesso em {channel.mention}!')
            else:
                log_antigo = servidor.channel_id_log
                servidor.channel_id_log = channel.id
                await ServidorRepository().update(self.bot.db_connection, servidor)
                return await ctx.reply('Chat de logs alterado com sucesso!\n'
                                       f'Antigo: <#{log_antigo}>\nNovo: <#{channel.id}>')
        else:
            servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
            if servidor.channel_id_log is not None:
                servidor.channel_id_log = None
                await ServidorRepository().update(self.bot.db_connection, servidor)
                return await ctx.reply(f'Log desativado!')
            else:
                return await self.bot.send_help(ctx)

    @_channel_log.error
    async def _channel_log_error(self, ctx, error):
        if self.bot.maintenance_mode and (
                isinstance(error, commands.BadArgument) or isinstance(error, commands.errors.ChannelNotFound)):
            return await ctx.reply(f'Não consegui encontrar este channel.')
        raise error

    @Androxus.comando(name='setup_logs',
                      aliases=['logs', 'sl'],
                      description='Comando que é usado para configurar os logs.',
                      examples=['``{prefix}setup_logs``',
                                '``{prefix}sl``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _setup_logs(self, ctx):
        # TODO
        sr = ServidorRepository()
        servidor = await sr.get_servidor(self.bot.db_connection, ctx.guild.id)
        if servidor.channel_id_log is None:
            return await ctx.reply(f'Você precisa configurar um chat para os logs primeiro!'
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
            return await ctx.send(
                f'{ctx.author.mention} Eu não sei o que é {msg.content}. Eu só aceito ``sim`` ou ``não``')
        servidor.role_alterado = value
        await sr.update(self.bot.db_connection, servidor)
        return await ctx.send(f'{ctx.author.mention} configurações feitas com sucesso! Para você ver todas as'
                              ' configurações, digite "configs"')

    @Androxus.comando(name='clear',
                      aliases=['limpar', 'purge'],
                      description='Vou limpar o chat.',
                      parameters=['<número de mensagens>'],
                      examples=['``{prefix}clear`` ``10``',
                                '``{prefix}purge`` ``40``'],
                      perm_user='gerenciar mensagens',
                      perm_bot='gerenciar mensagens')
    @permissions.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _clear(self, ctx, messages=None):
        if messages is not None:
            if is_number(messages):
                try:
                    messages = int(messages)
                except ValueError:
                    return await ctx.reply(f'Eu só aceito números inteiros!')
            else:
                return await ctx.reply(f'Digite um número válido!')
            if 200 >= messages >= 1:
                try:
                    deleted = await ctx.channel.purge(limit=messages + 1, check=lambda m: not m.pinned)
                except:
                    return await ctx.send(f'{ctx.author.mention} não consegui deletar as mensagens. Tente novamente.')
                else:
                    if (len(deleted) - 1) >= messages:
                        return await ctx.send(f'{ctx.author.mention} deletou {len(deleted) - 1} mensagens!',
                                              delete_after=5)
                    else:
                        return await ctx.send(f'{ctx.author.mention} não foi(ram) deletada(s) '
                                              f'{abs(messages - len(deleted) - 1)} mensagem(ns), pois estava(m) '
                                              f'fixada(s).',
                                              delete_after=5)
            else:
                return await ctx.reply(f'Informe um número entre 1 e 200!')
        else:
            return await self.bot.send_help(ctx)


def setup(bot):
    bot.add_cog(Admin(bot))
