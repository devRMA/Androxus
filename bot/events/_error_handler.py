# type: ignore
# # MIT License

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

from traceback import format_exception
from typing import Final

from disnake import AllowedMentions, CmdInter, Message
from disnake.ext import commands

from androxus import Bot
from language import Translator
from utils import log
from utils.colors import LRED

IGNORED: Final = (commands.CommandNotFound, )


async def error_handler(
    ctx: commands.Context[Bot] | CmdInter, error: commands.CommandError
) -> Message | None:
    """|coro|

    The function will be handler erros raised while invoking a command or
    interaction.

    Parameters
    -----------
    ctx : `disnake.ext.commands.Context` or `disnake.CmdInter`
        The context of the command or interaction.
    error : `disnake.ext.commands.CommandError`
        The Exception raised.

    Returns
    -------
    `disnake.Message` or `None`
        The message that was sent.
    """
    # source:
    # https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612

    if isinstance(ctx, commands.Context):
        # This prevents any commands with local handlers being handled
        # here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return None

        # This prevents any cogs with an overwritten cog_command_error
        # being handled here.
        if (cog := ctx.cog):
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return None

    # Allows us to check for original exceptions raised and sent to
    # CommandInvokeError.
    # If nothing is found. We keep the exception passed to
    # on_command_error.
    error = getattr(error, 'original', error)

    if isinstance(error, IGNORED):
        return None

    trans = await Translator(ctx).init()

    if isinstance(error, commands.errors.NotOwner):
        return await ctx.send(
            f'{ctx.author.mention} ' + trans.__('You are not my creator!')
        )
    elif isinstance(error, commands.errors.UserNotFound):
        return await ctx.send(
            f'{ctx.author.mention} ' +
            trans.__('User `:user` was not found', {'user': error.argument}),
            allowed_mentions=AllowedMentions.none()
        )
    elif isinstance(error, commands.errors.CheckFailure):
        return await ctx.send('nop')
    log(
        'ERROR',
        '\n'.join(format_exception(error)),
        'error',
        first_color=LRED,
        second_color=LRED
    )
