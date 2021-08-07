# -*- coding: utf-8 -*-
# Androxus bot
# Info.py
# source: https://github.com/AlexFlipnote/discord_bot.py/blob/master/cogs/discord.py

__author__ = 'Rafael'

import asyncio
from asyncio import sleep
from os import getpid
from sys import version
from time import monotonic

import discord
import psutil
from colorama import Fore, Style
from discord import ui, ButtonStyle
from discord.ext import commands
from discord.ui import Button
from stopwatch import Stopwatch

from Classes.General import DictForFormat
from EmbedGenerators.HelpCommand import embed_help_command
from EmbedGenerators.HelpGroup import embed_help_group
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.InformacoesRepository import InformacoesRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils.Utils import capitalize, datetime_format, prettify_number, get_most_similar_item, string_similarity, \
    cut_string
from utils.Utils import get_last_commit, get_prefix
from utils.Utils import get_last_update
from utils.converters import DiscordUser
from utils.permissions import is_owner


class Info(commands.Cog):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.General.Androxus): Instância do bot

        """
        self.bot = bot
        self.sr = ServidorRepository()
        self.cpr = ComandoPersonalizadoRepository()

    @commands.group(name='info', case_insensitive=True, invoke_without_command=True, ignore_extra=False,
                    aliases=['informações', 'informaçoes', 'informacões', 'informacoes', 'information'])
    async def info_gp(self, ctx):
        await ctx.reply(embed=await embed_help_group(ctx), mention_author=False)

    @info_gp.command(name='avatar', aliases=['av'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _avatar(self, ctx, *, user: DiscordUser = None):
        if user is None:
            user = ctx.author
        message = (await self.bot.translate(ctx, values_={
            'user': user
        }))[0]
        return await ctx.send(**message)

    @info_gp.command(name='userinfo', aliases=['profile', 'memberinfo', 'ui'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _userinfo(self, ctx, *, user: DiscordUser = None):
        emojis_badges = {
            'staff': self.bot.get_emoji('staff_badge'),
            'partner': self.bot.get_emoji('parceiro_badge'),
            'hypesquad': self.bot.get_emoji('hs_badge'),
            'bug_hunter': self.bot.get_emoji('bug_hunter_badge'),
            'hypesquad_bravery': self.bot.get_emoji('hs_bravery_badge'),
            'hypesquad_brilliance': self.bot.get_emoji('hs_brilliance_badge'),
            'hypesquad_balance': self.bot.get_emoji('hs_balance_badge'),
            'early_supporter': self.bot.get_emoji('early_supporter_badge'),
            'bug_hunter_level_2': self.bot.get_emoji('bug_hunter_badge'),
            'verified_bot_developer': self.bot.get_emoji('dev_badge')
        }
        perms = await self.bot.translate(ctx, others_='perms')
        others = await self.bot.translate(ctx, others_='userinfo', values_={
            'online': self.bot.get_emoji('online'),
            'dnd': self.bot.get_emoji('dnd'),
            'idle': self.bot.get_emoji('idle'),
            'offline': self.bot.get_emoji('offline'),
            'boost': self.bot.get_emoji('boost'),
            'hacking': self.bot.get_emoji('hacking'),
            'streaming': self.bot.get_emoji('streaming'),
            'disco': self.bot.get_emoji('disco')
        })
        lang = await self.bot.get_language(ctx)
        strftime = await self.bot.translate(ctx, others_='strftime')
        strftime = strftime.get('br' if lang != 'en_us' else 'us')
        if user is None:
            user = ctx.author
        color = discord.Colour.random().value
        if hasattr(user, 'roles'):
            for role in sorted(user.roles, key=lambda r: r.position, reverse=True):
                if role.id != ctx.guild.default_role.id and role.colour.value != 0:
                    color = role.colour.value
                    break
        badges = ''
        if ctx.guild and ctx.guild.owner_id == user.id:
            badges += '👑'
        if user.bot:
            badges += str(self.bot.get_emoji('bot_badge'))
        if hasattr(user, 'public_flags'):
            for flag_name, have in iter(user.public_flags):
                if have:
                    badges += str(emojis_badges.get(flag_name, ''))
        if user.avatar.is_animated() or (hasattr(user, 'premium_since') and user.premium_since is not None):
            badges += str(self.bot.get_emoji('nitro'))
        if hasattr(user, 'premium_since') and user.premium_since is not None:
            badges += str(self.bot.get_emoji('boost'))
        status_emoji = ''
        status_text = None
        if hasattr(user, 'raw_status'):
            status_emoji, status_text = others.get('status', {}).get(user.raw_status, '').split(' ', maxsplit=1)
        messages = await self.bot.translate(ctx, values_={
            'color': color,
            'badges': badges,
            'user': user,
            'status_emoji': status_emoji,
            'created_at_date': user.created_at.strftime(strftime),
            'created_at_formatted': datetime_format(user.created_at, lang=lang)
        })
        embeds_to_use = [0, 1]
        if hasattr(user, 'nick') and (user.nick is not None):
            messages[0].get('embed').add_field(name=others.get('embed1_field_name'), value=f'`{user.nick}`',
                                               inline=True)
        if hasattr(user, 'joined_at'):
            rank_members = [str(c) for c in sorted(user.guild.members, key=lambda x: x.joined_at)]
            embed2 = messages[1].get('embed')
            embed2_field_value = f'`{user.joined_at.strftime(strftime)}`({datetime_format(user.joined_at, lang=lang)})'
            embed2.add_field(name=others.get('embed2_field1_name'),
                             value=embed2_field_value,
                             inline=True)
            embed2_field_value = f'**{prettify_number(rank_members.index(str(user)) + 1)}°**/'
            embed2_field_value += f'{prettify_number(len(rank_members))}'
            embed2.add_field(name=others.get('embed2_field2_name'),
                             value=embed2_field_value,
                             inline=True)
            if user.premium_since is not None:
                embed2_field_value = f'`{user.premium_since.strftime(strftime)}`'
                embed2_field_value += f'({datetime_format(user.premium_since, lang=lang)})'
                embed2.add_field(name=others.get('embed2_field3_name'),
                                 value=embed2_field_value,
                                 inline=True)
        if hasattr(user, 'raw_status') and (user.raw_status != 'offline') and \
                (user.raw_status != 'invisible') and (not user.bot):
            embeds_to_use.append(2)
            embed3 = messages[2].get('embed')
            platforms = others.get('platforms')
            emoji_on = str(self.bot.get_emoji('ativado'))
            emoji_off = str(self.bot.get_emoji('desativado'))
            embed3_field_value = ''
            for platform_attr, platform_name in platforms.items():
                embed3_field_value += platform_name
                embed3_field_value += emoji_on if getattr(user, platform_attr).value != 'offline' else emoji_off
                embed3_field_value += '\n'
            embed3.add_field(name=others.get('embed3_field1_name'),
                             value=embed3_field_value,
                             inline=False)
            if status_text is not None:
                embed3.add_field(name=others.get('embed3_field2_name'),
                                 value=capitalize(status_text),
                                 inline=True)
            if hasattr(user, 'activities') and len(user.activities) > 0:
                activities = others.get('activities')
                for activity in user.activities:
                    if activity.type.name == 'streaming':
                        streaming_values = activities.get(activity.type.name)
                        embed3_field_value = streaming_values.get('value').format_map(DictForFormat({
                            'activity_p': activity.platform,
                            'activity_n': activity.name,
                            'created_at': datetime_format(activity.created_at, lang=lang)
                        }))
                        embed3.add_field(name=streaming_values.get('name'),
                                         value=embed3_field_value,
                                         inline=True)
                    elif activity.type.name == 'custom':
                        if activity.emoji or activity.name:
                            custom_values = activities.get(activity.type.name)
                            emoji = activity.emoji if activity.emoji else others.get('none')
                            txt = activity.name if activity.name else others.get('none')
                            embed3_field_value = custom_values.get('value').format_map(DictForFormat({
                                'emoji': emoji,
                                'txt': txt
                            }))
                            embed3.add_field(name=custom_values.get('name'),
                                             value=embed3_field_value,
                                             inline=False)
                    elif activity.type.name == 'playing':
                        playing_values = activities.get(activity.type.name)
                        embed3_field_value = f'`{activity.name}`'
                        if activity.start is not None:
                            embed3_field_value += playing_values.get('value').format_map(DictForFormat({
                                'started': datetime_format(activity.start, lang=lang)
                            }))
                        embed3.add_field(name=playing_values.get('name'),
                                         value=embed3_field_value,
                                         inline=True)
        if hasattr(user, 'roles') and len(user.roles) > 1:
            roles = [role for role in sorted(user.roles, key=lambda r: r.position, reverse=True)
                     if role.id != ctx.guild.default_role.id]
            roles_count = len(roles)
            if roles_count > 0:
                embeds_to_use.append(3)
                roles_mention = ', '.join(f'<@&{r.id}>' for r in roles)
                roles_name = None
                if len(roles_mention) > 1_000:
                    roles_name = ', '.join(f'`{r.name}`' for r in roles)
                if roles_name is not None and len(roles_name) > 1_000:
                    roles_name = cut_string(roles_name, width=1_000)
                roles = roles_name or roles_mention
                roles = f'**{roles}**'
                embed4 = messages[3].get('embed')
                embed4_field_name = others.get('embed4_field1_name').format_map(DictForFormat({
                    'roles_count': roles_count
                }))
                embed4.add_field(name=embed4_field_name,
                                 value=roles,
                                 inline=False)
                user_perms = ctx.message.channel.permissions_for(user)
                perms_user_have = []
                for perm_name, have in iter(user_perms):
                    if have:
                        perm = perms.get(perm_name)
                        if perm:
                            perms_user_have.append(f'`{perm}`')
                embed4_field_name = others.get('embed4_field2_name').format_map(DictForFormat({
                    'perms': len(perms_user_have)
                }))
                if len(perms_user_have) >= 1:
                    embed4_field_value = capitalize(', '.join(perms_user_have))
                else:
                    embed4_field_value = others.get('embed4_field2_value')
                embed4.add_field(name=embed4_field_name,
                                 value=embed4_field_value,
                                 inline=False)
        for pos, message in enumerate(messages):
            message.get('embed').set_footer(text=f'{ctx.author} ─ {pos + 1}/{len(embeds_to_use)}',
                                            icon_url=ctx.author.avatar.url)

        class UserinfoView(ui.View):
            def __init__(self, context: commands.Context, messages_to_send: list):
                super().__init__()
                self.ctx = context
                self.messages = messages_to_send
                for m in self.messages:
                    m['view'] = self
                self.last_interaction = monotonic()
                self.current_page = 0
                self.last_page = embeds_to_use[-1]

            async def interaction_check(self, interaction):
                can_use = self.ctx.author.id == interaction.user.id
                if not can_use:
                    erros = await self.ctx.bot.translate(ctx, error_='interaction', values_={
                        'atencao': self.ctx.bot.get_emoji('atencao'),
                        'display_name': interaction.user.display_name
                    })
                    await interaction.response.send_message(**erros[0])
                else:
                    self.last_interaction = monotonic()
                return can_use

            @ui.button(style=ButtonStyle.grey, emoji=self.bot.get_emoji('first_btn'), row=0)
            async def btn_first(self, button, interaction):
                if self.current_page > 0:
                    self.current_page = 0
                    await interaction.response.edit_message(**self.messages[self.current_page])

            @ui.button(style=ButtonStyle.grey, emoji=self.bot.get_emoji('back_btn'), row=0)
            async def btn_back(self, button, interaction):
                if self.current_page > 0:
                    self.current_page -= 1
                    if self.current_page in embeds_to_use:
                        await interaction.response.edit_message(**self.messages[self.current_page])
                    else:
                        self.current_page += 1
                else:
                    self.current_page = self.last_page
                    await interaction.response.edit_message(**self.messages[self.current_page])

            @ui.button(style=ButtonStyle.red, emoji=self.bot.get_emoji('stop_btn'), row=0)
            async def btn_stop(self, button, interaction):
                self.stop()

            @ui.button(style=ButtonStyle.grey, emoji=self.bot.get_emoji('next_btn'), row=0)
            async def btn_next(self, button, interaction):
                if self.current_page < self.last_page:
                    self.current_page += 1
                    if self.current_page in embeds_to_use:
                        await interaction.response.edit_message(**self.messages[self.current_page])
                    else:
                        self.current_page -= 1
                else:
                    self.current_page = 0
                    await interaction.response.edit_message(**self.messages[self.current_page])

            @ui.button(style=ButtonStyle.grey, emoji=self.bot.get_emoji('last_btn'), row=0)
            async def btn_last(self, button, interaction):
                if self.current_page < self.last_page:
                    self.current_page = self.last_page
                    await interaction.response.edit_message(**self.messages[self.current_page])

        view = UserinfoView(ctx, messages)
        for item in view.children:
            if isinstance(item, Button):
                if len(embeds_to_use) <= 2 and (str(item.emoji) == '⏮' or str(item.emoji) == '⏭'):
                    view.children.remove(item)
        msg = await ctx.reply(mention_author=False, **messages[0])
        timeout = 60.0
        while True:
            if view.last_interaction + timeout <= monotonic():
                view.stop()
            if view.is_finished():
                return await msg.edit(view=None)
            await sleep(0.01)

    @info_gp.command(name='splash', aliases=['fundo_convite', 'fundoconvite'])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _splash(self, ctx):
        if ctx.guild.splash:
            messages = await self.bot.translate(ctx)
            await ctx.send(**messages[0])
        else:
            erros = await self.bot.translate(ctx, error_='splash')
            await ctx.send(**erros[0])

    @info_gp.command(name='discovery_splash', aliases=['discoverysplash'])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _discovery_splash(self, ctx):
        if ctx.guild.discovery_splash:
            messages = await self.bot.translate(ctx)
            await ctx.send(**messages[0])
        else:
            erros = await self.bot.translate(ctx, error_='discovery_splash')
            await ctx.send(**erros[0])

    @info_gp.command(name='serverinfo', aliases=['server_info', 'guildinfo', 'guild_info', 'si'])
    @commands.guild_only()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _serverinfo(self, ctx):
        if not ctx.guild.chunked:
            await ctx.guild.chunk()
        message_to_send = 1 if ctx.guild.description else 0
        bots = 0
        categories = 0
        stages = 0
        txt_channels = 0
        voice_channels = 0
        nsfw = 0
        news = 0
        rank_members = []
        for member in sorted(ctx.guild.members, key=lambda x: x.joined_at):
            if member.bot:
                bots += 1
            rank_members.append(str(member))
        for c in ctx.guild.channels:
            if isinstance(c, discord.CategoryChannel):
                categories += 1
            elif isinstance(c, discord.TextChannel):
                txt_channels += 1
                if c.is_nsfw():
                    nsfw += 1
                if c.is_news():
                    news += 1
            elif isinstance(c, discord.VoiceChannel):
                voice_channels += 1
            elif isinstance(c, discord.StageChannel):
                stages += 1
        strftime = await self.bot.translate(ctx, others_='strftime')
        lang = await self.bot.get_language(ctx)
        strftime = strftime.get('br' if lang != 'en_us' else 'us')
        messages = await self.bot.translate(ctx, values_={
            'member_count': prettify_number(ctx.guild.member_count),
            'bots': prettify_number(bots),
            'people': prettify_number(ctx.guild.member_count - bots),
            'emojis': prettify_number(len(ctx.guild.emojis)),
            'categories': prettify_number(categories),
            'stages': prettify_number(stages),
            'stage': self.bot.get_emoji('stage'),
            'txt_channels': prettify_number(txt_channels),
            'voice_channels': prettify_number(voice_channels),
            'nsfw': prettify_number(nsfw),
            'news': prettify_number(news),
            'all_channels': prettify_number(stages + txt_channels + voice_channels),
            'roles': prettify_number(len(ctx.guild.roles)),
            'region': ctx.guild.region[0].capitalize(),
            'created_at_date': ctx.guild.created_at.strftime(strftime),
            'created_at_formatted': datetime_format(ctx.guild.created_at, lang=lang),
            'joined_at_date': ctx.guild.me.joined_at.strftime(strftime),
            'joined_at_formatted': datetime_format(ctx.guild.me.joined_at, lang=lang),
            'join_rank': prettify_number(rank_members.index(str(ctx.guild.me)) + 1)
        })
        embed = messages[message_to_send].get('embed')
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        if ctx.guild.banner:
            embed.set_image(url=ctx.guild.banner.url)
        elif ctx.guild.splash:
            embed.set_image(url=ctx.guild.splash.url)
        elif ctx.guild.discovery_splash:
            embed.set_image(url=ctx.guild.discovery_splash.url)
        await ctx.send(**messages[message_to_send])

    @info_gp.command(name='server_avatar', aliases=['serveravatar', 'icone', 'icon', 'sa'])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _server_avatar(self, ctx):
        if ctx.guild.icon:
            messages = await self.bot.translate(ctx)
            await ctx.send(**messages[0])
        else:
            erros = await self.bot.translate(ctx, error_='server_avatar')
            await ctx.send(**erros[0])

    @info_gp.command(name='server_banner', aliases=['serverbanner', 'banner', 'sb'])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _server_banner(self, ctx):
        if ctx.guild.banner:
            messages = await self.bot.translate(ctx)
            await ctx.send(**messages[0])
        else:
            erros = await self.bot.translate(ctx, error_='server_banner')
            await ctx.send(**erros[0])

    @info_gp.command(name='configs', aliases=['configurações', 'configuraçoes',
                                              'configuracões', 'configuracoes', 'settings'])
    @commands.guild_only()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _configs(self, ctx):
        server = await self.sr.get_servidor(self.bot.db_connection, ctx.guild.id)
        messages = await self.bot.translate(ctx, values_={
            'prefix': server.prefixo,
            'sugestao_cmd': self.bot.get_emoji('ativado' if server.sugestao_de_comando else 'desativado')
        })
        others = await self.bot.translate(ctx, others_='configs', values_={
            'ativado': self.bot.get_emoji('ativado'),
            'desativado': self.bot.get_emoji('desativado'),
            'channel_id_log': server.channel_id_log
        })
        embed = messages[0].get('embed')
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.add_field(name=others.get('field1_name'),
                        value=others.get('field1_value' if server.channel_id_log else 'field1_value2'),
                        inline=True)
        if server.channel_id_log:
            logs = []
            for msg, attr in others.get('logs_attr').items():
                if getattr(server, attr):
                    logs.append(msg)
            if len(logs) > 0:
                embed.add_field(name=others.get('field2_name'),
                                value=capitalize(', '.join(logs)) + '.',
                                inline=True)
        await ctx.send(**messages[0])

    @info_gp.command(name='joinrank', aliases=['old_members_rank', 'oldmembersrank', 'jr',
                                               'membros_antigos', 'membrosantigos'])
    @commands.guild_only()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _joinrank(self, ctx, *, member: DiscordUser = None):
        if member is None:
            member = ctx.author
        members = sorted(ctx.guild.members, key=lambda x: x.joined_at)

        def get_pos(m):
            try:
                return members.index(m) + 1
            except ValueError:
                return -1

        def to_emoji(number):
            if number == 1:
                return '🥇'
            elif number == 2:
                return '🥈'
            elif number == 3:
                return '🥉'
            emojis = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:',
                      ':seven:', ':eight:', ':nine:']
            result = ''
            for number in prettify_number(number):
                if number != '.':
                    result += emojis[int(number)]
                else:
                    result += ' '
            return result

        if len(ctx.guild.members) >= 10:
            if get_pos(member) <= 5:
                selected = members[:10]
            else:
                selected = members[get_pos(member) - 5:get_pos(member) + 5]
        else:
            selected = members.copy()
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
            if item.id in self.bot.configs.owners:
                rank += str(self.bot.get_emoji('dev_badge'))
            rank += '\n'
        messages = await self.bot.translate(ctx, values_={
            'len_members': len(ctx.guild.members),
            'rank': rank
        })
        await ctx.send(**messages[0])

    @info_gp.command(name='botinfo', aliases=['detalhes', 'bi', 'about'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _botinfo(self, ctx):
        stopwatch_banco = Stopwatch()
        sql_version = await InformacoesRepository().get_sql_version(self.bot.db_connection)
        stopwatch_banco.stop()
        # se a pessoa usou o comando, mencionando o bot:
        if ctx.prefix.replace("!", "").replace(" ", "") == self.bot.user.mention:
            # vai pegar o prefixo que está no banco
            prefixo = await get_prefix(self.bot, ctx)
        else:
            # se a pessoa não marcou o bot:
            prefixo = ctx.prefix
        lang = await self.bot.get_language(ctx)
        this_process = psutil.Process(getpid())
        all_commands = []
        for group in self.bot.get_all_groups():
            all_commands += group.commands
        messages = await self.bot.translate(ctx, values_={
            'prefix': prefixo, 'info': self.bot.get_emoji('info'),
            'created_at': self.bot.user.created_at.strftime("%d/%m/%Y"),
            'age': datetime_format(self.bot.user.created_at, lang=lang),
            'owner_emoji': self.bot.get_emoji('owner'),
            'owner': str(self.bot.get_user(self.bot.configs.owners[0])),
            'pato': self.bot.get_emoji('pato'),
            'guilds': prettify_number(len(self.bot.guilds)),
            'parrot': self.bot.get_emoji('parrot'),
            'users': prettify_number(len(set(self.bot.users))),
            'api_ping': prettify_number(int(self.bot.latency * 1000)),
            'database': self.bot.get_emoji('database'),
            'db_ping': str(stopwatch_banco),
            'loading': self.bot.get_emoji('loading'),
            'cpu_usage': prettify_number(psutil.cpu_percent()),
            'ram_usage': f'{(this_process.memory_info().rss / 1e+6):.2f}',
            'discordpy': self.bot.get_emoji('discordpy'),
            'dpy_version': discord.__version__,
            'python': self.bot.get_emoji('python'),
            'py_version': version[0:5],
            'db': sql_version[:15],
            'commands': prettify_number(len(all_commands)),
            'uptime': datetime_format(self.bot.uptime, lang=lang),
            'last_att': datetime_format(await get_last_update(self.bot.session), lang=lang)
        })
        await ctx.send(**messages[0])

    @info_gp.command(name='source', aliases=['github', 'programação', 'programaçao', 'programacão',
                                             'programacao', 's'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _source(self, ctx):
        messages = await self.bot.translate(ctx, values_={
            'python': self.bot.get_emoji('python')
        })
        await ctx.send(**messages[0])

    @info_gp.command(name='ping', aliases=['latency', 'latência', 'p'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _ping(self, ctx):
        messages = await self.bot.translate(ctx, values_={
            'loading': self.bot.get_emoji('loading'),
            'database': self.bot.get_emoji('database'),
            'api_ping': '',
            'db_ping': '',
            'dc_ping': ''
        })
        stopwatch_banco = Stopwatch()
        async with self.bot.db_connection.acquire() as conn:
            await conn.fetch('select version();')
        stopwatch_banco.stop()
        stopwatch_message = Stopwatch()
        mensagem_do_bot = await ctx.send(**messages[0])
        stopwatch_message.stop()
        messages = await self.bot.translate(ctx, values_={
            'loading': self.bot.get_emoji('loading'),
            'database': self.bot.get_emoji('database'),
            'api_ping': prettify_number(int(self.bot.latency * 1000)),
            'db_ping': str(stopwatch_banco),
            'dc_ping': str(stopwatch_message)
        })
        await asyncio.sleep(stopwatch_message.duration * 2)
        await mensagem_do_bot.edit(**messages[1])

    @info_gp.command(name='invite', aliases=['convidar', 'convite', 'i'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _invite(self, ctx):
        messages = await self.bot.translate(ctx, values_={
            'love': self.bot.get_emoji('love')
        })
        await ctx.send(**messages[0])

    @info_gp.command(name='changelog', aliases=['ultima_att', 'ultimaatt', 'última_att', 'últimaatt', 'att_log',
                                                'attlog'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _changelog(self, ctx):
        lang = await self.bot.get_language(ctx)
        messages = await self.bot.translate(ctx, values_={
            'last_commit': await get_last_commit(self.bot.session),
            'last_update': datetime_format(await get_last_update(self.bot.session), lang=lang)
        })
        await ctx.send(**messages[0])

    @info_gp.command(name='uptime', aliases=['tempo_on', 'tempoon', 'ut', 'u'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _uptime(self, ctx):
        lang = await self.bot.get_language(ctx)
        messages = await self.bot.translate(ctx, values_={
            'uptime': datetime_format(self.bot.uptime, lang=lang)
        })
        await ctx.send(**messages[0])

    @info_gp.command(name='help', aliases=['ajuda', 'h'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _help(self, ctx, *, command=None):
        embed_color = 0x6AffED
        messages = await self.bot.translate(ctx, values_={
            'prefix': (await self.bot.get_prefix(ctx.message))[-1],
            'color': embed_color,
            'commands': 0,
            'field_value': ''
        })
        others = await self.bot.translate(ctx, others_='help')
        if command is None and ctx.command.name == 'help':
            field_value = ''
            groups_display_name = others.get('groups', {})
            emojis = {}
            for group in self.bot.get_all_groups():
                display_name = groups_display_name.get(group.name)
                if display_name:
                    emoji = self.bot.get_emoji_from_group(group.name)
                    emojis[group.name] = emoji
                    field_value += f'{emoji} ── {display_name}\n'
            field_value += f'{self.bot.get_emoji("personalizado")} ── {groups_display_name.get("personalizado")}\n'
            all_commands = []
            for group in self.bot.get_all_groups():
                all_commands += group.commands
            messages = await self.bot.translate(ctx, values_={
                'prefix': (await self.bot.get_prefix(ctx.message))[-1],
                'color': embed_color,
                'commands': len(all_commands),
                'field_value': field_value
            })
            for group in self.bot.get_all_groups():
                messages.append(await embed_help_group(ctx, group, color=embed_color))

            class HelpView(ui.View):
                timeout: float

                def __init__(self, context: commands.Context):
                    super().__init__()
                    self.ctx = context
                    self.last_interaction = monotonic()
                    self.current_page = 'home'

                def select_button(self, button):
                    for child in self.children:
                        if isinstance(child, Button) and child.style == ButtonStyle.blurple:
                            child.style = ButtonStyle.grey
                    button.style = ButtonStyle.blurple

                async def back_to_home(self, interaction):
                    btn = getattr(self, '_btn_home')
                    self.select_button(btn)
                    self.current_page = 'home'
                    await interaction.response.edit_message(embed=messages[0]['embed'], view=self)

                async def interaction_check(self, interaction):
                    if not hasattr(self, '_btn_home'):
                        setattr(self,
                                '_btn_home',
                                list(filter(lambda i: isinstance(i, Button) and str(i.emoji) == '🏠', self.children))[0]
                                )
                    can_use = self.ctx.author.id == interaction.user.id
                    if not can_use:
                        ephemeral_error = (await self.ctx.bot.translate(ctx, error_='interaction', values_={
                            'atencao': self.ctx.bot.get_emoji('atencao'),
                            'display_name': interaction.user.display_name
                        }))[0]
                        await interaction.response.send_message(**ephemeral_error)
                    else:
                        self.last_interaction = monotonic()
                    return can_use

                @ui.button(style=ButtonStyle.grey, emoji=self.bot.get_emoji('administração'), row=0)
                async def adm_page(self, button, interaction):
                    if self.current_page != 'adm':
                        self.select_button(button)
                        await interaction.response.edit_message(embed=messages[1], view=self)
                        self.current_page = 'adm'
                    else:
                        await self.back_to_home(interaction)

                @ui.button(style=ButtonStyle.grey, emoji=self.bot.get_emoji('diversão'), row=0)
                async def fun_page(self, button, interaction):
                    if self.current_page != 'fun':
                        self.select_button(button)
                        await interaction.response.edit_message(embed=messages[2], view=self)
                        self.current_page = 'fun'
                    else:
                        await self.back_to_home(interaction)

                @ui.button(style=ButtonStyle.grey, emoji=self.bot.get_emoji('info'), row=0)
                async def info_page(self, button, interaction):
                    if self.current_page != 'info':
                        self.select_button(button)
                        await interaction.response.edit_message(embed=messages[3], view=self)
                        self.current_page = 'info'
                    else:
                        await self.back_to_home(interaction)

                @ui.button(style=ButtonStyle.grey, emoji=self.bot.get_emoji('matemática'), row=1)
                async def math_page(self, button, interaction):
                    if self.current_page != 'math':
                        self.select_button(button)
                        await interaction.response.edit_message(embed=messages[4], view=self)
                        self.current_page = 'math'
                    else:
                        await self.back_to_home(interaction)

                @ui.button(style=ButtonStyle.blurple, emoji='🏠', row=1)
                async def home_page(self, button, interaction):
                    if self.current_page != 'home':
                        self.select_button(button)
                        await interaction.response.edit_message(embed=messages[0]['embed'], view=self)
                        self.current_page = 'home'

                @ui.button(style=ButtonStyle.grey, emoji=self.bot.get_emoji('owner'), row=1, disabled=True)
                async def owner_page(self, button, interaction):
                    if self.current_page != 'owner':
                        self.select_button(button)
                        await interaction.response.edit_message(embed=messages[5], view=self)
                        self.current_page = 'owner'
                    else:
                        await self.back_to_home(interaction)

                @ui.button(style=ButtonStyle.grey, emoji=self.bot.get_emoji('úteis'), row=2)
                async def utils_page(self, button, interaction):
                    if self.current_page != 'utils':
                        self.select_button(button)
                        await interaction.response.edit_message(embed=messages[6], view=self)
                        self.current_page = 'utils'
                    else:
                        await self.back_to_home(interaction)

                @ui.button(style=ButtonStyle.grey, emoji=self.bot.get_emoji('personalizado'), row=2, disabled=True)
                async def pers_page(self, button, interaction):
                    if self.current_page != 'pers':
                        self.select_button(button)
                        await interaction.response.edit_message(embed=messages[7], view=self)
                        self.current_page = 'pers'
                    else:
                        await self.back_to_home(interaction)

                @ui.button(style=ButtonStyle.red, emoji=self.bot.get_emoji('stop'), row=2)
                async def exit_btn(self, button, interaction):
                    self.stop()

            view = HelpView(ctx)
            for item in view.children:
                if isinstance(item, Button):
                    if item.emoji == self.bot.get_emoji('owner'):
                        try:
                            if is_owner(ctx):
                                item.disabled = False
                        except commands.errors.NotOwner:
                            pass
                    elif item.emoji == self.bot.get_emoji('personalizado'):
                        if ctx.guild:
                            servidor = await self.sr.get_servidor(self.bot.db_connection, ctx.guild.id)
                            cmds_personalizados = await self.cpr.get_commands(self.bot.db_connection, servidor)
                            if len(cmds_personalizados) >= 1:
                                item.disabled = False
                                messages.append(await embed_help_group(ctx, 'personalizado',
                                                                       list(map(lambda c: c.comando,
                                                                                cmds_personalizados)),
                                                                       color=embed_color))
            messages[0]['view'] = view
            msg = await ctx.send(**messages[0])
            timeout = 60.0
            while True:
                if view.last_interaction + timeout <= monotonic():
                    view.stop()
                if view.is_finished():
                    return await msg.edit(view=None)
                await sleep(0.01)
        else:
            if command is None:
                command = ctx.command
            else:
                command = self.bot.get_command(command)
            if command is None:
                all_names = list(map(lambda c: c.name, self.bot.commands))
                for group in self.bot.get_all_groups():
                    all_names.append(group.name)
                    for cmd in group.commands:
                        all_names.append(cmd.name)
                        for alias in cmd.aliases:
                            all_names.append(alias)
                command_name = ctx.message.content.lower()[len(ctx.prefix):].split(' ')
                command_name = command_name[-1]
                if ctx.guild:
                    servidor = await self.sr.get_servidor(self.bot.db_connection, ctx.guild.id)
                    all_names += list(
                        map(lambda c: c.comando, await self.cpr.get_commands(self.bot.db_connection, servidor)))
                suggestion = get_most_similar_item(command_name, all_names)
                use_suggestion = False
                # se a sugestão for pelo menos 50% semelhante ao comando
                if (suggestion is not None) and (string_similarity(command_name, suggestion) >= 0.5):
                    use_suggestion = True
                erros = await self.bot.translate(ctx, error_='help', values_={
                    'suggestion': suggestion,
                    'command_name': command_name,
                    'sad': self.bot.get_emoji('sad')
                })
                return await ctx.send(**erros[0 if use_suggestion else 1])
            embed = await embed_help_command(ctx, command)
            await ctx.send(embed=embed)


def setup(bot):
    cog = Info(bot)
    cmds = f'{Fore.BLUE}{len(list(cog.walk_commands()))}{Fore.LIGHTMAGENTA_EX}'
    print(f'{Style.BRIGHT}{Fore.GREEN}[{"COG LOADED":^16}]' +
          f'{Fore.LIGHTMAGENTA_EX}{cog.qualified_name}({cmds}){Style.RESET_ALL}'.rjust(60))
    bot.add_cog(cog)
