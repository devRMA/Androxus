from inspect import iscoroutinefunction
from traceback import format_exc

from colorama import Fore

from database.tests import Configs
from database.tests.guild_repository import GuildRepositoryTest
from utils import log


async def make_tests():
    await Configs.setup()
    tests_class = [GuildRepositoryTest]
    log('TESTING', 'STARTING DATABASE TESTS')
    for test_class in tests_class:
        table_name = test_class.__name__.removesuffix('RepositoryTest')
        log('TESTING', f'TESTS FOR MODEL "{table_name}"', Fore.CYAN, Fore.MAGENTA)
        tests = sorted(func for func in dir(test_class)
                       if func.startswith('test_'))
        test_obj = test_class()
        for test in tests:
            try:
                method = test_obj.__getattribute__(test)
                if iscoroutinefunction(method):
                    await method()
                else:
                    method()
                log('TESTING', f'{test} SUCCESS')
            except:
                log('TESTING', f'{test} ERROR')
                print(format_exc())
    await Configs.teardown()
    log('TESTING', 'DATABASE TESTS SUCCESSFULLY')
