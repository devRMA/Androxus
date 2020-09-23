# coding=utf-8
# Androxus bot
# permissions.py

# font: https://github.com/AlexFlipnote/discord_bot.py

import discord
from discord.ext import commands


def is_owner(ctx):
    return ctx.author.id == 305532760083398657


async def check_permissions(ctx, perms, *, check=all):
    if is_owner(ctx):
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_permissions(*, check=all, **perms):
    async def pred(ctx):
        return await check_permissions(ctx, perms, check=check)

    return commands.check(pred)

