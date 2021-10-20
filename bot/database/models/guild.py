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

from config import Config
from database.models.model import Model
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Guild(Base, Model):
    """
    Represents a guild in the database.

    Args:
        id (int): The guild id
        prefix (str, optional): The guild prefix.

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

    def __init__(self, id_, prefix=None):
        self.id = id_
        self.prefix = prefix or Config.DEFAULT_PREFIX

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
        return {
            'id': self.id,
            'prefix': self.prefix
        }

    def diff_in_dict(self, other: Guild) -> dict:
        """
        Returns a dictionary representation of the difference between the guild and another guild.

        Args:
            other (database.models.guild.Guild): The guild to compare to.

        Returns:
            dict: The guild's dictionary representation.

        """
        # check if it has the same id and is of the same class
        if self != other:
            return {}
        other_dict = other.to_dict()
        self_dict = self.to_dict()
        diff_dict = {}
        for key in other_dict.keys():
            if self_dict[key] != other_dict[key]:
                diff_dict[key] = other_dict[key]
        return diff_dict

    def fill(self, params: dict):
        """
        Update the guild with the given parameters.

        Args:
            params (dict): The parameters to update the guild with.

        """
        for key, value in params.items():
            if key == 'id':
                continue
            setattr(self, key, value)

    def merge(self, other: Guild):
        """
        Merge the guild with another guild.

        Args:
            other (database.models.guild.Guild): The guild to merge with.

        """
        self.fill(self.diff_in_dict(other))
