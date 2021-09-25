from config import Config
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Guild(Base):
    """
    Represents a guild in the database.


    Attributes:
        id (int): The guild's ID.
        prefix (str): The guild's prefix.

    """
    __tablename__ = 'guilds'
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=False,
        nullable=False
    )
    prefix = Column(String(10), nullable=False)

    def __init__(self, id, prefix=None):
        self.id = id
        self.prefix = prefix or Config.DEFAULT_PREFIX

    @staticmethod
    async def create_table(engine: AsyncEngine):
        """
        Creates the "guilds" table.

        Args:
            engine (sqlalchemy.ext.asyncio.engine.AsyncEngine): The database engine.

        """
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
