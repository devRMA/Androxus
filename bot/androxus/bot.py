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
from os import listdir, getenv
from os.path import abspath

from aiohttp.client import ClientSession
from disnake import __version__ as disnake_version
from configs import Configs
from database import bootstrap as db_bootstrap
from database.factories.connection_factory import ConnectionFactory
from disnake import Game, Intents
from disnake.ext import commands
from disnake.utils import utcnow
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from stopwatch import Stopwatch
from utils import log
from utils.colors import LBLUE, LGREEN, LYELLOW
from utils.database import get_prefix


def _load_cogs(bot):
    """
    Loads all cogs of the bot.

    Args:
        bot (Bot): The bot instance.

    """
    # bot.remove_command('help')
    bot.load_extension('jishaku')
    paths = ['message', 'normal', 'slash', 'user']
    for path in paths:
        for file in listdir(abspath('./') + '/commands/' + path):
            if file.endswith('.py'):
                filename = file.removesuffix('.py')
                bot.load_extension(f'commands.{path}.{filename}')


class Bot(commands.Bot):
    """
    The main class of the bot.

    Attributes:
        __version__ (str): The current version of the bot.
        start_date (datetime): The date when the bot was started.
        maintenance (bool): Whether the bot is in maintenance mode.
        db_engine (AsyncEngine): The database engine.
        db_session (AsyncSession): The database session.
        http_session (ClientSession): The aiohttp session.

    """
    __version__ = '3.0a'
    start_date: datetime = None
    maintenance: bool = False
    db_engine: AsyncEngine = None
    db_session: AsyncSession = None
    http_session: ClientSession = None
    configs: Configs = Configs()
    _status = cycle((
        'V3 online',
        'Androxus V3'
    ))
    _startup_timer: Stopwatch = None

    def __init__(self, *args, **kwargs):
        self._startup_timer = Stopwatch()
        log('BOT', 'STARTING BOT...', first_color=LYELLOW)

        async def _prefix_or_mention(bot, message):
            prefix = await get_prefix(bot, message)
            return commands.when_mentioned_or(prefix)(bot, message)

        kwargs['command_prefix'] = _prefix_or_mention
        kwargs['owner_id'] = self.configs.owner_id
        kwargs['case_insensitive'] = True
        kwargs['intents'] = Intents.all()
        kwargs['strip_after_prefix'] = True
        kwargs['activity'] = Game(name='😴 Starting ...')
        kwargs['test_guilds'] = self.configs.test_guilds
        super().__init__(*args, **kwargs)
        _load_cogs(self)

    async def on_ready(self) -> None:
        if self.db_session is None or self.db_engine is None:
            self._startup_timer.stop()
            self.db_engine = ConnectionFactory.get_engine()
            self.db_session = ConnectionFactory.get_session(self.db_engine)
            self.start_date = utcnow()
            await db_bootstrap(self.db_engine)
            log('BOT', f'LOGGED IN {self.user}', first_color=LGREEN)
            log('BOT', f'ID: {self.user.id}', first_color=LGREEN)
            log('INFO', f'{len(set(self.get_all_members()))} USERS!',
                first_color=LBLUE)
            log('INFO', f'{len(self.guilds)} GUILDS!',
                first_color=LBLUE)
            log('INFO', f'BOT VERSION: {self.__version__}',
                first_color=LBLUE)
            log('INFO', 'PYTHON VERSION: ' + getenv('PYTHON_VERSION'),
                first_color=LBLUE)
            log('INFO', f'DISNAKE VERSION: {disnake_version}',
                first_color=LBLUE)
            log('INFO', f'TIME TO START: {self._startup_timer}',
                first_color=LBLUE)
