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

from disnake.ext import commands

from androxus import Bot

from ._error_handler import error_handler


class OnCommandError(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context[Bot], exception: commands.CommandError
    ) -> None:
        """
        The event triggered when an error is raised while invoking a command.

        Parameters
        ----------
        ctx : `disnake.ext.commands.Context`
            The context used for command invocation.
        exception : `disnake.ext.commands.CommandError`
            The Exception raised.
        """
        await error_handler(ctx, exception)


def setup(bot: Bot) -> None:
    bot.add_cog(OnCommandError())
