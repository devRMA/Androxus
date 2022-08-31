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

from __future__ import annotations

from datetime import datetime
from itertools import cycle
from os import listdir
from os.path import abspath
from platform import python_version
from typing import TYPE_CHECKING, Any, ClassVar, MutableMapping, TypeAlias

from aiohttp.client import ClientSession
from discord import Game, Message, Object
from discord import __version__ as discord_version
from discord.ext import commands, tasks
from discord.utils import utcnow
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from stopwatch import Stopwatch
from toml import load

from configs import Configs
from database import bootstrap as db_bootstrap
from database.connection import ConnectionFactory
from language.translator import Translator
from utils import SingletonMeta, log
from utils.colors import LBLUE, LGREEN, LYELLOW
from utils.database import get_prefix
from utils.numbers import format_numbers
from utils.others import get_cogs

if TYPE_CHECKING:
    TSession: TypeAlias = sessionmaker[AsyncSession]
else:
    TSession: TypeAlias = AsyncSession


class Bot(commands.Bot, metaclass=SingletonMeta):
    """
    The main class of the bot.

    Attributes:
        __version__ (str): The current version of the bot.
        configs (Configs): The configs of the bot.
        db_engine: Engine used to connect to the database.
        db_session: The session connected to the database.
        http_session (ClientSession): The aiohttp session.
        maintenance (bool): Whether the bot is in maintenance mode.
        started_at(datetime): When the bot was started.

    """
    _startup_timer: Stopwatch
    _status = cycle(('Androxus V3', '{users} Users!', '{servers} Guilds!'))
    configs: ClassVar[Configs] = Configs()
    db_engine: AsyncEngine
    db_session: TSession
    http_session: ClientSession
    maintenance: ClassVar[bool] = False
    started_at: datetime

    def __init__(self) -> None:
        self._startup_timer = Stopwatch()
        log('BOT', 'STARTING BOT...', first_color=LYELLOW)

        async def _prefix_or_mention(bot: Bot, message: Message) -> list[str]:
            prefix = await get_prefix(bot, message)
            return commands.when_mentioned_or(prefix)(bot, message)

        super().__init__(
            command_prefix=_prefix_or_mention,
            owner_id=self.configs.owner_id,
            case_insensitive=True,
            intents=self.configs.intents,
            strip_after_prefix=True,
            activity=Game(name='\N{SLEEPING FACE} Starting ...'),
        )

    @property
    def __version__(self) -> str:
        """`str`: The current version of the bot."""
        path = f'{abspath("./")}/pyproject.toml'
        with open(path, 'r', encoding='utf-8') as file:
            data: MutableMapping[str, Any] = load(file)
            tool = data.get('tool', dict[str, Any]())
            poetry = tool.get('poetry', dict[str, Any]())
            return str(poetry.get('version', ''))

    async def setup_hook(self) -> None:
        """|coro|

        The event that will fire when the bot is ready, but before connecting
        to the Websocket.
        """
        self._startup_timer.stop()
        self.started_at = utcnow()
        self.db_engine = ConnectionFactory.get_engine()
        self.db_session = ConnectionFactory.get_session(self.db_engine)

        await db_bootstrap(self.db_engine)
        await self.tree.set_translator(Translator())

        # Loads all cogs of the bot.
        # bot.remove_command('help')
        for cog in get_cogs():
            await self.load_extension(cog)

        if len(self.configs.test_guilds) > 0:
            for testing_guild_id in self.configs.test_guilds:
                guild = Object(testing_guild_id)
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)

        try:
            self._change_status.start()
        except RuntimeError:
            pass

    async def on_ready(self) -> None:
        if self.user is not None:
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
                f'DISCORD.PY VERSION: {discord_version}',
                first_color=LBLUE
            )
            log(
                'INFO',
                f'TIME TO START: {self._startup_timer}',
                first_color=LBLUE
            )

    async def on_message(self, message: Message) -> None:
        """|coro|

        The event triggered when a message is received.
        """
        if (not hasattr(self,
                        'db_session')) or (not hasattr(self, 'db_engine')):
            return None
        await self.process_commands(message)

    @tasks.loop(minutes=1)
    async def _change_status(self) -> None:
        status_name = str(next(self._status)).format(
            servers=format_numbers(len(self.guilds)),
            users=format_numbers(len(self.users))
        )
        await self.change_presence(activity=Game(name=status_name))

    def get_languages(self) -> list[str]:
        """
        Returns a list of languages supported by the bot.

        Returns
        -------
            list[`str`]
                The list of languages supported by the bot.
        """
        languages = list[str]()
        languages.append(self.configs.default_language)
        for language in listdir(abspath('./') + '/language/json/'):
            if language.endswith('.json'):
                languages.append(language.removesuffix('.json'))
        return languages
