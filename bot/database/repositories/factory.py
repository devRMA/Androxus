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

from typing import TYPE_CHECKING, Optional, TypeAlias

from enums import RepositoryType

from .guild_repository import GuildRepository

if TYPE_CHECKING:
    from androxus import Bot
    TBot: TypeAlias = Bot
else:
    TBot: TypeAlias = None


class RepositoryFactory:
    """
    Class that creates a repository instance.
    """
    @staticmethod
    def create(repository_type: RepositoryType, bot: Optional[TBot] = None):
        """
        Creates a repository instance.

        Args:
            repository_type (RepositoryType): The repository type.
            bot (Bot, optional): The bot instance.

        Returns:
            Repository: The repository instance.

        """
        if bot is None:
            from androxus import Bot
            bot = Bot()
        if repository_type == RepositoryType.GUILD:
            return GuildRepository(bot.db_session)
        raise TypeError(
            'The repository type must be a RepositoryType instance.'
        )
