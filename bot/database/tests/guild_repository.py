from config import Config
from . import Configs
from . import Test
from ..models import Guild
from ..repositories import GuildRepository

GUILD_ID_TEST = 123456789
DEFAULT_PREFIX = Config.DEFAULT_PREFIX
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

    async def test_4_guild_get_fail(self):
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
