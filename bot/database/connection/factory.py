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

from os import getenv
from typing import TYPE_CHECKING, Optional, TypeAlias

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    Session: TypeAlias = sessionmaker[AsyncSession]
else:
    Session: TypeAlias = AsyncSession


class ConnectionFactory:
    """
    Class that creates a connection to the database.
    """
    @staticmethod
    def get_engine(dsn: Optional[str] = None) -> AsyncEngine:
        """
        Creates a engine to the database.

        Parameters
        ----------
            dsn `str`, optional
                The database connection string.

        Returns
        ----------
            `sqlalchemy.ext.asyncio.AsyncEngine`
                An AsyncEngine object.

        """
        if dsn is None:
            user = getenv('DB_USER', '')
            pw = getenv('DB_PASS', '')
            host = getenv('DB_HOST', '')
            port = getenv('DB_PORT', '')
            db_name = getenv('DB_NAME', '')
            dsn = f'postgresql+asyncpg://{user}:{pw}@{host}:{port}/{db_name}'
        return create_async_engine(dsn)

    @staticmethod
    def get_session(engine: Optional[AsyncEngine]) -> Session:
        """
        Creates a session to the database.

        Parameters
        ----------
            engine : `sqlalchemy.ext.asyncio.engine.AsyncEngine`, optional
                An AsyncEngine object.

        Returns
        ----------
            sessionmaker[`sqlalchemy.ext.asyncio.AsyncSession`]
                The session.

        """
        if engine is None:
            engine = ConnectionFactory.get_engine()
        return sessionmaker(
            engine,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession
        )
