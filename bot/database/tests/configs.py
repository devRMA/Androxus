from os import getenv

from colorama import Fore

from database import bootstrap as db_bootstrap
from database.models import __models__
from utils import log
from ..factories import ConnectionFactory


class Configs:
    engine = None
    session = None

    @staticmethod
    async def setup():
        log('TEST CONFIGS', 'PREPARING THE ENVIRONMENT', Fore.CYAN, Fore.LIGHTYELLOW_EX)
        user = getenv('DB_TEST_USER')
        db_pass = getenv('DB_TEST_PASS')
        host = getenv('DB_TEST_HOST')
        port = getenv('DB_TEST_PORT')
        db_name = getenv('DB_TEST_NAME')
        dsn = f'postgresql+asyncpg://{user}:{db_pass}@{host}:{port}/{db_name}'
        Configs.engine = ConnectionFactory.get_engine(
            dsn
        )
        Configs.session = ConnectionFactory.get_session(Configs.engine)
        await Configs.__drop_tables()
        await db_bootstrap(Configs.engine)
        log('TEST CONFIGS', 'SUCCESSFULLY CONFIGURED ENVIRONMENT', Fore.CYAN, Fore.LIGHTGREEN_EX)

    @staticmethod
    async def teardown():
        log('TEST CONFIGS', 'CLEANING THE ENVIRONMENT', Fore.CYAN, Fore.LIGHTYELLOW_EX)
        await Configs.__drop_tables()
        if Configs.session is not None:
            Configs.session = None
        if Configs.engine is not None:
            await Configs.engine.dispose()
            Configs.engine = None
        log('TEST CONFIGS', 'SUCCESSFULLY CLEAN ENVIRONMENT', Fore.CYAN, Fore.LIGHTGREEN_EX)

    @staticmethod
    async def __drop_tables():
        log('TEST CONFIGS', 'DELETING TABLES', Fore.CYAN, Fore.RED)
        for model in __models__:
            await model.drop_table(Configs.engine)
        log('TEST CONFIGS', 'TABLES SUCCESSFULLY DELETED', Fore.CYAN, Fore.LIGHTRED_EX)
