# -*- coding: utf-8 -*-
# Androxus bot
# Admin.py

__author__ = 'Rafael'

import asyncio

import discord
from discord.ext import commands

from Classes import Androxus
from database.Repositories.ServidorRepository import ServidorRepository
from utils import permissions
from utils.Utils import get_emoji_dance, get_configs, convert_to_bool, is_number
from utils.converters import BannedMember


class Admin(commands.Cog, command_attrs=dict(category='administração')):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.Androxus.Androxus): Instância do bot

        """
        self.bot = bot
        self.sr = ServidorRepository()

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
    async def _ban(self, ctx, member: discord.Member = None, *, reason=None):
        messages_error = await self.bot.translate(ctx, error_='ban', values_={
            'ah_nao': self.bot.get_emoji('ah_nao'),
            'sad': self.bot.get_emoji('sad')
        })
        # se a pessoa passou o membro
        if member:
            # vai verificar se a pessoa pode usar o comando
            if ctx.guild.owner == member:
                return await ctx.send(**messages_error[0])
            elif member == ctx.author:
                return await ctx.send(**messages_error[1])
            elif member == self.bot.user:
                return await ctx.send(**messages_error[2])
            elif ctx.author.id in self.bot.configs['owners'] or ctx.author == ctx.guild.owner:
                pass  # se for o dono do bot, ou dono do servidor, vai ignorar as próxima verificação
            elif ctx.author.top_role <= member.top_role:
                return await ctx.send(**messages_error[3])
        else:
            # se a pessoa não passou o membro:
            return await self.bot.send_help(ctx)
        messages = await self.bot.translate(ctx, values_={
            'banned': self.bot.get_emoji('banned'),
            'member': member,
            'reason': reason
        })
        reasons = await self.bot.translate(ctx, others_='ban', values_={
            'reason': reason
        })
        try:
            if not member.bot:
                msg = await member.send(reasons['member_no_reason' if reason is None else 'member_reason'])
        except:
            pass
        try:
            reason_audit = reasons['reason_audit_log_no_reason' if reason is None else 'reason_audit_log']
            await ctx.guild.ban(member, reason=reason_audit)
        except discord.errors.Forbidden:
            try:
                if not member.bot:
                    await msg.delete()
            except:
                pass
            await ctx.send(**messages_error[4])
        else:
            message_successful = messages[0] if reason else messages[1]
            await ctx.send(**message_successful)

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
    async def _kick(self, ctx, member: discord.Member = None, *, reason=None):
        messages_error = await self.bot.translate(ctx, error_='kick', values_={
            'ah_nao': self.bot.get_emoji('ah_nao'),
            'sad': self.bot.get_emoji('sad')
        })
        # se a pessoa passou o membro
        if member:
            # vai verificar se a pessoa pode usar o comando
            if ctx.guild.owner == member:
                return await ctx.send(**messages_error[0])
            elif member == ctx.author:
                return await ctx.send(**messages_error[1])
            elif member == self.bot.user:
                return await ctx.send(**messages_error[2])
            elif ctx.author.id in self.bot.configs['owners'] or ctx.author == ctx.guild.owner:
                pass  # se for o dono do bot, ou dono do servidor, vai ignorar as próxima verificação
            elif ctx.author.top_role <= member.top_role:
                return await ctx.send(**messages_error[3])
        else:
            # se a pessoa não passou o membro:
            return await self.bot.send_help(ctx)
        messages = await self.bot.translate(ctx, values_={
            'member': member,
            'reason': reason
        })
        reasons = await self.bot.translate(ctx, others_='kick', values_={
            'reason': reason
        })
        try:
            if not member.bot:
                msg = await member.send(reasons['member_no_reason' if reason is None else 'member_reason'])
        except:
            pass
        try:
            reason_audit = reasons['reason_audit_log_no_reason' if reason is None else 'reason_audit_log']
            await ctx.guild.kick(member, reason=reason_audit)
        except discord.errors.Forbidden:
            try:
                if not member.bot:
                    await msg.delete()
            except:
                pass
            await ctx.send(**messages_error[4])
        else:
            message_successful = messages[0] if reason else messages[1]
            await ctx.send(**message_successful)

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
    async def _unban(self, ctx, member: BannedMember = None, *, reason=None):
        if member is None:
            return await self.bot.send_help(ctx)
        messages = await self.bot.translate(ctx, values_={
            'member': member,
            'reason': reason
        })
        others = await self.bot.translate(ctx, others_='unban', values_={
            'reason': reason
        })
        erros = await self.bot.translate(ctx, error_='unban')
        message_successful = messages[0 if reason else 1]
        if member.reason:
            message_successful['embed'].add_field(name=others['old_ban_reason'],
                                                  value=str(member.reason),
                                                  inline=False)
        try:
            reason_audit = others['reason_audit_log_no_reason' if reason is None else 'reason_audit_log']
            await ctx.guild.unban(member.user, reason=reason_audit)
        except discord.Forbidden:
            await ctx.send(**erros[0])
        except discord.HTTPException:
            await ctx.send(**erros[1])
        else:
            await ctx.send(**message_successful)

    @Androxus.comando(name='change_prefix',
                      aliases=['prefixo', 'prefix'],
                      description='Comando que é usado para mudar o meu prefixo',
                      parameters=['[prefixo (padrão: "--")]'],
                      examples=['``{prefix}change_prefix`` ``!!``',
                                '``{prefix}prefixo``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _change_prefix(self, ctx, new_prefix=get_configs()['default_prefix']):
        if len(new_prefix) <= 20:
            servidor = await self.sr.get_servidor(self.bot.db_connection, ctx.guild.id)
            old_prefix = servidor.prefixo
            servidor.prefixo = new_prefix
            await self.sr.update(self.bot.db_connection, servidor)
            messages = await self.bot.translate(ctx, values_={
                'new_prefix': new_prefix,
                'old_prefix': old_prefix,
                'dance': get_emoji_dance()
            })
            if new_prefix != self.bot.configs['default_prefix']:
                await ctx.send(**messages[0])
            else:
                await ctx.send(**messages[1])
        else:
            erro = (await self.bot.translate(ctx, error_='change_prefix'))[0]
            await ctx.send(**erro)

    @Androxus.comando(name='change_lang',
                      aliases=['language', 'lingua', 'língua', 'lang'],
                      description='Comando que é usado para mudar a língua',
                      parameters=['[lingua (padrão: "en_us")]'],
                      examples=['``{prefix}change_prefix`` ``!!``',
                                '``{prefix}prefixo``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.check(permissions.is_owner)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _change_lang(self, ctx, new_lang='en_us'):
        servidor = await self.sr.get_servidor(self.bot.db_connection, ctx.guild.id)
        if new_lang.lower() in self.bot.supported_langs:
            servidor.lang = new_lang.lower()
            await self.sr.update(self.bot.db_connection, servidor)
            messages = await self.bot.translate(ctx)
            await ctx.send(**messages[0])
        else:
            await self.bot.send_help(ctx)

    @Androxus.comando(name='desativar_sugestao',
                      aliases=['ds', 'desativar_sugestão'],
                      description='Comando que é usado para desativar as sugestões, quando a pessoa usar meu prefixo, '
                                  'com um comando que não existe',
                      examples=['{prefix}desativar_sugestão',
                                '``{prefix}ds``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _desativar_sugestao(self, ctx):
        messages = await self.bot.translate(ctx)
        servidor = await self.sr.get_servidor(self.bot.db_connection, ctx.guild.id)
        if servidor.sugestao_de_comando:
            servidor.sugestao_de_comando = False
            await self.sr.update(self.bot.db_connection, servidor)
            return await ctx.send(**messages[0])
        else:
            return await ctx.send(**messages[1])

    @Androxus.comando(name='reativar_sugestao',
                      aliases=['rs', 'reativar_sugestão'],
                      description='Comando que é usado para reativar as sugestões, quando a pessoa usar meu prefixo, '
                                  'com um comando que não existe',
                      examples=['``{prefix}reativar_sugestão``',
                                '``{prefix}rs``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _reativar_sugestao(self, ctx):
        messages = await self.bot.translate(ctx)
        servidor = await self.sr.get_servidor(self.bot.db_connection, ctx.guild.id)
        if not servidor.sugestao_de_comando:
            servidor.sugestao_de_comando = True
            await self.sr.update(self.bot.db_connection, servidor)
            return await ctx.send(**messages[0])
        else:
            return await ctx.send(**messages[1])

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
        erros = await self.bot.translate(ctx, error_='channel_log')
        messages = await self.bot.translate(ctx, values_={
            'channel': channel or ctx.channel,  # passando o ctx.channel só para não dar erro na hora do format
            'old_log': ''  # passando em branco, pois só usa em um caso específico
        })
        if channel is not None:
            perms = channel.permissions_for(ctx.me)
            if not perms.send_messages:
                return await ctx.send(**erros[0])
            elif not perms.embed_links:
                return await ctx.send(**erros[1])
            elif not perms.attach_files:
                return await ctx.send(**erros[2])
            servidor = await self.sr.get_servidor(self.bot.db_connection, ctx.guild.id)
            if servidor.channel_id_log is None:
                servidor.channel_id_log = channel.id
                await self.sr.update(self.bot.db_connection, servidor)
                await ctx.send(**messages[0])
            else:
                messages = await self.bot.translate(ctx, values_={
                    'channel': channel,
                    'old_log': servidor.channel_id_log
                })
                servidor.channel_id_log = channel.id
                await self.sr.update(self.bot.db_connection, servidor)
                await ctx.send(**messages[1])
        else:
            servidor = await self.sr.get_servidor(self.bot.db_connection, ctx.guild.id)
            if servidor.channel_id_log is not None:
                servidor.channel_id_log = None
                await self.sr.update(self.bot.db_connection, servidor)
                await ctx.send(**messages[2])
            else:
                return await self.bot.send_help(ctx)

    @Androxus.comando(name='setup_logs',
                      aliases=['logs', 'sl', 'setupLogs'],
                      description='Comando que é usado para configurar os logs.',
                      examples=['``{prefix}setup_logs``',
                                '``{prefix}sl``'],
                      perm_user='administrador')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _setup_logs(self, ctx):
        servidor = await self.sr.get_servidor(self.bot.db_connection, ctx.guild.id)
        erros = await self.bot.translate(ctx, error_='setup_logs', values_={
            'user_input': ''
        })
        if servidor.channel_id_log is None:
            return await ctx.send(**erros[0])
        messages = await self.bot.translate(ctx)
        others = await self.bot.translate(ctx, others_='setup_logs', values_={
            'ativado': self.bot.get_emoji('ativado'),
            'desativado': self.bot.get_emoji('desativado')
        })
        for field_name, attr in others['logs_attr'].items():
            message = messages[0].copy()
            message['embed'] = messages[0]['embed'].copy()
            message['embed'].add_field(name=field_name, value='** **', inline=False)
            message['embed'].add_field(name=others['Now'], value=others[str(getattr(servidor, attr))], inline=False)
            await ctx.send(**message)
            try:
                msg_user = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                return await ctx.send(**erros[1])
            value = convert_to_bool(msg_user.content)
            if value is None:
                erros = await self.bot.translate(ctx, error_='setup_logs', values_={
                    'user_input': msg_user.content
                })
                return await ctx.send(**erros[2])
            setattr(servidor, attr, value)
            if ctx.channel.permissions_for(ctx.me).manage_messages:
                await ctx.channel.purge(limit=2, check=lambda m: m.author in [ctx.me, ctx.author])
        await self.sr.update(self.bot.db_connection, servidor)
        return await ctx.send(**messages[1])

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
            erros = await self.bot.translate(ctx, error_='clear')
            if is_number(messages):
                try:
                    messages = int(messages)
                except ValueError:
                    return await ctx.send(**erros[0])
            else:
                return await ctx.send(**erros[1])
            if 200 >= messages >= 1:
                try:
                    deleted = await ctx.channel.purge(limit=messages + 1, check=lambda m: not m.pinned)
                except:
                    return await ctx.send(**erros[2])
                else:
                    keep = abs(messages - (len(deleted) - 1))
                    translated_messages = await self.bot.translate(ctx, values_={
                        'deleted': len(deleted) - 1,
                        'keep': keep
                    })
                    if (len(deleted) - 1) >= messages:
                        return await ctx.send(**translated_messages[0])
                    else:
                        if keep > 1:
                            return await ctx.send(**translated_messages[1])
                        else:
                            return await ctx.send(**translated_messages[2])
            else:
                return await ctx.send(**erros[3])
        else:
            return await self.bot.send_help(ctx)


def setup(bot):
    bot.add_cog(Admin(bot))
