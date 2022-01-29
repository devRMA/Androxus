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

from disnake import Message
from disnake.ext import commands
from disnake.ext.commands.context import Context  # type: ignore

from androxus import Bot
from common import DevCommands


class DevNormal(commands.Cog):
    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx: Context[Bot]) -> Message | None:
        """
        Reloads all cogs
        """
        dev_commands = DevCommands(ctx)
        await dev_commands.init()
        return await dev_commands.reload()


def setup(bot: Bot):
    bot.add_cog(DevNormal())
