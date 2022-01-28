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

from inspect import iscoroutinefunction
from traceback import format_exc

from utils import (
    CYAN,
    MAGENTA,
    log
)

from .configs import Configs
from .guild_repository import GuildRepositoryTest


async def make_tests():
    await Configs.setup()
    tests_class = [GuildRepositoryTest]
    log('TESTING', 'STARTING DATABASE TESTS')
    for test_class in tests_class:
        table_name = test_class.__name__.removesuffix('RepositoryTest')
        log(
            'TESTING',
            f'TESTS FOR MODEL "{table_name}"',
            first_color=CYAN,
            second_color=MAGENTA
        )
        tests = sorted(
            func for func in dir(test_class) if func.startswith('test_')
        )
        test_obj = test_class()
        for test in tests:
            try:
                method = test_obj.__getattribute__(test)
                if iscoroutinefunction(method):
                    await method()
                else:
                    method()
                log('TESTING', f'{test} SUCCESS')
            except BaseException:
                log('TESTING', f'{test} ERROR')
                print(format_exc())
    await Configs.teardown()
    log('TESTING', 'DATABASE TESTS SUCCESSFULLY')
