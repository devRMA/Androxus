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
from os import listdir
from os.path import abspath
from platform import python_version
from typing import Any, Dict, List, MutableMapping

from aiohttp.client import ClientSession
from configs import Configs
from database import bootstrap as db_bootstrap
from database.connection import ConnectionFactory
from disnake import Game, Intents, Message
from disnake import __version__ as disnake_version
from disnake.ext import commands, tasks
from disnake.utils import utcnow
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore
from sqlalchemy.ext.asyncio.engine import AsyncEngine  # type: ignore
from stopwatch import Stopwatch
from toml import load
from utils import SingletonMeta, log
from utils.colors import LBLUE, LGREEN, LYELLOW
from utils.database import get_prefix
from utils.numbers import format_numbers
from utils.others import get_cogs


class Bot(commands.Bot, metaclass=SingletonMeta):
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
    maintenance: bool = False
    start_date: datetime
    db_engine: AsyncEngine
    db_session: AsyncSession
    http_session: ClientSession
    configs = Configs()
    _status = cycle(('Androxus V3', '{users} Users!', '{servers} Guilds!'))
    _startup_timer: Stopwatch

    def __init__(self) -> None:
        self._startup_timer = Stopwatch()
        log('BOT', 'STARTING BOT...', first_color=LYELLOW)

        async def _prefix_or_mention(bot: 'Bot', message: Message):
            prefix = await get_prefix(bot, message)
            return commands.when_mentioned_or(prefix)(bot, message)

        kwargs: Dict[str, Any] = {}
        kwargs['command_prefix'] = _prefix_or_mention
        kwargs['owner_id'] = self.configs.owner_id
        kwargs['case_insensitive'] = True
        kwargs['intents'] = Intents.all()
        kwargs['strip_after_prefix'] = True
        kwargs['activity'] = Game(name='\N{SLEEPING FACE} Starting ...')
        kwargs['test_guilds'] = self.configs.test_guilds

        super().__init__(**kwargs)  # type: ignore

        # Loads all cogs of the bot.
        # bot.remove_command('help')
        for cog in get_cogs():
            self.load_extension(cog)

    @property
    def __version__(self) -> str:
        path = f'{abspath("./")}/pyproject.toml'
        with open(path, 'r', encoding='utf-8') as file:
            data: MutableMapping[str, Any] = load(file)
            return data['tool']['poetry']['version']

    async def on_ready(self) -> None:
        if (not hasattr(self,
                        'db_session')) or (not hasattr(self, 'db_engine')):
            self._startup_timer.stop()
            setattr(self, 'db_engine', ConnectionFactory.get_engine())
            setattr(
                self, 'db_session',
                ConnectionFactory.get_session(self.db_engine)
            )
            setattr(self, 'start_date', utcnow())
            await db_bootstrap(self.db_engine)
            log('BOT', f'LOGGED IN {self.user}', first_color=LGREEN)
            log('BOT', f'ID: {self.user.id}', first_color=LGREEN)
            log(
                'INFO',
                f'{len(set(self.get_all_members()))} USERS!',
                first_color=LBLUE
            )
            log('INFO', f'{len(self.guilds)} GUILDS!', first_color=LBLUE)
            log('INFO', f'BOT VERSION: {self.__version__}', first_color=LBLUE)
            log(
                'INFO',
                f'PYTHON VERSION: {python_version()}',
                first_color=LBLUE
            )
            log(
                'INFO',
                f'DISNAKE VERSION: {disnake_version}',
                first_color=LBLUE
            )
            log(
                'INFO',
                f'TIME TO START: {self._startup_timer}',
                first_color=LBLUE
            )
            try:
                # starts loop to change status
                self._change_status.start()
            except RuntimeError:
                pass

    @tasks.loop(minutes=1)
    async def _change_status(self) -> None:
        status_name = str(next(self._status)).format(
            servers=format_numbers(len(self.guilds)),
            users=format_numbers(len(self.users))
        )
        await self.change_presence(activity=Game(name=status_name))

    def get_languages(self) -> List[str]:
        languages: List[str] = []
        languages.append(self.configs.default_language)
        for language in listdir(abspath('./') + '/language/json/'):
            if language.endswith('.json'):
                languages.append(language.removesuffix('.json'))
        return languages
