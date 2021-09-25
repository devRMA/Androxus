from colorama import Fore
from sqlalchemy import inspect
from utils import log

from database.models import __models__


async def check_tables(engine):
    log('BOOTSTRAPING DB', 'CHECKING TABLES')
    async with engine.connect() as conn:
        for model in __models__:
            table_name = model.__tablename__
            if not await conn.run_sync(
                lambda con: inspect(con).has_table(table_name)
            ):
                log(
                    'BOOTSTRAPING DB',
                    f'CREATING TABLE {table_name}'
                )
                await model.create_table(engine)


async def bootstrap(engine):
    await check_tables(engine)
    log(
        'BOOTSTRAPING DB',
        'DONE'
    )
