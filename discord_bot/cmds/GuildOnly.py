# coding=utf-8
# Androxus bot
# GuildOnly.py
# font: https://github.com/AlexFlipnote/discord_bot.py

__author__ = 'Rafael'

from discord.ext import commands
import discord
from discord_bot.modelos.EmbedHelp import embedHelp
from datetime import datetime
from discord_bot.utils.Utils import random_color, capitalize, datetime_format
from googletrans import Translator
import asyncio


class GuildOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def help_avatar(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.avatar.name,
                          descricao=self.avatar.description,
                          parametros=['<"Mencionar uma pessoa ou um id">'],
                          exemplos=['``{pref}avatar``' + f' {ctx.author.mention}'])
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(description='Eu vou mandar a foto de perfil da pessoa que você marcar.')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def avatar(self, ctx, *args):
        if ctx.message.mentions:  # se tiver alguma menção na mensagem
            await ctx.send(
                f'{ctx.message.mentions[0].avatar_url}')  # vai pegar a primeira menção, e pega o avatar da pessoa
        else:  # se a pessoa não mencionou ninguém, entra aqui
            if args:  # se a pessoa passou pelo menos alguma coisa
                if len(args) == 1:  # se a pessoa passou mais de um item
                    try:  # vai tentar converter o argumento para int
                        id_de_quem_ver_o_avatar = int(args[0])  # conversão
                        user = self.bot.get_user(
                            id_de_quem_ver_o_avatar)  # se chegou aqui, vai tentar pegar o usuário com esse id
                        if user is not None:  # se achou uma pessoa
                            await ctx.send(f'{user.avatar_url}')  # vai mandar o avatar desta pessoa
                        else:  # se o user for None, é porque o bot não achou esse usuário
                            await ctx.send('<a:sad:755774681008832623> Não consegui encontrar o usuário' +
                                           f' <@{id_de_quem_ver_o_avatar}>\nEu preciso ter pelo menos 1' +
                                           ' servidor em comum com a pessoa, para conseguir encontrar ela.')
                    except ValueError:  # se der erro, é porque a pessoa não passou apenas números
                        await ctx.send(f'<a:atencao:755844029333110815> O valor ``{args[0]}`` não é um id valido!')
                else:  # se a pessoa passou mais de 1 argumento
                    await ctx.send('<a:atencao:755844029333110815> Você me disse muitas coisas,' +
                                   ' eu só preciso, ou do id da pessoa, ou que você mencione ela.')
            else:  # se a pessoa não passou nenhum argumento:
                await ctx.send(f'{ctx.author.avatar_url}')

    @commands.command(hidden=True)
    async def help_userinfo(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.userinfo.name,
                          descricao=self.userinfo.description,
                          exemplos=['``{pref}userinfo``'])
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(description='Eu vou mandar o máximo de informações sobre um usuário.')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def userinfo(self, ctx, *args):
        async with ctx.channel.typing():  # vai aparecer "bot está digitando"
            user = None
            if ctx.message.mentions:  # se tiver alguma menção na mensagem
                user = ctx.message.mentions[0]  # vai pegar a primeira menção
            else:  # se a pessoa não mencionou ninguém, entra aqui
                if args:  # se a pessoa passou pelo menos alguma coisa
                    if len(args) == 1:  # se a pessoa passou mais de um item
                        try:  # vai tentar converter o argumento para int
                            id_user = int(args[0])  # conversão
                            if ctx.guild:
                                user = ctx.guild.get_member(id_user)  # vai tentar pegar o user no server
                            if user is None:  # se não achou na guild, vai ver se o bot acha
                                user = self.bot.get_user(id_user)
                            if user is None:  # se a pessoa não está na guild e o bot tbm não achou:
                                return await ctx.send('<a:sad:755774681008832623> Não consegui encontrar o usuário!' +
                                                      f'\nEu preciso ter pelo menos 1' +
                                                      ' servidor em comum com a pessoa, para conseguir encontrar ela.')
                        except ValueError:  # se der erro, é porque a pessoa não passou apenas números
                            await ctx.send(f'<a:atencao:755844029333110815> O valor ``{args[0]}`` não é um id valido!')
                            return
                    else:  # se a pessoa passou mais de 1 argumento
                        await ctx.send('<a:atencao:755844029333110815> Você me disse muitas coisas,' +
                                       ' eu só preciso, ou do id da pessoa, ou que você mencione ela.')
                        return
                else:  # se a pessoa não passou nenhum argumento:
                    user = ctx.author
            roles = None
            if hasattr(user, 'roles'):
                roles = ', '.join(
                    [f"<@&{x.id}>" for x in sorted(user.roles, key=lambda x: x.position, reverse=True) if
                     x.id != ctx.guild.default_role.id]
                ) if len(user.roles) > 1 else None
            if hasattr(user, 'top_role'):
                cor = user.top_role.colour.value
            else:
                cor = discord.Colour(random_color())
            info2 = None
            info1 = discord.Embed(title=f'Informações sobre o(a) {user.name}!',
                                  colour=cor,
                                  description='O máximo de informação que eu consegui encontrar.',
                                  timestamp=datetime.utcnow())
            info1.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            info1.set_thumbnail(url=user.avatar_url)
            info1.add_field(name="Nome e tag:", value=f'``{user}``', inline=True)
            info1.add_field(name="Id: ", value=f'``{user.id}``', inline=True)
            if hasattr(user, 'nick'):
                if user.nick is not None:
                    info1.add_field(name="Nickname", value=f'``{user.nick}``', inline=True)
            info1.add_field(name="Conta criada em:",
                            value=f'``{user.created_at.strftime("%d/%m/%Y")}({datetime_format(user.created_at)})``',
                            inline=True)
            if hasattr(user, 'joined_at'):
                info1.add_field(name="Entrou no servidor há:",
                                value=f'``{user.joined_at.strftime("%d/%m/%Y")}({datetime_format(user.joined_at)})``',
                                inline=True)
                # só vai mostrar as permissões da pessoa, se ela estiver no server
                info2 = discord.Embed(title=f'Outras informações sobre o(a) {user.name}!',
                                      colour=cor,
                                      description='** **',
                                      timestamp=datetime.utcnow())
                info2.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                info2.set_thumbnail(url=user.avatar_url)
                if roles is not None:
                    info2.add_field(name=f'Cargos({len(roles.split(", "))}):', value=roles, inline=False)
                all_perms = user.permissions_in(ctx.message.channel)
                perms = []
                for atributo in dir(all_perms):
                    if isinstance(getattr(all_perms, atributo), bool):
                        if getattr(all_perms, atributo):
                            perms.append(atributo)
                translator = Translator()
                for c in range(0, len(perms)):
                    # além de substituir os "_" por espaços, vai traduzir a permissão
                    perm_filtrada = perms[c].replace('_', ' ')
                    perm_filtrada = perm_filtrada.replace('ban members', 'banir membros')
                    perm_filtrada = perm_filtrada.replace('kick members', 'expulsar membros')
                    perm_filtrada = perm_filtrada.replace('embed links', 'enviar links')
                    perms[c] = f"``{translator.translate(perm_filtrada, dest='pt').text}``"
                info2.add_field(name=f'Permissões({len(perms)}):', value=capitalize(', '.join(perms)), inline=False)

        async def menus_user_info(msg):
            while True:
                def check_page1(reaction, user):  # fica verificando a pagina 1, para ver se é para ir para a pagina 2
                    return (user.id == ctx.author.id) and (str(reaction.emoji) == '➡')

                def check_page2(reaction, user):  # fica verificando a pagina 2, para ver se é para ir para a pagina 1
                    return (user.id == ctx.author.id) and (str(reaction.emoji) == '⬅')

                await self.bot.wait_for('reaction_add', timeout=30.0, check=check_page1)
                await msg.clear_reactions()
                await msg_bot.add_reaction('⬅')
                await msg.edit(embed=info2)
                await self.bot.wait_for('reaction_add', timeout=30.0, check=check_page2)
                await msg.clear_reactions()
                await msg_bot.add_reaction('➡')
                await msg.edit(embed=info1)
        msg_bot = await ctx.send(embed=info1)
        if info2:
            await msg_bot.add_reaction('➡')
            try:
                # vai fica 30 segundos esperando o usuário apertas nos emojis
                await asyncio.wait_for(menus_user_info(msg_bot), timeout=30.0)
            except asyncio.TimeoutError:  # se acabar o tempo
                pass

    @commands.command(hidden=True)
    async def help_serverinfo(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.serverinfo.name,
                          descricao=self.serverinfo.description,
                          exemplos=['``{pref}serverinfo``'])
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(description='Eu vou mandar o máximo de informações sobre um servidor.')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        if ctx.invoked_subcommand is None:
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
                embed.set_image(url=ctx.guild.banner_url_as(format="png"))

            embed.add_field(name='Nome do servidor', value=f'``{ctx.guild.name}``', inline=True)
            if ctx.guild.description:
                embed.add_field(name='Descrição do servidor', value=f'``{ctx.guild.description}``', inline=True)
            embed.add_field(name='Id do servidor', value=f'``{ctx.guild.id}``', inline=True)
            embed.add_field(name='Dono', value=f'``{ctx.guild.owner}\n({ctx.guild.owner_id})``', inline=True)
            embed.add_field(name='Membros', value=f'``{ctx.guild.member_count}``', inline=True)
            embed.add_field(name='Bots', value=f'``{bots}``', inline=True)
            embed.add_field(name='Emojis', value=f'``{len(ctx.guild.emojis)}``', inline=True)
            embed.add_field(name='Chats', value=f'``{len(ctx.guild.text_channels)}``', inline=True)
            embed.add_field(name='Calls', value=f'``{len(ctx.guild.voice_channels)}``', inline=True)
            embed.add_field(name='Cargos', value=f'``{len(ctx.guild.roles)}``', inline=True)
            embed.add_field(name='Região', value=f'``{str(ctx.guild.region).capitalize()}``', inline=True)
            embed.add_field(name='Criado em:', value=f'``{ctx.guild.created_at.strftime("%d/%m/%Y")}' +
                                                     f'({datetime_format(ctx.guild.created_at)})``', inline=True)
            await ctx.send(embed=embed)

    @commands.command(hidden=True, aliases=["help_icone"])
    async def help_server_avatar(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.server_avatar.name,
                          descricao=self.server_avatar.description,
                          exemplos=['``{pref}server_avatar``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.server_avatar.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=["icone"], description='Eu vou enviar o icone do servidor (se tiver).')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def server_avatar(self, ctx):
        if not ctx.guild.icon:
            await ctx.send("Este servidor não tem avatar.")
            return
        await ctx.send(f"{ctx.guild.icon_url_as(size=1024)}")

    @commands.command(hidden=True, aliases=["help_banner"])
    async def help_server_banner(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.server_banner.name,
                          descricao=self.server_banner.description,
                          exemplos=['``{pref}server_banner``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.server_banner.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=["banner"], description='Eu vou enviar o banner do servidor (se tiver).')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def server_banner(self, ctx):
        if not ctx.guild.banner:
            await ctx.send("Este servidor não tem banner.")
            return
        await ctx.send(f"{ctx.guild.banner_url_as(format='png')}")


def setup(bot):
    bot.add_cog(GuildOnly(bot))
