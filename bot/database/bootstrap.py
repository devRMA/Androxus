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

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database.models import __models__
from utils import log
from utils.colors import CYAN, LYELLOW, WHITE


async def check_tables(engine: AsyncEngine) -> None:
    """|coro|

    Check if tables exist, if not create them

    Parameters
    ----------
        engine : `sqlalchemy.ext.asyncio.engine.AsyncEngine`
            The database engine.
    """
    log(
        'BOOTSTRAPPING DB',
        'CHECKING TABLES',
        first_color=CYAN,
        second_color=LYELLOW
    )
    async with engine.connect() as conn:
        for model in __models__:
            table_name = model.__tablename__
            if not await conn.run_sync(
                lambda con: inspect(con).has_table(table_name)
            ):
                log(
                    'BOOTSTRAPPING DB',
                    f'CREATING TABLE "{table_name}"',
                    first_color=CYAN,
                    second_color=LYELLOW
                )
                await model.create_table(engine)
    log(
        'BOOTSTRAPPING DB',
        'TABLES CHECKING COMPLETED',
        first_color=CYAN,
        second_color=LYELLOW
    )


async def bootstrap(engine: AsyncEngine) -> None:
    """|coro|

    Bootstrap the database.

    Parameters
    ----------
        engine : `sqlalchemy.ext.asyncio.engine.AsyncEngine`
            The database engine.
    """
    log('BOOTSTRAPPING DB', 'STARTING', first_color=CYAN, second_color=WHITE)
    await check_tables(engine)
    log('BOOTSTRAPPING DB', 'DONE', first_color=CYAN, second_color=WHITE)
