# coding=utf-8
# Androxus bot
# Admin.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.ext import commands

from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.utils import permissions
from discord_bot.utils.Utils import get_configs, get_emoji_dance
from discord_bot.utils.Utils import random_color


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


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_banir'])
    async def help_ban(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.ban.name,
                          descricao=self.ban.description,
                          parametros=['<membro do servidor>', '[motivo]'],
                          exemplos=['``{pref}ban`` ``@membro#1234`` ``ofendeu membro``',
                                    '``{pref}banir`` ``123456789``'],
                          perm_pessoa='banir membros',
                          perm_bot='banir membros',
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.ban.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['banir'], description='Banir algum membro.')
    @permissions.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member = None, *args):
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
                        return await self.help_ban(ctx)
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
                return await self.help_ban(ctx)
            embed = discord.Embed(title=f'<a:banned:756138595882107002> Usuário banido!',
                                  colour=discord.Colour(random_color()),
                                  description=f'Usuário: {member}\nId: {member.id}\nMotivo: ' +
                                              f'{str(reason).replace("None", "Nenhum")}',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=str(ctx.author),
                             icon_url=ctx.author.avatar_url)
            msg_ban = f'Você foi banido do servidor {ctx.guild}!'
            if reason:
                msg_ban += f'\nPelo motivo: {reason}'
        try:
            msg = await member.send(msg_ban)
        except:
            pass
        reason = f'Banido por: {ctx.author} —— Motivo: {str(reason).replace("None", "")}'
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

    @commands.command(hidden=True, aliases=['help_expulsar'])
    async def help_kick(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.kick.name,
                          descricao=self.kick.description,
                          parametros=['<membro do servidor>', '[motivo]'],
                          exemplos=['``{pref}kick`` ``@membro#1234`` ``não quero você aqui!``',
                                    '``{pref}expulsar`` ``123456789``'],
                          perm_pessoa='expulsar membros',
                          perm_bot='expulsar membros',
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.ban.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['expulsar'], description='Expulsa algum membro!')
    @permissions.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member = None, *args):
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
                        return await self.help_kick(ctx)
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
                return await self.help_kick(ctx)
            embed = discord.Embed(title=f'Usuário expulso!',
                                  colour=discord.Colour(random_color()),
                                  description=f'Usuário: {member}\nId: {member.id}\nMotivo: ' +
                                              f'{str(reason).replace("None", "Nenhum")}',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=str(ctx.author),
                             icon_url=ctx.author.avatar_url)
            msg_kick = f'Você foi expulso do servidor {ctx.guild}!'
            if reason:
                msg_kick += f'\nPelo motivo: {reason}'
        msg = await member.send(msg_kick)
        reason = f'Expulso por: {ctx.author} —— Motivo: {str(reason).replace("None", "")}'
        try:
            await ctx.guild.kick(member, reason=reason)
        except discord.errors.Forbidden:
            await msg.delete()
            await ctx.send('Eu não tenho permissão para expulsar esse usuário. <a:sad:755774681008832623>')
        else:
            await ctx.send(content=get_emoji_dance(), embed=embed)

    @commands.command(hidden=True, aliases=['help_desbanir', 'help_revogar_ban'])
    async def help_unban(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.unban.name,
                          descricao=self.unban.description,
                          parametros=['<membro>', '[motivo]'],
                          exemplos=['``{pref}unban`` ``"membro#1234"`` ``pode voltar``\n**(Observer que para usar ' +
                                    'o comando unban, passando o nome e a tag da pessoa, é necessário usar "")**',
                                    '``{pref}revogar_ban`` ``123456789``'],
                          perm_pessoa='banir membros',
                          perm_bot='banir membros',
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.unban.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['desbanir', 'revogar_ban'], description='Revoga o banimento de algum membro!')
    @permissions.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, member: BannedMember = None, *args):
        async with ctx.typing():  # vai aparecer "bot está digitando"
            if member is None:
                return await self.help_unban(ctx)
            reason = None
            if args:
                reason = ' '.join(args)
            embed = discord.Embed(title=f'Ban revogado!',
                                  colour=discord.Colour(random_color()),
                                  description=f'Usuário: {member.user}\nId: {member.user.id}\nMotivo: ' +
                                              f'{str(reason).replace("None", "Nenhum")}',
                                  timestamp=datetime.utcnow())
            if member.reason:
                embed.add_field(name='Antigo ban:',
                                value=f'{member.reason}',
                                inline=False)
            embed.set_footer(text=str(ctx.author),
                             icon_url=ctx.author.avatar_url)
            reason = f'Ban revogado por: {ctx.author} —— Motivo: {str(reason).replace("None", "")}'
        try:
            await ctx.guild.unban(member.user, reason=reason)
        except discord.Forbidden:
            await ctx.send('Não tenho permissão para revogar banimentos!')
        except discord.HTTPException:
            await ctx.send('Desculpe, mas ocorreu um erro na hora de executar o comando, tente novamente mais tarde.')
        else:
            await ctx.send(content=get_emoji_dance(), embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
