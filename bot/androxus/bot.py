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

from database import bootstrap as db_bootstrap
from disnake.ext import commands
from sqlalchemy.ext.asyncio import create_async_engine


class Bot(commands.Bot):

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
