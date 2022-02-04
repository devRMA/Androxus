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
from disnake.ext.commands import Context  # type: ignore

from androxus import Bot
from common import ConfigsCommands
from utils.permissions import has_permissions


class ConfigsNormal(commands.Cog):
    @commands.command(aliases=['lang'])
    @has_permissions(manage_messages=True)
    async def language(self, ctx: Context[Bot]) -> Message | None:
        """
        Changes the language of the bot, for the current guild
        """
        configs_commands = ConfigsCommands(ctx)
        await configs_commands.init()
        return await configs_commands.language()


def setup(bot: Bot) -> None:
    bot.add_cog(ConfigsNormal())
