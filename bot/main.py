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

from os import getenv

from colorama import init
from disnake.ext import commands
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database.tests import make_tests
from bootstrap import init

from database import bootstrap as db_bootstrap
from database.repositories.guild_repository import GuildRepository

from asyncio import new_event_loop


async def main():
    init()
    if getenv('DO_TESTS') == 'true':
        await make_tests()

if __name__ == '__main__':
    loop = new_event_loop()
    loop.run_until_complete(main())

# init()
# load_dotenv()
# bot = commands.Bot(command_prefix='!!')


# @bot.event
# async def on_ready():
#     user = getenv('DB_USER')
#     pw = getenv('DB_PASS')
#     host = getenv('DB_HOST')
#     port = getenv('DB_PORT')
#     db_name = getenv('DB_NAME')
#     dsn = f'postgresql+asyncpg://{user}:{pw}@{host}:{port}/{db_name}'
#     engine = create_async_engine(
#         dsn
#     )
#     await db_bootstrap(engine)
#     async_session = sessionmaker(
#         engine,
#         autocommit=False,
#         expire_on_commit=False,
#         class_=AsyncSession
#     )
#     repository = GuildRepository(async_session)
#     guild = await repository.create(1)
#     if guild is None:
#         print('Guild already exists')
#     else:
#         print(f'guild.id: {guild.id}')
#         await repository.delete(guild)
#     print('Logged in as')
#     print(bot.user.name)
#     print(bot.user.id)
#     print('------')


# bot.run(getenv('TOKEN'))
