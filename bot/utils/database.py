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

from disnake import Message
from disnake.ext.commands import Bot as DisnakeBot  # type: ignore
from disnake.ext.commands import Context  # type: ignore
from enums import RepositoryType

from database.repositories import RepositoryFactory


async def get_prefix(
    bot: DisnakeBot, message: Message | Context[DisnakeBot]
) -> str:
    """
    Get the prefix for the message.

    Args:
        bot (androxus.Bot): The bot instance.
        message (Message or Context): The message or context, instance.

    Returns:
        str: The prefix.

    """
    if message.guild:
        guild_repository = RepositoryFactory.create(RepositoryType.GUILD, bot)
        guild = await guild_repository.find_by_id_or_create(message.guild.id)
        return guild.prefix
    return bot.configs.default_prefix  # type: ignore
