# # MIT License

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

from asyncio import sleep
from typing import Optional

from database.repositories import RepositoryFactory
from disnake import CmdInter, Colour, Embed, Member, Message, User
from disnake.utils import format_dt, utcnow
from enums import RepositoryType
from stopwatch import Stopwatch

from .base import Base


class InfoCommands(Base):
    async def ping(self) -> Optional[Message]:
        """
        Get the bot latency
        """
        # getting latency with the database
        guild_repo = RepositoryFactory.create(RepositoryType.GUILD)
        stopwatch_db = Stopwatch()
        await guild_repo.find(0)
        stopwatch_db.stop()

        # getting the latency to send a message
        stopwatch_message = Stopwatch()
        bot_message = await self.ctx.send(  # type: ignore
            embed=Embed(
                title=self.__('Calculating latency...') +
                f' {self.bot.get_emoji(756715436149702806)}',
                timestamp=utcnow(),
                color=Colour.random()
            ).set_footer(
                text=str(self.author), icon_url=self.author.display_avatar.url
            )
        )
        stopwatch_message.stop()

        if isinstance(self.ctx, CmdInter):
            bot_message = await self.ctx.original_message()

        embed_title = '\N{TABLE TENNIS PADDLE AND BALL} ' + \
            self.__('API latency:') + \
            f' {int(self.bot.latency * 1000)}ms!\n' + \
            f'{self.bot.get_emoji(756712226303508530)} ' + \
            self.__('Database response time:') + \
            f' {stopwatch_db}!\n' + \
            '\N{INCOMING ENVELOPE} ' + \
            self.__('Discord response time:') + \
            f' {stopwatch_message}'
        await sleep(stopwatch_message.duration * 2)
        return await bot_message.edit(  # type: ignore
            embed=Embed(
                title=embed_title, timestamp=utcnow(), color=Colour.random()
            ).set_footer(
                text=str(self.author), icon_url=self.author.display_avatar.url
            )
        )

    async def uptime(self) -> Optional[Message]:
        """
        Get the bot uptime
        """
        return await self.ctx.send(  # type: ignore
            embed=Embed(
                title='\N{TIMER CLOCK} ' + self.__('When I started:'),
                description=format_dt(self.bot.start_date, 'R'),
                timestamp=utcnow(),
                color=Colour.random()
            ).set_footer(
                text=str(self.author), icon_url=self.author.display_avatar.url
            )
        )

    async def avatar(self, user: Member | User) -> Optional[Message]:
        """
        Get the user avatar
        """
        embed_description = '\N{WHITE RIGHT POINTING BACKHAND INDEX} ' + \
            self.__('Click [here](:link) to see the avatar', {
                'link': user.display_avatar.url
            })
        return await self.ctx.send(  # type: ignore
            embed=Embed(
                title='\N{EYE} ' +
                self.__('Avatar of :username', {'username': user.display_name}),
                description=embed_description,
                timestamp=utcnow(),
                color=Colour.random()
            ).set_footer(
                text=str(self.author), icon_url=self.author.display_avatar.url
            ).set_image(user.display_avatar.url)
        )
