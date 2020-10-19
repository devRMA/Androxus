# coding=utf-8
# Androxus bot
# permissions.py

# source: https://github.com/AlexFlipnote/discord_bot.py/blob/master/utils/permissions.py

import discord
from discord.ext import commands

from utils.Utils import get_configs


def is_owner(ctx):
    if ctx.author.id in get_configs()['owners']:
        return True
    raise commands.errors.NotOwner('You do not own this bot.')


async def check_permissions(ctx, perms, *, check=all):
    try:
        if is_owner(ctx):
            return True
    except commands.errors.NotOwner:
        pass

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_permissions(*, check=all, **perms):
    async def pred(ctx):
        return await check_permissions(ctx, perms, check=check)

    return commands.check(pred)


async def bot_check_permissions(ctx, **perms):
    resolved = ctx.channel.permissions_for(ctx.me)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())


def can_send(ctx):
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).send_messages


def can_embed(ctx):
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).embed_links


def can_upload(ctx):
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).attach_files


def can_react(ctx):
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).add_reactions


def can_use_external_emojis(ctx):
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).external_emojis
