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

from traceback import format_exception

from disnake import Colour, Embed, Message
from disnake.utils import utcnow
from stopwatch import Stopwatch
from utils import get_cogs

from .base import Base


class DevCommands(Base):
    async def reload(self) -> Message:
        """
        Reloads all cogs
        """
        message = ''
        successfully_icon = '\N{WHITE HEAVY CHECK MARK}'
        unsuccessfully_icon = '\N{WARNING SIGN}'
        for cog in get_cogs():
            cog_name = str(cog).removeprefix('commands.')
            cog_stopwatch = Stopwatch()
            try:
                self.bot.reload_extension(cog)
            except Exception as exc:
                cog_stopwatch.stop()
                traceback_data = ''.join(format_exception(
                    type(exc),
                    exc,
                    exc.__traceback__,
                    1
                ))
                message += f'{unsuccessfully_icon} `{cog_name}`\n' \
                    f'```py\n{traceback_data}\n```\n'
            else:
                cog_stopwatch.stop()
                message += f'{successfully_icon} `{cog_name} - {cog_stopwatch}`\n'
        return await self.send(embed=Embed(
            title=self.__('Reloaded all cogs'),
            description=message,
            timestamp=utcnow(),
            color=Colour.random()
        ).set_footer(
            text=str(self.author),
            icon_url=self.author.display_avatar.url
        ))
