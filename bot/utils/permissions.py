# MIT License

# Copyright(c) 2021-2022 Rafael

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import TYPE_CHECKING, Callable, Iterable, TypeAlias

from discord import Member
from discord.ext import commands

from configs import Configs

if TYPE_CHECKING:
    from androxus import Bot
    TBot: TypeAlias = Bot
else:
    TBot: TypeAlias = None

# code based from:
# https://github.com/AlexFlipnote/discord_bot.py/blob/106cc68decf698f577088784c57f1fbee5bbc3f0/utils/permissions.py


def is_owner(ctx: commands.Context[TBot]) -> bool:
    """
    Check if the user is the owner of the bot.
    """
    if ctx.author.id == Configs.owner_id:
        return True
    raise commands.errors.NotOwner('You are not the owner of the bot.')


async def check_permissions(
    ctx: commands.Context[TBot],
    perms: dict[str, bool],
    *,
    check: Callable[[Iterable[object]], bool] = all
) -> bool:
    """
    Check if the user has the permissions to run the command.

    Parameters
    ----------
    ctx : `discord.ext.commands.Context`
        The context of the command.
    perms : dict[`str`, `bool`]
        The permissions to check.
    check : Callable[[Iterable[`object`]], `bool`], optional
        The function to use to check the permissions. By default all()

    Returns
    -------
    `bool`
        True if the user has the permissions, False otherwise.
    """
    try:
        return is_owner(ctx)
    except commands.errors.NotOwner:
        pass
    if isinstance(ctx.author, Member):
        resolved = ctx.channel.permissions_for(ctx.author)
        return check(
            getattr(resolved, name, None) == value
            for name, value in perms.items()
        )
    return False


def has_permissions(
    *, check: Callable[[Iterable[object]], bool] = all, **perms: bool
):
    """
    Check if the user has the permissions to run the command.

    Parameters
    ----------
    check : Callable[[Iterable[`object`]], `bool`], optional
        The function to use to check the permissions. By default all()
    """
    async def pred(ctx: commands.Context[TBot]) -> bool:
        return await check_permissions(ctx, perms, check=check)

    return commands.check(pred)
