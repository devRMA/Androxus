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

from __future__ import annotations

from configs import Configs
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base

from .model import Model

Base = declarative_base()


class Guild(Base, Model):
    """
    Represents a guild in the database.

    Args:
        id (int): The guild id
        prefix (str, optional): The guild prefix.
        language (str, optional): The guild language.

    Attributes:
        id (int): The guild's ID.
        prefix (str): The guild's prefix.
        language (str): The guild's language.

    """
    __tablename__ = 'guilds'
    id = Column(
        BigInteger, primary_key=True, autoincrement=False, nullable=False
    )
    prefix = Column(String(10), nullable=False)
    language = Column(String(255), nullable=False)

    def __init__(self, id_, prefix=None, language=None):
        self.id = id_
        self.prefix = prefix or Configs.default_prefix
        self.language = language or Configs.default_language

    def __eq__(self, other):
        return isinstance(other, Guild) and (self.id == other.id)

    @staticmethod
    async def create_table(engine: AsyncEngine):
        """
        Creates the "guilds" table.

        Args:
            engine (sqlalchemy.ext.asyncio.engine.AsyncEngine): The database engine.

        """
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def drop_table(engine: AsyncEngine):
        """
        Drops the "guilds" table.

        Args:
            engine (sqlalchemy.ext.asyncio.engine.AsyncEngine): The database engine.

        """
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the guild.

        Returns:
            dict: The guild's dictionary representation.

        """
        return {'id': self.id, 'prefix': self.prefix, 'language': self.language}
