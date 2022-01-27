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

from androxus import Bot
from common import InfoCommands
from disnake import CommandInteraction as Interaction
from disnake import Member, Message, User
from disnake.ext import commands


def _return_author(inter: Interaction) -> Member | User:
    return inter.author


class InfoSlash(commands.Cog):
    @commands.slash_command()  # type: ignore
    async def ping(self, inter: Interaction) -> Optional[Message]:
        """
        Get the bot latency
        """
        info_commands = InfoCommands(inter)
        await info_commands.init()
        return await info_commands.ping()

    @commands.slash_command()  # type: ignore
    async def uptime(self, inter: Interaction) -> Optional[Message]:
        """
        Get the bot uptime
        """
        info_commands = InfoCommands(inter)
        await info_commands.init()
        return await info_commands.uptime()

    @commands.slash_command()  # type: ignore
    async def avatar(
        self,
        inter: Interaction,
        user: Member | User = commands.Param(_return_author),
    ) -> Optional[Message]:
        """Get the user avatar

        Parameters
        ----------
        user: The user to get the avatar from, defaults to the author

        """
        info_commands = InfoCommands(inter)
        await info_commands.init()
        return await info_commands.avatar(user)


def setup(bot: Bot):
    bot.add_cog(InfoSlash())
