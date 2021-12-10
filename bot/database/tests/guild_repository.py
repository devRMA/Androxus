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

from configs import Configs as ConfigsBot

from ..models import Guild
from ..repositories import GuildRepository
from . import Configs, Test

GUILD_ID_TEST = 123456789
DEFAULT_PREFIX = ConfigsBot.default_prefix
CHANGED_PREFIX = DEFAULT_PREFIX + '..'


class GuildRepositoryTest(Test):
    def __init__(self):
        self.session = Configs.session
        self.repository = GuildRepository(self.session)

    async def test_01_guild_create(self):
        guild = Guild(GUILD_ID_TEST)
        result = await self.repository.create(GUILD_ID_TEST)
        self.assert_equal(guild, result)

    async def test_02_guild_duplicate_value(self):
        result = await self.repository.create(GUILD_ID_TEST)
        guild = await self.repository.find(GUILD_ID_TEST)
        self.assert_equal(guild, result)

    async def test_03_guild_get(self):
        guild = await self.repository.find(GUILD_ID_TEST)
        self.assert_is_not_none(guild)
        self.assert_equal(guild.id, GUILD_ID_TEST)
        self.assert_equal(guild.prefix, DEFAULT_PREFIX)

    async def test_04_guild_get_fail(self):
        result = await self.repository.find(GUILD_ID_TEST + 2)
        self.assert_is_none(result)

    async def test_05_guild_update(self):
        guild = await self.repository.find(GUILD_ID_TEST)
        guild.prefix = CHANGED_PREFIX
        await self.repository.update(guild)

    async def test_06_guild_update_confirm(self):
        guild = await self.repository.find(GUILD_ID_TEST)
        self.assert_equal(guild.id, GUILD_ID_TEST)
        self.assert_equal(guild.prefix, CHANGED_PREFIX)

    async def test_07_guild_delete_by_id(self):
        guild = await self.repository.find(GUILD_ID_TEST)
        result = await self.repository.delete(guild)
        self.assert_true(result)

    async def test_08_guild_delete_confirm(self):
        result = await self.repository.find(GUILD_ID_TEST)
        self.assert_is_none(result)

    async def test_09_guild_delete_by_object(self):
        guild = await self.repository.create(GUILD_ID_TEST)
        result = await self.repository.delete(guild)
        self.assert_true(result)

    async def test_10_guild_delete_fail(self):
        result = await self.repository.delete(GUILD_ID_TEST)
        self.assert_false(result)
