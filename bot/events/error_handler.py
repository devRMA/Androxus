# type: ignore
# # MIT License

# Copyright(c) 2021 Rafael

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

from disnake import AllowedMentions
from disnake.ext import commands

from androxus import Bot
from language import Translator


class ErrorHandler(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context[Bot], error: commands.CommandError
    ):
        """
        The event triggered when an error is raised while invoking a command.

        Args:
            ctx (commands.Context): The context used for command invocation.
            error (commands.CommandError): The Exception raised.

        """
        # source:
        # https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612

        # This prevents any commands with local handlers being handled
        # here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error
        # being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(
                cog.cog_command_error
            ) is not None:
                return

        ignored = (commands.CommandNotFound, )

        # Allows us to check for original exceptions raised and sent to
        # CommandInvokeError.
        # If nothing is found. We keep the exception passed to
        # on_command_error.
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        trans = await Translator(ctx).init()

        if isinstance(error, commands.errors.NotOwner):
            return await ctx.send(
                f'{ctx.author.mention} ' + trans.__('You are not my creator!')
            )
        elif isinstance(error, commands.errors.UserNotFound):
            return await ctx.send(
                f'{ctx.author.mention} ' + trans.
                __('User `:user` was not found', {'user': error.argument}),
                allowed_mentions=AllowedMentions.none()
            )
        else:
            print(error)
            print(type(error))


def setup(bot: Bot):
    bot.add_cog(ErrorHandler())
