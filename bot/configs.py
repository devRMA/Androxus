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

from os import getenv
from typing import ClassVar

from discord import Intents, Locale, Permissions


class Configs:
    """
    This class is used to store the configuration of the bot.

    Attributes
    -----------
        default_prefix: `str`
            The default prefix for the bot.
        prefix: `str`
            An alias for default_prefix.
        required_permissions: `discord.Permissions`
            The permissions required to use the bot.
        owner_id: `int`
            The ID of the bot's owner.
        default_language: `str`
            The default language for the bot.
        language: `str`
            An alias for default_language.
        test_guilds: list[`int`]
            The ids of the servers you want to test the slash commands
    """
    default_prefix: ClassVar[str] = getenv('DEFAULT_PREFIX', '')
    prefix: ClassVar[str] = default_prefix
    # TODO : Use only the necessary permissions
    required_permissions: ClassVar[Permissions] = Permissions(8)
    owner_id: ClassVar[int] = int(getenv('OWNER_ID', 0))
    default_language: ClassVar[str] = str(
        Locale[getenv('DEFAULT_LANGUAGE', 'american_english')]
    )
    language: ClassVar[str] = default_language
    # TODO : Use only the necessary intents
    intents: ClassVar[Intents] = Intents.all()

    @property
    def test_guilds(self) -> list[int]:
        """list[`int`]: The list of test guild IDs."""
        if len(test_guilds := eval(getenv('TEST_GUILDS', '[]'))) > 0:
            return test_guilds
        return []
