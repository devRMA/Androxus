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

from typing import Any, Optional

from sqlalchemy import BigInteger, Column, String
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import declarative_base

from configs import Configs

from .model import Model

Base = declarative_base()


class Guild(Model, Base):
    """
    Represents a guild in the database.

    Parameters
    ----------
        id : `int`
            The guild id
        prefix : `str`, optional
            The guild prefix.

    Attributes
    ----------
        id : `int`
            The guild's ID.
        prefix : `str`
            The guild's prefix.
    """
    __tablename__ = 'guilds'
    id = Column(
        BigInteger, primary_key=True, autoincrement=False, nullable=False
    )
    prefix = Column(String(10), nullable=False)

    def __init__(
        self,
        id_: int,
        prefix: Optional[str] = None,
    ) -> None:
        super().__init__(id_)
        self.prefix = prefix or Configs.default_prefix

    @staticmethod
    async def create_table(engine: AsyncEngine) -> None:
        """
        Creates the "guilds" table.

        Parameters
        ----------
            engine : `sqlalchemy.ext.asyncio.engine.AsyncEngine`
                The database engine.
        """
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def drop_table(engine: AsyncEngine) -> None:
        """
        Drops the "guilds" table.

        Parameters
        ----------
            engine : `sqlalchemy.ext.asyncio.engine.AsyncEngine`
                The database engine.
        """
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    def to_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary representation of the guild.

        Returns
        ----------
            dict[`str`, `Any`]
                The guild's dictionary representation.
        """
        return {'id': self.id, 'prefix': self.prefix}
