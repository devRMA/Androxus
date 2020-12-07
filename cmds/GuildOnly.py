# -*- coding: utf-8 -*-
# Androxus bot
# GuildOnly.py
# source: https://github.com/AlexFlipnote/discord_bot.py/blob/master/cogs/discord.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from DiscordUtils.Pagination import CustomEmbedPaginator
from discord.ext import commands

from Classes import Androxus
from database.Repositories.ServidorRepository import ServidorRepository
from utils.Utils import random_color, capitalize, datetime_format, get_most_similar_items_with_similarity, \
    prettify_number
from utils.converters import DiscordUser


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
                      examples=['`{prefix}avatar` {author_mention}'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _avatar(self, ctx, *, user: DiscordUser = None):
        if user is None:
            user = ctx.author
        e = discord.Embed(title=f'Avatar do(a) {str(user)}!',
                          colour=discord.Colour(random_color()),
                          description=f'Clique [aqui]({user.avatar_url}) para baixar o avatar.',
                          timestamp=datetime.utcnow())
        e.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        e.set_image(url=str(user.avatar_url))
        return await ctx.send(embed=e)

    @Androxus.comando(name='userinfo',
                      aliases=['profile', 'memberinfo', 'ui'],
                      description='Eu vou mandar o máximo de informações sobre um usuário.',
                      parameters=['[usuário (padrão: quem usou o comando)]'],
                      examples=['`{prefix}userinfo` {author_mention}'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _userinfo(self, ctx, *, user: DiscordUser = None):
        if user is None:
            user = ctx.author
        if hasattr(user, 'top_role'):
            cor = user.top_role.colour.value
        else:
            cor = discord.Colour(random_color())
        emojis_badges = {
            'staff': self.bot.get_emoji('staff_badge'),
            'partner': self.bot.get_emoji('parceiro_badge'),
            'hypesquad': self.bot.get_emoji('hs_badge'),
            'bug_hunter': self.bot.get_emoji('bug_hunter_badge'),
            'hypesquad_bravery': self.bot.get_emoji('hs_bravery_badge'),
            'hypesquad_brilliance': self.bot.get_emoji('hs_brilliance_badge'),
            'hypesquad_balance': self.bot.get_emoji('hs_balance_badge'),
            'early_supporter': self.bot.get_emoji('early_supporter_badge'),
            'team_user': '',
            'system': '',
            'bug_hunter_level_2': self.bot.get_emoji('bug_hunter_badge'),
            'verified_bot': '',
            'verified_bot_developer': self.bot.get_emoji('dev_badge')
        }
        badges = ''
        if ctx.guild:
            if ctx.guild.owner_id == user.id:
                badges += '👑'
        if user.bot:
            badges += str(self.bot.get_emoji('bot_badge'))
        if hasattr(user, 'public_flags'):
            for flag, have in iter(user.public_flags):
                if have:
                    badges += str(emojis_badges[flag])
        if user.is_avatar_animated() or (hasattr(user, 'premium_since') and user.premium_since is not None):
            badges += str(self.bot.get_emoji('nitro'))
        if hasattr(user, 'premium_since') and user.premium_since is not None:
            badges += str(self.bot.get_emoji('boost'))
        status_emoji = ''
        status_text = None
        if hasattr(user, 'raw_status'):
            if user.raw_status == 'online':
                status_emoji = str(self.bot.get_emoji('online'))
                status_text = 'online'
            elif user.raw_status == 'dnd':
                status_emoji = str(self.bot.get_emoji('dnd'))
                status_text = 'ocupado'
            elif user.raw_status == 'idle':
                status_emoji = str(self.bot.get_emoji('idle'))
                status_text = 'ausente'
            elif (user.raw_status == 'offline') or (user.raw_status == 'invisible'):
                status_emoji = str(self.bot.get_emoji('offline'))
                status_text = 'offline'
        embed_base = discord.Embed(title=f'{badges} {user.display_name} {status_emoji}',
                                   colour=cor,
                                   timestamp=datetime.utcnow())
        embeds = []
        embed1 = embed_base.copy()
        embed1.set_image(url=user.avatar_url)
        embed1.add_field(name="📑 Nome e tag:", value=f'`{user}`', inline=True)
        embed1.add_field(name="🆔 Id: ", value=f'`{user.id}`', inline=True)
        embed1.add_field(name='🙋‍♂️ Menção:', value=user.mention, inline=True)
        if hasattr(user, 'nick') and (user.nick is not None):
            embed1.add_field(name="🔄 Apelido", value=f'`{user.nick}`', inline=True)
        embeds.append(embed1)
        embed2 = embed_base.copy()
        embed2.set_thumbnail(url=user.avatar_url)
        embed2.add_field(name="🗓 Conta criada em:",
                         value=f'`{user.created_at.strftime("%d/%m/%Y")}`({datetime_format(user.created_at)})',
                         inline=True)
        if hasattr(user, 'joined_at'):
            rank_members = [str(c) for c in sorted(user.guild.members, key=lambda x: x.joined_at)]
            embed2.add_field(name="📥 Entrou no servidor em:",
                             value=f'`{user.joined_at.strftime("%d/%m/%Y")}`({datetime_format(user.joined_at)})',
                             inline=True)
            embed2.add_field(name='🏆 rank dos membros mais antigos:',
                             value=f'**{prettify_number(rank_members.index(str(user)) + 1)}°**/'
                                   f'{prettify_number(len(rank_members))}',
                             inline=True)
            if user.premium_since is not None:
                embed2.add_field(
                    name=f'{self.bot.get_emoji("boost")} Começou a dar boost neste servidor em:',
                    value=f'`{user.premium_since.strftime("%d/%m/%Y")}`('
                          f'{datetime_format(user.premium_since)})',
                    inline=True)
        embeds.append(embed2)
        if hasattr(user, 'raw_status') and (user.raw_status != 'offline') and \
                (user.raw_status != 'invisible') and (not user.bot):
            embed3 = embed_base.copy()
            embed3.set_thumbnail(url=user.avatar_url)
            if user.is_on_mobile():
                plataforma = '📱 Celular'
            else:
                if user.web_status.value != 'offline':
                    plataforma = '💻 Pc ─ usando o site 🌐'
                else:
                    plataforma = '💻 Pc ─ usando o discord desktop 🖥'
            embed3.add_field(name=f'{self.bot.get_emoji("hacking")} Está acessando o discord pelo:',
                             value=f'`{plataforma}`',
                             inline=False)
            if status_text is not None:
                embed3.add_field(name=f'🕵️ Status: {status_text}',
                                 value='** **',
                                 inline=True)
            if hasattr(user, 'activities') and len(user.activities) > 0:
                streaming = False
                custom = False
                playing = False
                for activity in user.activities:
                    if (activity.type.name == 'streaming') and (not streaming):
                        embed3.add_field(name=f'{self.bot.emoji("streaming")} Fazendo live',
                                         value=f'**🎙 Plataforma**: `{activity.platform}`\n'
                                               f'**🏷 Nome da live**: `{activity.name}`\n'
                                               f'**🕛 Começou**: `{datetime_format(activity.created_at)}`',
                                         inline=False)
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
                            embed3.add_field(name=f'{self.bot.emoji("disco")} Status personalizado',
                                             value=f'🔰 Emoji: {emoji}\n'
                                                   f'🖋 Frase: {texto}',
                                             inline=False)
                            custom = True
                    elif (activity.type.name == 'playing') and (not playing):
                        if activity.start is not None:
                            value = f'`{activity.name}`\n**🕛 Começou a jogar:**\n' + \
                                    f'`{datetime_format(activity.start)}`'
                        else:
                            value = f'`{activity.name}`'
                        embed3.add_field(name='🕹 Jogando',
                                         value=value,
                                         inline=False)
                        playing = True
            embeds.append(embed3)
        if hasattr(user, 'roles') and len(user.roles) > 1:
            roles = [role for role in sorted(user.roles, key=lambda r: r.position, reverse=True)
                     if role.id != ctx.guild.default_role.id]
            roles_count = len(roles)
            if roles_count > 0:
                roles_mention = ', '.join(f'<@&{r.id}>' for r in roles)
                roles_name = None
                if len(roles_mention) > 1000:
                    roles_name = ', '.join(f'`{r.name}`' for r in roles)
                if roles_name is not None and len(roles_name) > 1000:
                    roles_name = f'{roles_name[:1000]}...'
                roles = roles_name or roles_mention
                roles = f'**{roles}**'
                embed4 = embed_base.copy()
                embed4.set_thumbnail(url=user.avatar_url)
                embed4.add_field(name=f'🏅 Cargos({roles_count}):',
                                 value=roles,
                                 inline=False)
                # estamos pegando e filtrando as permissões que o user tem, neste chat
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
                            perms[c] = f"`{perm_traducao[-1]}`"
                            break
                if 'external_emojis' in perms:
                    perms.pop(perms.index('external_emojis'))
                if len(perms) >= 1:
                    embed4.add_field(name=f'📌 Permissões neste chat({len(perms)}):',
                                     value=capitalize(', '.join(perms)),
                                     inline=False)
                else:
                    embed4.add_field(name=f'📌 Permissão neste chat(0):',
                                     value='Este usuário não tem possui permissões, neste chat!',
                                     inline=False)
                embeds.append(embed4)
        for pos, embed in enumerate(embeds):
            embed.set_footer(text=f'{ctx.author} ─ {pos + 1}/{len(embeds)}',
                             icon_url=ctx.author.avatar_url)
        paginator = CustomEmbedPaginator(ctx=ctx,
                                         timeout=60,
                                         auto_footer=False,
                                         remove_reactions=ctx.channel.permissions_for(
                                             ctx.me).manage_messages)
        if len(embeds) > 2:
            paginator.add_reaction('⏮', 'first')
        paginator.add_reaction('◀️', 'back')
        paginator.add_reaction('⏹️', 'clear')
        paginator.add_reaction('▶', 'next')
        if len(embeds) > 2:
            paginator.add_reaction('⏭', 'last')
        msg = await paginator.run(embeds)
        for reaction in msg.reactions:
            if reaction.me:
                await reaction.remove(ctx.me)

    @Androxus.comando(name='splash',
                      aliases=['fundo_convite'],
                      description='Eu vou enviar a imagem de fundo do convite deste servidor (se tiver).',
                      examples=['`{prefix}splash`'])
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
                      examples=['`{prefix}discovery_splash`'])
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
                      examples=['`{prefix}serverinfo`'])
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
                      examples=['`{prefix}server_avatar`'])
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
                      examples=['`{prefix}server_banner`'])
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
                      examples=['`{prefix}configs`'])
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
                logs.append('`mensagem deletada`')
            if servidor.mensagem_editada:
                logs.append('`mensagem editada`')
            if servidor.avatar_alterado:
                logs.append('`avatar alterado`')
            if servidor.nome_alterado:
                logs.append('`nome alterado`')
            if servidor.tag_alterado:
                logs.append('`tag alterada`')
            if servidor.nick_alterado:
                logs.append('`nick alterado`')
            if servidor.role_alterado:
                logs.append('`cargo adicionado/removido`')
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
                      examples=['`{prefix}joinrank`',
                                '`{prefix}jr` `-r`',
                                '`{prefix}jr` `androxus`'],
                      hidden=True)
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
