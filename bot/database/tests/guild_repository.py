from traceback import format_exc

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import exc

from . import Configs
from . import Test
from ..models import Guild
from ..repositories import GuildRepository


class GuildRepositoryTest(Test):
    def __init__(self):
        self.session = Configs.session
        self.repository = GuildRepository(self.session)

    async def test_01_guild_create(self):
        guild = Guild(123456789)
        result = await self.repository.create(123456789)
        self.assert_equal(guild, result)

    async def test_02_guild_duplicate_value(self):
        try:
            await self.repository.create(123456789)
        except exc.SQLAlchemyError as error:
            print(error)
            print('full stack:')
            print(format_exc())
            self.assert_is_instance(error, UniqueViolationError)
