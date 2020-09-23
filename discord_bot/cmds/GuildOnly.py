# coding=utf-8
# Androxus bot
# GuildOnly.py
# font: https://github.com/AlexFlipnote/discord_bot.py

__author__ = 'Rafael'

from discord.ext import commands
import discord
from discord_bot.modelos.EmbedHelp import embedHelp
from datetime import datetime
from discord_bot.utils.Utils import random_color


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
                            user = self.bot.get_user(id_user)  # se chegou aqui, vai tentar pegar o usuário com esse id
                            if user is None:  # se achou uma pessoa
                                await ctx.send('<a:sad:755774681008832623> Não consegui encontrar o usuário!' +
                                               f'\nEu preciso ter pelo menos 1' +
                                               ' servidor em comum com a pessoa, para conseguir encontrar ela.')
                                return
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
                    [f"<@&{x.id}>" for x in sorted(user.roles, key=lambda x: x.position, reverse=True) if x.id != ctx.guild.default_role.id]
                ) if len(user.roles) > 1 else None
            if hasattr(user, 'top_role'):
                cor = user.top_role.colour.value
            else:
                cor = discord.Colour(random_color())
            embed = discord.Embed(title=f'Informações sobre o(a) {user}!',
                                  colour=cor,
                                  description='O máximo de informação que eu consegui encontrar.',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="Nome e tag", value=user, inline=True)
            embed.add_field(name="Id: ", value=user.id, inline=True)
            if hasattr(user, 'nick'):
                if user.nick is not None:
                    embed.add_field(name="Nickname", value=user.nick, inline=True)
            embed.add_field(name="Conta criada em:", value=user.created_at.strftime("%d/%m/%Y às %H:%M:%S"), inline=True)
            if hasattr(user, 'joined_at'):
                embed.add_field(name="Entrou no servidor em:", value=user.joined_at.strftime("%d/%m/%Y às %H:%M:%S"), inline=True)
                embed.add_field(name="Cargos", value=roles, inline=False)
        return await ctx.send(embed=embed)

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
            bots = sum(1 for member in ctx.guild.members if member.bot)

            embed = discord.Embed(title=f'Informações sobre este servidor!',
                                  colour=discord.Colour(random_color()),
                                  description='O máximo de informação que eu consegui encontrar.',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')

            if ctx.guild.icon:
                embed.set_thumbnail(url=ctx.guild.icon_url)
            if ctx.guild.banner:
                embed.set_image(url=ctx.guild.banner_url_as(format="png"))

            embed.add_field(name="Nome do servidor", value=ctx.guild.name, inline=True)
            embed.add_field(name="Id do servidor", value=ctx.guild.id, inline=True)
            embed.add_field(name="Membros", value=ctx.guild.member_count, inline=True)
            embed.add_field(name="Bots", value=bots, inline=True)
            embed.add_field(name="Dono", value=ctx.guild.owner, inline=True)
            embed.add_field(name="Região", value=str(ctx.guild.region).capitalize(), inline=True)
            embed.add_field(name="Criado em:", value=ctx.guild.created_at.strftime("%d/%m/%Y às %H:%M:%S"), inline=True)
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
