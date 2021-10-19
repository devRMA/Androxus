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

from typing import Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.session import sessionmaker

from database.models import Guild


class GuildRepository:
    """
    Class to manipulate the "guilds" table

    Args:
        session (sqlalchemy.orm.session.sessionmaker): The session to use to interact with the database.

    """

    def __init__(self, session: sessionmaker):
        self.session = session

    @staticmethod
    async def __get_by_id(session: AsyncSession, guild_id: int) -> Optional[Guild]:
        """
        Get a guild by its id

        Args:
            session (sqlalchemy.ext.asyncio.AsyncSession): The session to use to interact with the database.
            guild_id (int): The id of the guild to get.

        Returns:
            database.models.Guild: The guild object.

        """
        stmt = select(Guild).where(Guild.id == guild_id)
        return (await session.execute(stmt)).scalars().first()

    async def __exists(self, guild_id: int) -> bool:
        """
        Check if a guild exists

        Args:
            guild_id (int): The id of the guild to check.

        Returns:
            bool: True if the guild exists, False otherwise.

        """
        guild = await self.find(guild_id)
        return guild is not None

    async def find(self, guild_id: int) -> Optional[Guild]:
        """
        Get a guild by id

        Args:
            guild_id (int): The id of the guild to get.

        Returns:
            database.models.Guild: The guild object.

        """
        async with self.session() as session:
            return await self.__get_by_id(session, guild_id)

    async def create(self, guild_id: int) -> Optional[Guild]:
        """
        Create a new guild with default values

        Args:
            guild_id (int): The id of the guild to create.

        Returns:
            database.models.Guild: The guild object.

        """
        if await self.__exists(guild_id):
            return await self.find(guild_id)
        else:
            guild = Guild(guild_id)
            await self.save(guild)
            return guild

    async def save(self, guild: Guild):
        """
        Save a guild to the database

        Args:
            guild (database.models.Guild): The guild to save.

        """
        if not (await self.__exists(guild.id)):
            async with self.session() as session:
                session.add(guild)
                await session.commit()

    async def update(self, guild) -> bool:
        if await self.__exists(guild.id):
            async with self.session() as session:
                db_guild = await self.__get_by_id(session, guild.id)
                db_guild.merge(guild)
                await session.commit()
        else:
            await self.save(guild)

    async def delete(self, guild: Union[Guild, int]) -> bool:
        """
        Delete a guild

        Args:
            guild (database.models.Guild or int): The guild (or id) to delete.

        Returns:
            bool: True if the guild was deleted, False otherwise.

        """
        if isinstance(guild, int):
            if await self.__exists(guild):
                guild_to_delete = await self.find(guild)
            else:
                return False
        elif isinstance(guild, Guild):
            if await self.__exists(guild.id):
                guild_to_delete = guild
            else:
                return False
        else:
            return False
        async with self.session() as session:
            await session.delete(guild_to_delete)
            await session.commit()
            return True
