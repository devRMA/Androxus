# -*- coding: utf-8 -*-
# Androxus bot
# converters.py

__author__ = 'Rafael'

import discord
from discord.ext import commands

from Classes.erros import MultipleResults
from utils.Utils import find_user


class DiscordUser(commands.Converter):
    """
    Vai tentar procurar por nome, id, nome#tag, nick, menção
    por similaridade entre os users e o input,
    por users que começam com o input, users
    que terminam com o input e por fetch na API
    """

    async def convert(self, ctx, argument=None):
        if argument is not None:
            if ctx.prefix.replace('!', '').replace(' ', '') == ctx.bot.user.mention:
                if ctx.message.content.replace('!', '').count(ctx.bot.user.mention) == 1:
                    ctx.message.mentions.pop(0)
            if ctx.message.mentions:
                return ctx.message.mentions[-1]
            if isinstance(ctx.message.channel, discord.DMChannel):
                if str(argument).isdigit():
                    try:
                        return await ctx.bot.fetch_user(int(argument))
                    except:
                        return None
                else:
                    return None
            users = await find_user(argument, ctx=ctx)
            if len(users) == 1:
                return users[0]
            if len(users) == 0:
                return None
            if len(users) > 1:
                raise MultipleResults(users)
        return None


# font: https://github.com/Rapptz/RoboDanny
class BannedMember(commands.Converter):
    async def convert(self, ctx, argument):
        if argument:
            # se a pessoa usou o comando mencionando o bot
            if ctx.prefix.replace('!', '').replace(' ', '') == ctx.me.mention:
                # se a pessoa marcou o bot apenas 1 vez
                if ctx.message.content.replace('!', '').count(ctx.me.mention) == 1:
                    # vai tirar a menção da mensagem
                    ctx.message.mentions.pop(0)
            if ctx.message.mentions:
                try:
                    return await ctx.guild.fetch_ban(discord.Object(id=ctx.message.mentions[-1].id))
                except discord.NotFound:
                    erro = commands.BadArgument('Membro mencionado não está banido!')
                    erro.user = ctx.message.mentions[-1]
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
            entity = discord.utils.find(lambda u: any([str(u.user) == argument,
                                                       u.user.name == argument,
                                                       u.user.discriminator == argument]), ban_list)

            if entity is None:
                erro = commands.BadArgument('Esse membro não está banido!')
                erro.member = argument
                raise erro
            return entity
        else:
            return None
