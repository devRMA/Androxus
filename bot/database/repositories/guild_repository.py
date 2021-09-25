from typing import Optional, Union

from database.models import Guild
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class GuildRepository:
    """
    Class to manipulate the "guilds" table

    Args:
        session (sqlalchemy.ext.asyncio.AsyncSession): The session to use to interact with the database.

    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __get_by_id(self, session: AsyncSession, guild_id: int) -> Optional[Guild]:
        """
        Get a guild by its id

        Args:
            session (sqlalchemy.orm.session.Session): The session to use to interact with the database.
            guild_id (int): The id of the guild to get.

        Returns:
            database.models.Guild: The guild object.

        """
        stmt = select(Guild).where(Guild.id == guild_id)
        return (await session.execute(stmt)).scalars().first()

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
        async with self.session() as session:
            try:
                guild = Guild(guild_id)
                session.add(guild)
                await session.commit()
                return guild
            except Exception as e:
                print(e)
                await session.rollback()
                return None

    async def save(self, guild: Guild) -> bool:
        """
        Save a guild to the database

        Args:
            guild (database.models.Guild): The guild to save.

        Returns:
            bool: True if the guild was saved, False otherwise.

        """
        async with self.session() as session:
            try:
                session.add(guild)
                await session.commit()
                return True
            except:
                await session.rollback()
                return False

    async def delete(self, guild: Union[Guild, int]) -> bool:
        """
        Delete a guild

        Args:
            guild (database.models.Guild or int): The guild (or id) to delete.

        Returns:
            bool: True if the guild was deleted, False otherwise.

        """
        async with self.session() as session:
            try:
                guild_to_delete = None
                if isinstance(guild, int):
                    guild_to_delete = await self.__get_by_id(session, guild)
                elif isinstance(guild, Guild):
                    guild_to_delete = guild
                else:
                    return False
                await session.delete(guild_to_delete)
                await session.commit()
                return True
            except:
                await session.rollback()
                return False
