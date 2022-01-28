# MIT License

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

from typing import Optional

from disnake import (
    Member,
    Message,
    User
)
from disnake.ext import commands
from disnake.ext.commands.context import Context  # type: ignore

from androxus import Bot
from common import InfoCommands


class InfoNormal(commands.Cog):
    @commands.command(aliases=['latency'])
    async def ping(self, ctx: Context[Bot]) -> Optional[Message]:
        """
        Get the bot latency
        """
        info_commands = InfoCommands(ctx)
        await info_commands.init()
        return await info_commands.ping()

    @commands.command(aliases=['ut'])
    async def uptime(self, ctx: Context[Bot]) -> Optional[Message]:
        """
        Get the bot uptime
        """
        info_commands = InfoCommands(ctx)
        await info_commands.init()
        return await info_commands.uptime()

    @commands.command(aliases=['av'])
    async def avatar(self, ctx: Context[Bot],
                     user: Optional[Member | User]) -> Optional[Message]:
        """
        Get the user avatar
        """
        user = user or ctx.author
        info_commands = InfoCommands(ctx)
        await info_commands.init()
        return await info_commands.avatar(user)


def setup(bot: Bot):
    bot.add_cog(InfoNormal())
