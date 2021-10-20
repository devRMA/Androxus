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

from os import getenv
from typing import List

from disnake import Permissions


class Configs:
    """
    This class is used to store the configuration of the bot.

    Attributes:
        default_prefix (str): The default prefix for the bot.
        prefix (str): An alias for default_prefix.
        required_permissions (disnake.Permissions): The permissions
        necessary for all bot commands to work.
        owner_id (int): The ID of the bot owner.
        test_guilds (List[int]): The ids of the servers you want to test the
        slash commands

    """
    default_prefix: str = getenv('DEFAULT_PREFIX')
    prefix: str = default_prefix
    required_permissions: Permissions = Permissions(8)
    owner_id: int = int(getenv('OWNER_ID'))

    @property
    def test_guilds(self) -> List[int]:
        """
        The IDs of the test guilds.

        Returns:
            List[int]: The list of test guild IDs.

        """
        test_guilds = getenv('TEST_GUILDS')
        if test_guilds != '':
            if test_guilds.count(',') > 0:
                if test_guilds.count('[') == 1 and test_guilds.count(']') == 1:
                    return [
                        int(_id.replace(' ', ''))
                        for _id in test_guilds.replace(
                            '[', '').replace(
                            ']', '').split(',')
                    ]
        return []