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

from datetime import datetime
from itertools import cycle
from os import getenv, listdir
from os.path import abspath

from aiohttp.client import ClientSession
from database import bootstrap as db_bootstrap
from disnake import Game, Intents
from disnake.ext import commands
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm.session import sessionmaker

# from stopwatch import Stopwatch


def _load_cogs(bot):
    bot.remove_command('help')
    bot.load_extension('jishaku')
    for file in listdir(abspath('./') + '/cogs'):
        if file.endswith('.py'):
            filename = file.removesuffix('.py')
            bot.load_extension(f'cogs.{filename}')


class Bot(commands.Bot):
    __version__ = '3.0a'
    start_date: datetime = datetime.utcnow()
    maintenance: bool = False
    db_session: sessionmaker = None
    http_session: ClientSession = None
    _status = cycle((
        'V3 online',
        'Androxus V3'
    ))

    def __init__(self, *args, **kwargs):
        # self._startup_timer = Stopwatch()

        # async def _prefix_or_mention(bot, message):
        #     prefix = await get_prefix(bot, message)
        #     return commands.when_mentioned_or(prefix)(bot, message)

        kwargs['command_prefix'] = "!!"
        kwargs['owner_id'] = int(getenv('OWNER_ID'))
        kwargs['case_insensitive'] = True
        kwargs['intents'] = Intents.all()
        kwargs['strip_after_prefix'] = True
        kwargs['activity'] = Game(name='😴 Starting ...')
        kwargs['test_guilds'] = [425864977996578816]
        super().__init__(*args, **kwargs)
        _load_cogs(self)

    async def on_ready(self):
        user = getenv('DB_USER')
        pw = getenv('DB_PASS')
        host = getenv('DB_HOST')
        port = getenv('DB_PORT')
        db_name = getenv('DB_NAME')
        dsn = f'postgresql+asyncpg://{user}:{pw}@{host}:{port}/{db_name}'
        engine = create_async_engine(
            dsn
        )
        await db_bootstrap(engine)
        print(f'Logged in as: {self.user}')
