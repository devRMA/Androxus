# -*- coding: utf-8 -*-
# Androxus bot
# Admin.py

__author__ = 'Rafael'

import asyncio
from datetime import datetime

import discord
from colorama import Style, Fore
from discord.ext import commands

from EmbedGenerators.HelpGroup import embed_help_group
from database.Models.ComandoDesativado import ComandoDesativado
from database.Models.ComandoPersonalizado import ComandoPersonalizado
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils import permissions
from utils.Utils import get_configs, is_number
from utils.Utils import get_emoji_dance, convert_to_bool, capitalize, convert_to_string
from utils.converters import BannedMember


class Admin(commands.Cog):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.General.Androxus): Instância do bot

        """
        self.bot = bot
        self.sr = ServidorRepository()

    @commands.group(name='administração', case_insensitive=True, invoke_without_command=True, ignore_extra=False,
                    aliases=['adm', 'admin', 'administraçao', 'administracão', 'administracao',
                             'management', 'administration'])
    async def administracao_gp(self, ctx):
        await ctx.reply(embed=await embed_help_group(ctx), mention_author=False)

    @administracao_gp.command(name='ban', aliases=['banir'])
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
            elif ctx.author.id in self.bot.configs.owners or ctx.author == ctx.guild.owner:
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

    @administracao_gp.command(name='kick', aliases=['expulsar'])
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
            elif ctx.author.id in self.bot.configs.owners or ctx.author == ctx.guild.owner:
                pass  # se for o dono do bot, ou dono do servidor, vai ignorar as próxima verificação
            elif ctx.author.top_role <= member.top_role:
                return await ctx.send(**messages_error[3])
        else:
            # se a pessoa não passou o membro:
            return await self.bot.send_help(ctx)
        messages = await self.bot.translate(ctx, values_={
            'member': member,
            'member_id': member.id if hasattr(member, 'id') else 0,
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

    @administracao_gp.command(name='unban', aliases=['desbanir', 'revogar_ban'])
    @permissions.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _unban(self, ctx, member: BannedMember = None, *, reason=None):
        if member is None:
            return await self.bot.send_help(ctx)
        messages = await self.bot.translate(ctx, values_={
            'member': member,
            'member_id': member.id if hasattr(member, 'id') else 0,
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

    @administracao_gp.command(name='change_prefix',
                              aliases=['prefixo', 'prefix', 'changeprefix', 'set_prefix', 'setprefix'])
    @permissions.has_permissions(manage_messages=True)
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
            if new_prefix != self.bot.configs.default_prefix:
                await ctx.send(**messages[0])
            else:
                await ctx.send(**messages[1])
        else:
            erro = (await self.bot.translate(ctx, error_='change_prefix'))[0]
            await ctx.send(**erro)

    @administracao_gp.command(name='change_lang',
                              aliases=['language', 'lingua', 'língua', 'lang', 'changelang', 'set_lang', 'setlang'])
    @permissions.has_permissions(manage_messages=True)
    @commands.check(permissions.is_owner)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _change_lang(self, ctx, *, new_lang=None):
        servidor = await self.sr.get_servidor(self.bot.db_connection, ctx.guild.id)
        default_lang = self.bot.translations.get(get_configs().get('default_lang'))
        is_default = False
        old_lang = self.bot.translations.get(servidor.lang)
        erros = await self.bot.translate(ctx, error_='change_lang', values_={
            'new_lang': new_lang,
            'langs': ', '.join(map(lambda l: f'`{l.name}`', self.bot.translations.supported_languages))
        })
        if new_lang is None:
            new_lang = default_lang
            is_default = True
        else:
            new_lang = self.bot.translations.get(new_lang.lower())
        if new_lang:
            if old_lang != new_lang.name:
                servidor.lang = new_lang.name
                await self.sr.update(self.bot.db_connection, servidor)
                messages = await self.bot.translate(ctx, values_={
                    'dance': get_emoji_dance(),
                    'old_lang': old_lang,
                    'new_lang': new_lang
                })
                await ctx.send(**messages[1 if is_default else 0])
            else:
                await ctx.send(**erros[0])
        else:
            await ctx.send(**erros[1])

    @administracao_gp.command(name='desativar_sugestao', aliases=['ds', 'desativar_sugestão', 'disable_suggestion',
                                                                  'desativarsugestao', 'desativarsugestão',
                                                                  'disablesuggestion'])
    @permissions.has_permissions(manage_messages=True)
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

    @administracao_gp.command(name='reativar_sugestao', aliases=['rs', 'reativar_sugestão', 'reactivate_suggestion',
                                                                 'reativarsugestao', 'reativarsugestão',
                                                                 'reactivatesuggestion'])
    @permissions.has_permissions(manage_messages=True)
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

    @administracao_gp.command(name='channel_log', aliases=['chat_log', 'cl', 'channellog', 'chatlog'])
    @permissions.has_permissions(manage_messages=True)
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

    @administracao_gp.command(name='setup_logs', aliases=['logs', 'sl', 'setuplogs'])
    @permissions.has_permissions(manage_messages=True)
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
        messages_to_delete = []
        for field_name, attr in others.get('logs_attr').items():
            message = messages[0].copy()
            message['embed'] = messages[0]['embed'].copy()
            message['embed'].add_field(name=field_name, value='** **', inline=False)
            message['embed'].add_field(name=others['Now'], value=others[str(getattr(servidor, attr))], inline=False)
            messages_to_delete.append(await ctx.send(**message))
            try:
                msg_user = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=30)
                messages_to_delete.append(msg_user)
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
                await ctx.channel.purge(limit=2, check=lambda m: m in messages_to_delete)
        await self.sr.update(self.bot.db_connection, servidor)
        return await ctx.send(**messages[1])

    @administracao_gp.command(name='clear', aliases=['limpar', 'purge', 'purificar'])
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

    @administracao_gp.command(name='desativar_comando', aliases=['disable_command', 'dc', 'desativarcomando'])
    @permissions.has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _desativar_comando(self, ctx, *, comando: str = None):
        if comando is None:
            return await self.bot.send_help(ctx)
        comandos_que_nao_podem_ser_desativados = ['desativar_comando',
                                                  'reativar_comando',
                                                  'help']
        comando_para_desativar = self.bot.get_command(comando)
        if comando_para_desativar is None:
            return await ctx.reply(f'não tenho esse comando!')
        if comando_para_desativar.name in comandos_que_nao_podem_ser_desativados:
            return await ctx.reply(
                f'Você não pode desativar este comando! {self.bot.get_emoji("no_no")}')
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        comando_desativado = ComandoDesativado(servidor, comando_para_desativar.name)
        await ComandoDesativadoRepository().create(self.bot.db_connection, comando_desativado)
        embed = discord.Embed(title=f'Comando desativado com sucesso!', colour=discord.Colour.random(),
                              description=f'Comando desativado: {comando_para_desativar.name}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar.url}')
        return await ctx.reply(content=self.bot.get_emoji('off'), embed=embed, mention_author=False)

    @administracao_gp.command(name='reativar_comando',
                              aliases=['reactivate_command', 'reativarcomando', 'reactivatecommand'])
    @permissions.has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _reativar_comando(self, ctx, comando=None):
        if comando is None:
            return await self.bot.send_help(ctx)
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        comando_para_reativar = self.bot.get_command(comando)
        if comando_para_reativar is None:
            return await ctx.reply('Não tenho esse comando!')
        comando_desativado = ComandoDesativado(servidor, comando_para_reativar.name)
        comandos_desativados = await ComandoDesativadoRepository().get_commands(self.bot.db_connection, servidor)
        if comando_desativado not in [cmd for cmd in comandos_desativados]:
            return await ctx.reply(f'{self.bot.get_emoji("atencao")} Este comando já está ativo!')
        await ComandoDesativadoRepository().delete(self.bot.db_connection, comando_desativado)
        embed = discord.Embed(title=f'Comando reativado com sucesso!', colour=discord.Colour.random(),
                              description=f'Comando reativado: {comando_para_reativar.name}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar.url}')
        return await ctx.reply(content=self.bot.get_emoji('on'), embed=embed, mention_author=False)

    @administracao_gp.command(name='adicionar_comando', aliases=['add_command', 'ac',
                                                                 'adicionarcomando', 'addcommand',
                                                                 'criar_comando', 'criarcomando',
                                                                 'create_command', 'createcommand'])
    @permissions.has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _adicionar_comando(self, ctx, comando='', resposta='', in_text='t'):
        in_text = convert_to_bool(in_text)
        if in_text is None:
            return await ctx.reply(
                f'Valor ``{in_text}`` inválido! Os valores que eu aceito são: sim, não, yes, no, 0, 1')
        if ctx.message.content.count('"') < 4:
            return await ctx.reply('Parece que você digitou o comando errado!\nVocê deve usar o comando assim:\n'
                                   f'{ctx.prefix}adicionar_comando **"**comando**"** **"**resposta**"**')
        if (comando.replace(' ', '') == '') or (resposta.replace(' ', '') == ''):
            return await self.bot.send_help(ctx)
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        comando_personalizado = ComandoPersonalizado(servidor,
                                                     comando.lower(),
                                                     resposta,
                                                     in_text)
        await ComandoPersonalizadoRepository().create(self.bot.db_connection, comando_personalizado)
        in_text_str = capitalize(convert_to_string(in_text))
        embed = discord.Embed(title=f'Comando adicionado com sucesso!', colour=discord.Colour.random(),
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar.url)
        embed.add_field(
            name=f'Comando: {comando.lower()}\nResposta: {resposta}\nIgnorar a posição do comando: {in_text_str}',
            value=f'** **',
            inline=False)
        await ctx.reply(content=get_emoji_dance(), embed=embed, mention_author=False)

    @administracao_gp.command(name='remover_comando',
                              aliases=['remove_command', 'rc', 'removercomando', 'removecommand'])
    @permissions.has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _remover_comando(self, ctx, *, comando: str = None):
        if comando is None:
            return await self.bot.send_help(ctx)
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        # vai verificar se o comando está no banco
        # aliás, pra remover o comando, ele precisa existir no banco
        comando_personalizado = ComandoPersonalizado(servidor, comando.lower(), '', False)
        if comando_personalizado not in [cmd for cmd in
                                         await ComandoPersonalizadoRepository().get_commands(self.bot.db_connection,
                                                                                             servidor)]:
            return await ctx.reply(f'{self.bot.get_emoji("atencao")} Este comando não existe!')
        await ComandoPersonalizadoRepository().delete(self.bot.db_connection, comando_personalizado)
        embed = discord.Embed(title=f'Comando removido com sucesso!',
                              colour=discord.Colour.random(),
                              description=f'Comando: {comando}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar.url)
        return await ctx.reply(content=get_emoji_dance(), embed=embed, mention_author=False)

    @administracao_gp.command(name='modificar_comando',
                              aliases=['update_command', 'mc', 'modificarcomando', 'updatecommand'])
    @permissions.has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _modificar_comando(self, ctx, comando='', resposta='', in_text='t'):
        in_text = convert_to_bool(in_text)
        if in_text is None:
            await ctx.reply(f'Valor ``{in_text}`` inválido! Os valores que eu aceito são: sim, não, yes, no, 0, 1')
            return
        if ctx.message.content.count('"') != 4:
            return await ctx.reply('Parece que você digitou o comando errado!\nVocê deve usar o comando assim:\n' +
                                   f'{ctx.prefix}modificar_comando **"**comando**"** **"**resposta**"**')
        if (comando.replace(' ', '') == '') or (resposta.replace(' ', '') == ''):
            return await self.bot.send_help(ctx)
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        comando_personalizado = ComandoPersonalizado(servidor,
                                                     comando.lower(),
                                                     resposta,
                                                     in_text)
        # vai verificar se o comando está no banco
        # aliás, pra modificar o comando, ele precisa existir no banco
        if comando_personalizado not in [cmd for cmd in
                                         await ComandoPersonalizadoRepository().get_commands(self.bot.db_connection,
                                                                                             servidor)]:
            return await ctx.reply(f'{self.bot.get_emoji("atencao")} Este comando não existe!')
        await ComandoPersonalizadoRepository().update(self.bot.db_connection, comando_personalizado)
        in_text_str = capitalize(convert_to_string(in_text))
        embed = discord.Embed(title=f'Comando modificado com sucesso!', colour=discord.Colour.random(),
                              description=f'Comando: {comando}\nResposta: {resposta}\n'
                                          f'Ignorar a posição do comando: {in_text_str}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar.url)
        await ctx.reply(content=get_emoji_dance(), embed=embed, mention_author=False)


def setup(bot):
    cog = Admin(bot)
    cmds = f'{Fore.BLUE}{len(list(cog.walk_commands()))}{Fore.LIGHTMAGENTA_EX}'
    print(f'{Style.BRIGHT}{Fore.GREEN}[{"COG LOADED":^16}]' +
          f'{Fore.LIGHTMAGENTA_EX}{cog.qualified_name}({cmds}){Style.RESET_ALL}'.rjust(60))
    bot.add_cog(cog)
