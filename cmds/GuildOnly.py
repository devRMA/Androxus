# -*- coding: utf-8 -*-
# Androxus bot
# GuildOnly.py
# source: https://github.com/AlexFlipnote/discord_bot.py/blob/master/cogs/discord.py

__author__ = 'Rafael'

import asyncio
from datetime import datetime
from random import choice

import discord
from discord.ext import commands

from Classes import Androxus
from Classes.erros import InvalidArgument
from database.Repositories.ServidorRepository import ServidorRepository
from utils import permissions
from utils.Utils import random_color, capitalize, datetime_format, get_most_similar_items_with_similarity, \
    prettify_number, find_user


class GuildOnly(commands.Cog, command_attrs=dict(category='info')):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.Androxus.Androxus): Instância do bot

        """
        self.bot = bot

    @Androxus.comando(name='avatar',
                      aliases=['av'],
                      description='Eu vou mandar a foto de perfil da pessoa que você marcar.',
                      parameters=['[usuário (padrão: quem usou o comando)]'],
                      examples=['``{prefix}avatar`` {author_mention}'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _avatar(self, ctx, *args):
        # se a pessoa usou o comando mencionando o bot
        if ctx.prefix.replace('!', '').replace(' ', '') == self.bot.user.mention:
            # se a pessoa marcou o bot apenas 1 vez
            if ctx.message.content.replace('!', '').count(self.bot.user.mention) == 1:
                # vai tirar a menção da mensagem
                ctx.message.mentions.pop(0)
        if ctx.message.mentions:  # se tiver alguma menção na mensagem
            embed = discord.Embed(title=f'Avatar do(a) {str(ctx.message.mentions[0])}!',
                                  colour=discord.Colour(random_color()),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
            embed.set_image(url=ctx.message.mentions[-1].avatar_url)
            return await ctx.send(embed=embed)
        else:  # se a pessoa não mencionou ninguém, entra aqui
            if args:  # se a pessoa passou pelo menos alguma coisa
                if len(args) == 1:  # se a pessoa passou 1item
                    try:  # vai tentar converter o argumento para int
                        id_de_quem_ver_o_avatar = int(args[0])  # conversão
                        # se chegou aqui, vai tentar pegar o usuário com esse id
                        user = self.bot.get_user(id_de_quem_ver_o_avatar)
                        # se o bot não achou um user, ele vai pega pela API do discord
                        if user is None:
                            try:
                                user = await self.bot.fetch_user(id_de_quem_ver_o_avatar)
                            except discord.errors.NotFound:
                                user = None
                            except discord.HTTPException:
                                user = None
                        # se mesmo assim, não achar o user
                        if user is None:
                            return await ctx.send(f'{ctx.author.mention} não consegui um usuário com este id!')
                        # vai mandar o avatar desta pessoa
                        e = discord.Embed(title=f'Avatar do(a) {str(user)}!',
                                          colour=discord.Colour(random_color()),
                                          timestamp=datetime.utcnow())
                        e.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                        e.set_image(url=user.avatar_url)
                        return await ctx.send(embed=e)
                    except ValueError:  # se der erro, é porque a pessoa não passou apenas números
                        pass
                # se chegou até aqui, é porque a pessoa não passou um id ou passou mais de 1 item
                user = None
                args = ' '.join(args)
                # listas que vão ser usadas caso a pessoa digite um nome inválido
                name = []
                name_tag = []
                nickname = []
                if ctx.guild:
                    for member in ctx.guild.members:
                        # se a pessoa tiver um nick
                        if member.nick is not None:
                            # vai ver se a pessoa digitou esse nick
                            if member.nick.lower() == args.lower():
                                user = member
                                break
                            nickname.append(member.nick.lower())
                        # se a pessoa passou o nome, nome#tag de algum membro:
                        if (args.lower() == member.name.lower()) or (args.lower() == str(member).lower()):
                            user = member
                            break
                        name.append(member.name.lower())
                        name_tag.append(str(member).lower())
                # se não achou a pessoa na guild
                if user is None:
                    for _user in self.bot.users:
                        # se a pessoa passou o nome ou nome#tag de algum user que o bot tem acesso:
                        if (args.lower() == _user.name) or (args.lower() == str(_user)):
                            user = _user
                            break
                        name.append(_user.name.lower())
                        name_tag.append(str(_user).lower())
                # se o bot não achou a pessoa
                if user is None:
                    # vai passar para set, apenas para eliminar itens repetidos
                    name = list(set(name))
                    name_tag = list(set(name_tag))
                    nickname = list(set(nickname))
                    msg = f'{ctx.author.mention} Eu não achei nenhum usuário com este nome/nick.'
                    user_by_nick = get_most_similar_items_with_similarity(args, nickname)
                    # se veio pelo menos 1 user pelo nick
                    if user_by_nick:
                        # vai pegar o nick mais parecido que veio, e se a similaridade for maior que 60%:
                        if user_by_nick[0][-1] > 0.6:
                            msg += f'\nVocê quis dizer `{user_by_nick[0][0]}` ?'
                            return await ctx.send(msg)
                    # se não passou pelo return de cima, vai ver se acha algum nome parecido com o que a pessoa
                    # digitou
                    user_by_name_tag = get_most_similar_items_with_similarity(args, name_tag)
                    # se veio pelo menos 1 user pelo nametag
                    if user_by_name_tag:
                        # se for pelo menos 60% similar:
                        if user_by_name_tag[0][-1] > 0.6:
                            msg += f'\nVocê quis dizer `{user_by_name_tag[0][0]}` ?'
                            return await ctx.send(msg)
                    # se não passou pelo return de cima, vai ver se acha algum user#tag parecido com o que a pessoa
                    # digitou
                    user_by_name = get_most_similar_items_with_similarity(args, name)
                    # se veio pelo menos 1 user pelo nametag
                    if user_by_name:
                        # vai pegar o nome mais parecido que veio e se a similaridade for maior que 60%:
                        if user_by_name[0][-1] > 0.6:
                            msg += f'\nVocê quis dizer `{user_by_name[0][0]}` ?'
                            return await ctx.send(msg)
                    # se não passou por nenhum if de cima, vai mandar a mensagem dizendo que não achou
                    return await ctx.send(msg)
                # se chegou aqui, vai mandar o avatar do user
                e = discord.Embed(title=f'Avatar do(a) {str(user)}!',
                                  colour=discord.Colour(random_color()),
                                  timestamp=datetime.utcnow())
                e.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                e.set_image(url=user.avatar_url)
                return await ctx.send(embed=e)
            else:  # se a pessoa não passou nenhum argumento:
                embed = discord.Embed(title=f'Seu avatar!',
                                      colour=discord.Colour(random_color()),
                                      timestamp=datetime.utcnow())
                embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
                embed.set_image(url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)

    @Androxus.comando(name='userinfo',
                      aliases=['profile', 'memberinfo', 'ui'],
                      description='Eu vou mandar o máximo de informações sobre um usuário.',
                      parameters=['[usuário (padrão: quem usou o comando)]'],
                      examples=['``{prefix}userinfo`` {author_mention}'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _userinfo(self, ctx, *args):
        try:
            user = None
            # se a pessoa usou o comando mencionando o bot
            if ctx.prefix.replace('!', '').replace(' ', '') == self.bot.user.mention:
                # se a pessoa marcou o bot apenas 1 vez
                if ctx.message.content.replace('!', '').count(self.bot.user.mention) == 1:
                    # vai tirar a menção da mensagem
                    ctx.message.mentions.pop(0)
            if ctx.message.mentions:  # se tiver alguma menção na mensagem
                user = ctx.message.mentions[-1]  # vai pegar a primeira menção
            else:  # se a pessoa não mencionou ninguém, entra aqui
                if args:  # se a pessoa passou pelo menos alguma coisa
                    try:  # vai tentar converter o primeiro argumento para int
                        id_user = int(args[0])  # conversão
                        if ctx.guild:
                            user = ctx.guild.get_member(id_user)  # vai tentar pegar o membro do server com esse id
                        if user is None:  # se não achou na guild, vai ver se o bot acha
                            user = self.bot.get_user(id_user)
                        # se o bot não achou um user, ele vai pega pela API do discord
                        if user is None:
                            try:
                                user = await self.bot.fetch_user(id_user)
                            except discord.errors.NotFound:
                                user = None
                            except discord.HTTPException:
                                user = None
                        # se mesmo assim, não achar o user
                        if user is None:
                            return await ctx.send(f'{ctx.author.mention} não consegui um usuário com este id!')
                    except ValueError:  # se der erro, é porque a pessoa não passou número no primeiro argumento
                        user = None
                    # se o user for None
                    if user is None:
                        # se entrou aqui, é o user ainda não foi achado
                        args = ' '.join(args)
                        # listas que vão ser usadas caso a pessoa digite um nome inválido
                        name = []
                        name_tag = []
                        nickname = []
                        # se o comando foi usado de um servidor:
                        if ctx.guild:
                            # vai procurar o membro passado pela pessoa
                            for member in ctx.guild.members:
                                # se a pessoa tiver um nick
                                if member.nick is not None:
                                    # vai ver se a pessoa digitou esse nick
                                    if member.nick.lower() == args.lower():
                                        user = member
                                        break
                                    # lista que vai ser usada caso não ache o membro
                                    nickname.append(member.nick.lower())
                                # se a pessoa passou o nome ou nome#tag de algum membro:
                                if (args.lower() == member.name.lower()) or (args.lower() == str(member).lower()):
                                    user = member
                                    break
                                # listas que vão ser usadas caso não ache o membro
                                name.append(member.name.lower())
                                name_tag.append(str(member).lower())
                        # se não achou a pessoa na guild
                        if user is None:
                            # vai ver se o bot acha a pessoa
                            for _user in self.bot.users:
                                # se a pessoa passou o nome ou nome#tag de algum user que o bot tem acesso:
                                if (args.lower() == _user.name) or (args.lower() == str(_user)):
                                    user = _user
                                    break
                                name.append(_user.name.lower())
                                name_tag.append(str(_user).lower())
                        # se o bot não achou nem o membro nem a pessoa
                        if user is None:
                            # é passado para um set, apenas para eliminar os itens repetidos
                            name = list(set(name))
                            name_tag = list(set(name_tag))
                            nickname = list(set(nickname))
                            # mensagem padrão
                            msg = f'{ctx.author.mention} Eu não achei nenhum usuário com este nome/nick.'
                            user_by_nick = get_most_similar_items_with_similarity(args, nickname)
                            # se veio pelo menos 1 user pelo nick
                            if user_by_nick:
                                # vai pegar o nick mais parecido que veio, e se a similaridade for maior que 60%:
                                if user_by_nick[0][-1] > 0.6:
                                    msg += f'\nVocê quis dizer `{capitalize(user_by_nick[0][0])}` ?'
                                    raise InvalidArgument(msg=msg)
                            # se não passou pelo return de cima, vai ver se acha algum nome parecido
                            # com o que a pessoa digitou
                            user_by_name_tag = get_most_similar_items_with_similarity(args, name_tag)
                            # se veio pelo menos 1 user pelo nametag
                            if user_by_name_tag:
                                # se for pelo menos 60% similar:
                                if user_by_name_tag[0][-1] > 0.6:
                                    msg += f'\nVocê quis dizer `{capitalize(user_by_name_tag[0][0])}` ?'
                                    raise InvalidArgument(msg=msg)
                            # se não passou pelo return de cima, vai ver se acha algum user#tag parecido com o
                            # que a pessoa digitou
                            user_by_name = get_most_similar_items_with_similarity(args, name)
                            # se veio pelo menos 1 user pelo nametag
                            if user_by_name:
                                # vai pegar o nome mais parecido que veio e se a similaridade for maior que 60%:
                                if user_by_name[0][-1] > 0.6:
                                    msg += f'\nVocê quis dizer `{capitalize(user_by_name[0][0])}` ?'
                                    raise InvalidArgument(msg=msg)
                            # se não passou por nenhum if de cima, vai mandar a mensagem dizendo que não achou
                            raise InvalidArgument(msg=msg)
                else:  # se a pessoa não passou nenhum argumento:
                    user = ctx.author
            roles = None
            if hasattr(user, 'roles'):
                roles = None
                if len(user.roles) > 1:
                    roles = []
                    for role in sorted(user.roles, key=lambda r: r.position, reverse=True):
                        if role.id != ctx.guild.default_role.id:
                            roles.append(role)
                    roles_mention = ', '.join([f'<@&{c}>' for c in map(lambda x: x.id, roles)])
                    roles_name = None
                    if len(roles_mention) > 1000:
                        roles_name = ', '.join([f'`{c}`' for c in map(lambda x: x.name, roles)])
                    if roles_name is not None and len(roles_name) > 1000:
                        roles_name = f'{roles_name[:1000]}...'
                    roles = roles_mention if roles_name is None else roles_name
            if hasattr(user, 'top_role'):
                cor = user.top_role.colour.value
            else:
                cor = discord.Colour(random_color())
            info2 = None
            badges = ''
            pf = user.public_flags
            if ctx.guild:
                if ctx.guild.owner_id == user.id:
                    badges += '👑'
            if pf.staff:
                badges += self.bot.emoji('staff_badge')
            if pf.partner:
                badges += self.bot.emoji('parceiro_badge')
            if pf.hypesquad:
                badges += self.bot.emoji('hs_badge')
            if pf.bug_hunter or pf.bug_hunter_level_2:
                badges += self.bot.emoji('bug_hunter_badge')
            if pf.hypesquad_bravery:
                badges += self.bot.emoji('hs_bravery_badge')
            if pf.hypesquad_brilliance:
                badges += self.bot.emoji('hs_brilliance_badge')
            if pf.hypesquad_balance:
                badges += self.bot.emoji('hs_balance_badge')
            if pf.early_supporter:
                badges += self.bot.emoji('early_supporter_badge')
            if user.bot:
                badges += self.bot.emoji('bot_badge')
            if pf.verified_bot_developer or pf.early_verified_bot_developer:
                badges += self.bot.emoji('dev_badge')
            # como o discord não deixar bots verem o profile do user
            # e no profile que diz se a pessoa tem nitro, vamos ver se 
            # ela tem um gif no avatar, se tiver, ela tem nitro
            # ou vamos ver se ela está dando boost no servidor
            if user.is_avatar_animated():
                badges += self.bot.emoji('nitro')
            elif hasattr(user, 'premium_since'):
                if user.premium_since is not None:
                    badges += self.bot.emoji('nitro')
            if hasattr(user, 'premium_since'):
                if user.premium_since is not None:
                    badges += self.bot.emoji('boost')
            status = ''
            if hasattr(user, 'raw_status'):
                if user.raw_status == 'online':
                    status = self.bot.emoji('online')
                elif user.raw_status == 'dnd':
                    status = self.bot.emoji('dnd')
                elif user.raw_status == 'idle':
                    status = self.bot.emoji('idle')
                elif (user.raw_status == 'offline') or (user.raw_status == 'invisible'):
                    status = self.bot.emoji('offline')
            info1 = discord.Embed(title=f'{badges} {user.display_name} {status}',
                                  colour=cor,
                                  timestamp=datetime.utcnow())
            info1.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
            info1.set_thumbnail(url=user.avatar_url)
            info1.add_field(name="📑 Nome e tag:", value=f'`{user}`', inline=True)
            info1.add_field(name="🆔 Id: ", value=f'``{user.id}``', inline=True)
            if hasattr(user, 'raw_status') and (not user.bot):
                # se a pessoa não estiver offline ou invisivel
                if (user.raw_status != 'offline') and (user.raw_status != 'invisible') and (not user.bot):
                    if user.is_on_mobile():
                        plataforma = '📱 Celular'
                    else:
                        if user.web_status.value != 'offline':
                            plataforma = '💻 Pc ─ usando o site 🌐'
                        else:
                            plataforma = '💻 Pc ─ usando o discord desktop 🖥'
                    info1.add_field(name="🕵️ Está acessando o discord pelo:", value=f'``{plataforma}``', inline=True)
            if hasattr(user, 'activities'):
                activities = user.activities
                streaming = False
                custom = False
                playing = False
                if len(activities) != 0:
                    for activity in activities:
                        if (activity.type.name == 'streaming') and (not streaming):
                            info1.add_field(name=f'{self.bot.emoji("streaming")} Fazendo live',
                                            value=f'**🎙 Plataforma**: `{activity.platform}`\n'
                                                  f'**🏷 Nome da live**: `{activity.name}`\n'
                                                  f'**🕛 Começou**: `{datetime_format(activity.created_at)}`',
                                            inline=True)
                            streaming = True
                        elif (activity.type.name == 'custom') and (not custom):
                            if (activity.emoji is not None) or (activity.name is not None):
                                if activity.emoji is not None:
                                    if activity.emoji.id in [c.id for c in self.bot.emojis]:
                                        emoji = f'{activity.emoji}'
                                    else:
                                        emoji = f'❓'
                                else:
                                    emoji = '`🚫 Nulo`'
                                if activity.name is not None:
                                    texto = f'`{activity.name}`'
                                else:
                                    texto = '`🚫 Nulo`'
                                info1.add_field(name=f'{self.bot.emoji("disco")} Status personalizado',
                                                value=f'🔰 Emoji: {emoji}\n'
                                                      f'🖋 Frase: {texto}',
                                                inline=True)
                                custom = True
                        elif (activity.type.name == 'playing') and (not playing):
                            if activity.start is not None:
                                value = f'`{activity.name}`\n**🕛 Começou a jogar:**\n' + \
                                        f'`{datetime_format(activity.start)}`'
                            else:
                                value = f'`{activity.name}`'
                            info1.add_field(name='🕹 Jogando',
                                            value=value,
                                            inline=True)
                            playing = True
            if hasattr(user, 'nick'):
                if user.nick is not None:
                    info1.add_field(name="🔄 Nickname", value=f'``{user.nick}``', inline=True)
            info1.add_field(name="🗓 Conta criada em:",
                            value=f'``{user.created_at.strftime("%d/%m/%Y")}``({datetime_format(user.created_at)})',
                            inline=True)
            if hasattr(user, 'joined_at'):
                rank_members = [str(c) for c in sorted(user.guild.members, key=lambda x: x.joined_at)]
                info1.add_field(name="📥 Entrou no servidor em:",
                                value=f'`{user.joined_at.strftime("%d/%m/%Y")}`({datetime_format(user.joined_at)})'
                                      f'\n**🏆 Está na `{prettify_number(rank_members.index(str(user)) + 1)}°` posição, '
                                      'no rank dos membros mais antigos!**',
                                inline=True)
                if user.premium_since is not None:
                    info1.add_field(
                        name=f'{self.bot.emoji("boost")} Começou a dar boost neste servidor em:',
                        value=f'`{user.premium_since.strftime("%d/%m/%Y")}`('
                              f'{datetime_format(user.premium_since)})',
                        inline=True)
                # só vai mostrar as permissões da pessoa, se ela estiver no server
                info2 = discord.Embed(title=f'{badges} {user.display_name}',
                                      colour=cor,
                                      timestamp=datetime.utcnow())
                info2.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
                info2.set_thumbnail(url=user.avatar_url)
                if roles is not None:
                    info2.add_field(name=f'🏅 Cargos({len(roles.split(", "))}):', value=roles, inline=False)
                all_perms = user.permissions_in(ctx.message.channel)
                perms = []
                for atributo in dir(all_perms):
                    if isinstance(getattr(all_perms, atributo), bool):
                        if getattr(all_perms, atributo):
                            perms.append(atributo)
                perms_traduzidas = {
                    'add_reactions': 'adicionar reações',
                    'administrator': 'administrador',
                    'attach_files': 'anexar arquivos',
                    'ban_members': 'banir membros',
                    'change_nickname': 'mudar apelido',
                    'create_instant_invite': 'criar convite',
                    'embed_links': 'enviar links',
                    'kick_members': 'expulsar membros',
                    'manage_channels': 'gerenciar canais',
                    'manage_emojis': 'gerenciar emojis',
                    'manage_guild': 'gerenciar servidor',
                    'manage_messages': 'gerenciar mensagens',
                    'manage_nicknames': 'gerenciar apelidos',
                    'manage_permissions': 'gerenciar permissões',
                    'manage_roles': 'gerenciar cargos',
                    'manage_webhooks': 'gerenciar webhooks',
                    'mention_everyone': 'mencionar everyone',
                    'read_message_history': 'ler histórico de mensagens',
                    'read_messages': 'ver mensagens',
                    'send_messages': 'enviar mensagens',
                    'send_tts_messages': 'enviar mensagem com tts',
                    'view_audit_log': 'ver registro de auditoria',
                    'view_channel': 'ver canal',
                    'view_guild_insights': 'ver desempenho do servidor',
                    'use_external_emojis': 'usar emojis externos'
                }
                for c in range(0, len(perms)):
                    # vai substituir os "_" por espaços e tirar o external_emojis
                    for perm_traducao in perms_traduzidas.items():
                        if perm_traducao[0] == perms[c]:
                            perms[c] = f"``{perm_traducao[-1]}``"
                            break
                if 'external_emojis' in perms:
                    perms.pop(perms.index('external_emojis'))
                if len(perms) >= 1:
                    info2.add_field(name=f'📌 Permissões neste chat({len(perms)}):',
                                    value=capitalize(', '.join(perms)), inline=False)
                else:
                    info2.add_field(name=f'📌 Permissão neste chat(0):',
                                    value='Este usuário não tem nenhuma permissão, neste chat!', inline=False)
        except InvalidArgument as erro:
            return await ctx.send(erro.msg)

        async def menus_user_info(ctx, msg):

            def check_page1(reaction, user, msg):  # fica verificando a pagina 1, para ver se é para ir para a pagina 2
                user_check = user.id == ctx.author.id
                reaction_check = str(reaction.emoji) == '➡'
                msg_check = msg.id == reaction.message.id
                return user_check and reaction_check and msg_check

            def check_page2(reaction, user, msg):  # fica verificando a pagina 2, para ver se é para ir para a pagina 1
                user_check = user.id == ctx.author.id
                reaction_check = str(reaction.emoji) == '⬅'
                msg_check = msg.id == reaction.message.id
                return user_check and reaction_check and msg_check

            async def check_reactions_without_perm(ctx, bot, msg):
                while True:
                    while True:
                        reaction, user = await bot.wait_for('reaction_add', timeout=900.0)
                        if check_page1(reaction, user, msg):
                            break
                    await msg.delete()
                    msg = await ctx.send(embed=info2)
                    await msg.add_reaction('⬅')
                    while True:
                        reaction, user = await bot.wait_for('reaction_add', timeout=900.0)
                        if check_page2(reaction, user, msg):
                            break
                    await msg.delete()
                    msg = await ctx.send(embed=info1)
                    await msg.add_reaction('➡')

            async def check_reactions_with_perm(bot, msg):
                while True:
                    while True:
                        reaction, user = await bot.wait_for('reaction_add', timeout=900.0)
                        if check_page1(reaction, user, msg):
                            break
                    await msg.clear_reactions()
                    await msg.add_reaction('⬅')
                    await msg.edit(embed=info2)
                    while True:
                        reaction, user = await bot.wait_for('reaction_add', timeout=900.0)
                        if check_page2(reaction, user, msg):
                            break
                    await msg.clear_reactions()
                    await msg.add_reaction('➡')
                    await msg.edit(embed=info1)

            # se o bot tiver perm pra usar o "clear_reactions"
            if ctx.guild.me.guild_permissions.manage_messages:
                await check_reactions_with_perm(self.bot, msg)
            else:  # se o bot não tiver permissão:
                await check_reactions_without_perm(ctx, self.bot, msg)

        msg_bot = await ctx.send(embed=info1)
        if info2:
            # se tiver o info2, significa que foi usado num servidor
            await msg_bot.add_reaction('➡')
            try:
                # vai fica 1 minuto e meio esperando o usuário apertas nas reações
                await asyncio.wait_for(menus_user_info(ctx, msg_bot), timeout=90.0)
            except asyncio.TimeoutError:  # se acabar o tempo
                pass

    @Androxus.comando(name='splash',
                      aliases=['fundo_convite'],
                      description='Eu vou enviar a imagem de fundo do convite deste servidor (se tiver).',
                      examples=['``{prefix}splash``'])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _splash(self, ctx):
        if ctx.guild.splash_url:
            embed = discord.Embed(title=f'Splash deste servidor!',
                                  colour=discord.Colour(random_color()),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
            embed.set_image(url=ctx.guild.splash_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'{ctx.author.mention} este servidor não tem uma foto de fundo no convite! ;-;')

    @Androxus.comando(name='discovery_splash',
                      description='Eu vou enviar discovery splash deste servidor (se tiver).',
                      examples=['``{prefix}discovery_splash``'])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _discovery_splash(self, ctx):
        if ctx.guild.discovery_splash_url:
            embed = discord.Embed(title=f'discovery splash deste servidor!',
                                  colour=discord.Colour(random_color()),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_image(url=ctx.guild.discovery_splash_url)
            return await ctx.send(embed=embed)
        else:
            return await ctx.send(f'{ctx.author.mention} este servidor não tem discovery splash ;-;')

    @Androxus.comando(name='serverinfo',
                      aliases=['guildinfo', 'si'],
                      description='Eu vou mandar o máximo de informações sobre um servidor.',
                      examples=['``{prefix}serverinfo``'])
    @commands.guild_only()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _serverinfo(self, ctx):
        bots = 0
        for member in ctx.guild.members:
            if member.bot:
                bots += 1
        embed = discord.Embed(title=f'Informações sobre este servidor!',
                              colour=discord.Colour(random_color()),
                              description='O máximo de informação que eu consegui encontrar sobre este servidor.',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')

        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon_url)
        if ctx.guild.banner:
            embed.set_image(url=ctx.guild.banner_url)
        elif ctx.guild.splash_url:
            embed.set_image(url=ctx.guild.splash_url)
        elif ctx.guild.discovery_splash_url:
            embed.set_image(url=ctx.guild.discovery_splash_url)

        embed.add_field(name='🪧 Servidor', value=f'`{ctx.guild.name}` ({ctx.guild.id})', inline=True)
        if ctx.guild.description:
            embed.add_field(name='📕 Descrição do servidor', value=f'{ctx.guild.description}', inline=True)
        embed.add_field(name='👑 Dono', value=f'`{ctx.guild.owner}` ({ctx.guild.owner_id})', inline=True)
        embed.add_field(name=f'👥 Membros ({prettify_number(ctx.guild.member_count)})',
                        value=f'🧍 Pessoas: {prettify_number(ctx.guild.member_count - bots)}\n'
                              f'🤖 Bots: {prettify_number(bots)}', inline=True)
        embed.add_field(name='🙂 Emojis', value=f'{prettify_number(len(ctx.guild.emojis))}', inline=True)
        embed.add_field(name=f'💬 Canais ('
                             f'{prettify_number(len(ctx.guild.text_channels) + len(ctx.guild.voice_channels))})',
                        value=f'📖 Chat: {prettify_number(len(ctx.guild.text_channels))}\n'
                              f'🗣 Voz: {prettify_number(len(ctx.guild.voice_channels))}',
                        inline=True)
        embed.add_field(name='🏅 Cargos', value=f'{prettify_number(len(ctx.guild.roles))}', inline=True)
        embed.add_field(name='🗺 Região', value=f'{str(ctx.guild.region).capitalize()}', inline=True)
        embed.add_field(name='📅 Criado em:',
                        value=f'{ctx.guild.created_at.strftime("%d/%m/%Y")}\n'
                              f'({datetime_format(ctx.guild.created_at)})', inline=True)
        rank_members = [str(c) for c in sorted(ctx.guild.members, key=lambda x: x.joined_at)]
        embed.add_field(name='📥 Entrei aqui em:',
                        value=f'`{ctx.guild.me.joined_at.strftime("%d/%m/%Y")}`\n'
                              f'({datetime_format(ctx.guild.me.joined_at)})\n'
                              f'Estou na posição `{prettify_number(rank_members.index(str(ctx.guild.me)) + 1)}°` no '
                              'rank dos membros mais antigos.',
                        inline=True)
        await ctx.send(embed=embed)

    @Androxus.comando(name='server_avatar',
                      aliases=['icone', 'icon', 'sa'],
                      description='Eu vou enviar o icone do servidor (se tiver).',
                      examples=['``{prefix}server_avatar``'])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _server_avatar(self, ctx):
        if not ctx.guild.icon:
            return await ctx.send("Este servidor não tem icone.")
        embed = discord.Embed(title=f'Icone deste servidor!',
                              colour=discord.Colour(random_color()),
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_image(url=ctx.guild.icon_url_as(size=1024))
        await ctx.send(embed=embed)

    @Androxus.comando(name='server_banner',
                      aliases=["banner", 'sb'],
                      description='Eu vou enviar o banner do servidor (se tiver).',
                      examples=['``{prefix}server_banner``'])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _server_banner(self, ctx):
        if not ctx.guild.banner:
            return await ctx.send("Este servidor não tem banner.")
        embed = discord.Embed(title=f'Banner deste servidor!',
                              colour=discord.Colour(random_color()),
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_image(url=ctx.guild.banner_url)
        await ctx.send(embed=embed)

    @Androxus.comando(name='configs',
                      aliases=['configurações', 'configuraçoes', 'settings'],
                      description='Eu vou mostrar todos as configurações deste servidor.',
                      examples=['``{prefix}configs``'])
    @commands.guild_only()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _configs(self, ctx):
        servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
        e = discord.Embed(title=f'Todas as configurações deste servidor!',
                          colour=discord.Colour(random_color()),
                          timestamp=datetime.utcnow())
        e.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        if ctx.guild.icon:
            e.set_thumbnail(url=ctx.guild.icon_url)
        if ctx.guild.banner:
            e.set_image(url=ctx.guild.banner_url)
        elif ctx.guild.splash_url:
            e.set_image(url=ctx.guild.splash_url)
        elif ctx.guild.discovery_splash_url:
            e.set_image(url=ctx.guild.discovery_splash_url)
        e.add_field(name=f'Prefixo',
                    value=f'{servidor.prefixo}',
                    inline=True)
        if servidor.sugestao_de_comando:
            sugestao_cmd = self.bot.emoji('ativado')
        else:
            sugestao_cmd = self.bot.emoji('desativado')
        e.add_field(name=f'Sugestao de comando',
                    value=sugestao_cmd,
                    inline=True)
        if servidor.channel_id_log is not None:
            e.add_field(name=f'Log',
                        value=f'{self.bot.emoji("ativado")}\nEm: <#{servidor.channel_id_log}>',
                        inline=True)
            logs = []
            if servidor.mensagem_deletada:
                logs.append('``mensagem deletada``')
            if servidor.mensagem_editada:
                logs.append('``mensagem editada``')
            if servidor.avatar_alterado:
                logs.append('``avatar alterado``')
            if servidor.nome_alterado:
                logs.append('``nome alterado``')
            if servidor.tag_alterado:
                logs.append('``tag alterada``')
            if servidor.nick_alterado:
                logs.append('``nick alterado``')
            if servidor.role_alterado:
                logs.append('``cargo adicionado/removido``')
            if len(logs) != 0:
                e.add_field(name=f'Logs ativos',
                            value=capitalize(', '.join(logs)),
                            inline=True)
        else:
            e.add_field(name=f'Log',
                        value=f'{self.bot.emoji("desativado")}',
                        inline=True)
        await ctx.send(embed=e)

    @Androxus.comando(name='joinrank',
                      aliases=['oldmembersrank', 'jr', 'membrosantigos'],
                      description='Eu vou mostrar o rank com os membros mais antigos do servidor.',
                      parameters=['["-r" (membro aleatorio) | usuário (padrão: autor)]'],
                      examples=['``{prefix}joinrank``',
                                '``{prefix}jr`` ``-r``',
                                '``{prefix}jr`` ``androxus``'],
                      hidden=True)
    @commands.guild_only()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _joinrank(self, ctx, *, args=None):
        if args is None:
            member = ctx.author
        else:
            members = find_user(args, ctx.guild.members, 0.6)
            if (len(members) == 0) or (len(members) == len(ctx.guild.members)):
                if args == '-r':
                    member = choice(ctx.guild.members)
                else:
                    return await ctx.send('Não achei nenhum membro!')
            elif len(members) == 1:
                member = members[0]
            else:
                if len(members) >= 5:
                    msg = '\n'.join(f'{u} (ID: {u.id})' for u in members[:5])
                    msg += f'\nE outro(s) {len(members) - 5} resultado(s)...'
                else:
                    msg = '\n'.join(f'{u} (ID: {u.id})' for u in members)
                return await ctx.send(f'Encontrei mais de um membro!\n{msg}')
        members = sorted(ctx.guild.members, key=lambda x: x.joined_at)

        def get_pos(m):
            try:
                return members.index(m) + 1
            except:
                return -1

        def to_emoji(number):
            if number == 1:
                return ':first_place:'
            elif number == 2:
                return ':second_place:'
            elif number == 3:
                return ':third_place:'
            result = prettify_number(number)
            result = result.replace('0', ':zero:')
            result = result.replace('1', ':one:')
            result = result.replace('2', ':two:')
            result = result.replace('3', ':three:')
            result = result.replace('4', ':four:')
            result = result.replace('5', ':five:')
            result = result.replace('6', ':six:')
            result = result.replace('7', ':seven:')
            result = result.replace('8', ':eight:')
            result = result.replace('9', ':nine:')
            result = result.replace('.', ' ')
            return result

        if len(ctx.guild.members) >= 10:
            if get_pos(member) <= 5:
                selected = members[:10]
            else:
                selected = members[get_pos(member) - 5:get_pos(member) + 5]
        else:
            selected = members.copy()
        e = discord.Embed(title=f'Rank dos membros mais antigos!',
                          colour=discord.Colour(random_color()),
                          timestamp=datetime.utcnow())
        e.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        rank = ''
        for item in selected:
            rank += f'{to_emoji(get_pos(item))} '
            if item == member:
                rank += f'**{member}** ← '
            else:
                rank += f'{item} '
            if item == ctx.me:
                rank += '🤖'
            if item == ctx.guild.owner:
                rank += '👑'
            if item.id in self.bot.configs['owners']:
                rank += self.bot.emoji('dev_badge')
            rank += '\n'
        e.add_field(name=f'Este servidor tem {len(ctx.guild.members)} membros.',
                    value=rank)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(GuildOnly(bot))
