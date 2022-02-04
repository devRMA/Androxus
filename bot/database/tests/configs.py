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
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Optional,
    TypeAlias
)

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession
)
from sqlalchemy.orm import sessionmaker

from utils import log
from utils.colors import (
    CYAN,
    LGREEN,
    LRED,
    LYELLOW,
    RED
)

from ..bootstrap import bootstrap as db_bootstrap
from ..connection import ConnectionFactory
from ..models import __models__


if TYPE_CHECKING:
    TSession: TypeAlias = sessionmaker[AsyncSession]
else:
    TSession: TypeAlias = AsyncSession


class Configs:
    engine: ClassVar[Optional[AsyncEngine]] = None
    session: ClassVar[Optional[TSession]] = None

    @staticmethod
    async def setup() -> None:
        """
        Setup the database connection configurations and create tables.
        """
        log(
            'TEST CONFIGS',
            'PREPARING THE ENVIRONMENT',
            first_color=CYAN,
            second_color=LYELLOW
        )
        user = getenv('DB_TEST_USER')
        db_pass = getenv('DB_TEST_PASS')
        host = getenv('DB_TEST_HOST')
        port = getenv('DB_TEST_PORT')
        db_name = getenv('DB_TEST_NAME')
        dsn = f'postgresql+asyncpg://{user}:{db_pass}@{host}:{port}/{db_name}'
        Configs.engine = ConnectionFactory.get_engine(dsn)
        Configs.session = ConnectionFactory.get_session(Configs.engine)
        await Configs._drop_tables()
        await db_bootstrap(Configs.engine)
        log(
            'TEST CONFIGS',
            'SUCCESSFULLY CONFIGURED ENVIRONMENT',
            first_color=CYAN,
            second_color=LGREEN
        )

    @staticmethod
    async def teardown() -> None:
        """
        Teardown the database connection configurations and drop tables.
        """
        log(
            'TEST CONFIGS',
            'CLEANING THE ENVIRONMENT',
            first_color=CYAN,
            second_color=LYELLOW
        )
        await Configs._drop_tables()
        if Configs.session is not None:
            Configs.session = None
        if Configs.engine is not None:
            await Configs.engine.dispose()
            Configs.engine = None
        log(
            'TEST CONFIGS',
            'SUCCESSFULLY CLEAN ENVIRONMENT',
            first_color=CYAN,
            second_color=LGREEN
        )

    @staticmethod
    async def _drop_tables() -> None:
        """
        Drops all tables in the database.
        """
        log(
            'TEST CONFIGS',
            'DELETING TABLES',
            first_color=CYAN,
            second_color=RED
        )
        for model in __models__:
            if Configs.engine is not None:
                await model.drop_table(Configs.engine)
        log(
            'TEST CONFIGS',
            'TABLES SUCCESSFULLY DELETED',
            first_color=CYAN,
            second_color=LRED
        )
