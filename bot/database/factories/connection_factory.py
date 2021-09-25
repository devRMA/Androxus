from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker


class ConnectionFactory:
    """
    Class that creates a connection to the database.
    """

    @staticmethod
    def get_engine(dsn: str = None) -> AsyncEngine:
        """
        Creates a engine to the database.

        Args:
            dsn (str, optional): The database connection string.

        Returns:
            sqlalchemy.ext.asyncio.AsyncEngine: An AsyncEngine object.

        """
        if dsn is None:
            user = getenv('DB_USER')
            pw = getenv('DB_PASS')
            host = getenv('DB_HOST')
            port = getenv('DB_PORT')
            db_name = getenv('DB_NAME')
            dsn = f'postgresql+asyncpg://{user}:{pw}@{host}:{port}/{db_name}'
        return create_async_engine(dsn)

    @staticmethod
    def get_session(engine: AsyncEngine = None) -> AsyncSession:
        """
        Creates a session to the database.

        Args:
            engine (sqlalchemy.ext.asyncio.engine.AsyncEngine, optional): An AsyncEngine object.

        Returns:
            sqlalchemy.ext.asyncio.AsyncSession: An AsyncSession object.

        """
        if engine is None:
            engine = ConnectionFactory.get_engine()
        return sessionmaker(
            engine,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession
        )
