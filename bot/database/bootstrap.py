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
                log('BOOTSTRAPPING DB',
                    f'CREATING TABLE "{table_name}"', Fore.CYAN, Fore.LIGHTYELLOW_EX)
                await model.create_table(engine)
    log('BOOTSTRAPPING DB', 'TABLES CHECKING COMPLETED',
        Fore.CYAN, Fore.LIGHTYELLOW_EX)


async def bootstrap(engine: AsyncEngine):
    """
    Bootstrap the database.

    Args:
        engine (sqlalchemy.ext.asyncio.engine.AsyncEngine): The database engine.

    """
    log('BOOTSTRAPPING DB', 'STARTING', Fore.CYAN, Fore.WHITE)
    await check_tables(engine)
    log('BOOTSTRAPPING DB', 'DONE', Fore.CYAN, Fore.WHITE)
