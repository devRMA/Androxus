from colorama import Fore
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database.models import __models__
from utils import log


async def check_tables(engine: AsyncEngine):
    """
    Check if tables exist, if not create them

    Args:
        engine (sqlalchemy.ext.asyncio.engine.AsyncEngine): The database engine.

    """
    log('BOOTSTRAPPING DB', 'CHECKING TABLES', Fore.CYAN, Fore.LIGHTYELLOW_EX)
    async with engine.connect() as conn:
        for model in __models__:
            table_name = model.__tablename__
            if not await conn.run_sync(
                    lambda con: inspect(con).has_table(table_name)
            ):
                log('BOOTSTRAPPING DB', f'CREATING TABLE "{table_name}"', Fore.CYAN, Fore.LIGHTYELLOW_EX)
                await model.create_table(engine)
    log('BOOTSTRAPPING DB', 'TABLES CHECKING COMPLETED', Fore.CYAN, Fore.LIGHTYELLOW_EX)


async def bootstrap(engine: AsyncEngine):
    """
    Bootstrap the database.

    Args:
        engine (sqlalchemy.ext.asyncio.engine.AsyncEngine): The database engine.

    """
    log('BOOTSTRAPPING DB', 'STARTING', Fore.CYAN, Fore.WHITE)
    await check_tables(engine)
    log('BOOTSTRAPPING DB', 'DONE', Fore.CYAN, Fore.WHITE)
