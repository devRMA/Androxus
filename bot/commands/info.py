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

from asyncio import sleep

from discord import Colour, Embed
from discord.app_commands import locale_str as _
from discord.ext import commands
from discord.utils import utcnow
from stopwatch import Stopwatch

from androxus import Bot, Context
from database.repositories import RepositoryFactory
from enums import RepositoryType


class InfoCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(name=_('ping'))
    async def ping(self, ctx: Context) -> None:
        # getting latency with the database
        guild_repo = RepositoryFactory.create(RepositoryType.GUILD)
        with Stopwatch() as stopwatch_db:
            await guild_repo.find(0)

        # getting the latency to send a message
        with Stopwatch() as stopwatch_message:
            bot_message = await ctx.send(
                embed=Embed(
                    title=ctx.__('latency-calculating') +
                    f' {self.bot.get_emoji(756715436149702806)}',
                    timestamp=utcnow(),
                    color=Colour.random()
                ).set_footer(
                    text=str(ctx.author),
                    icon_url=ctx.author.display_avatar.url
                )
            )

        embed_title = '\N{TABLE TENNIS PADDLE AND BALL} ' + \
            ctx.__('latency-api') + \
            f' {int(self.bot.latency * 1000)}ms!\n' + \
            f'{self.bot.get_emoji(756712226303508530)} ' + \
            ctx.__('latency-database') + \
            f' {stopwatch_db}!\n' + \
            '\N{INCOMING ENVELOPE} ' + \
            ctx.__('latency-discord') + \
            f' {stopwatch_message}'

        await sleep(stopwatch_message.elapsed * 2)

        await bot_message.edit(
            embed=Embed(
                title=embed_title, timestamp=utcnow(), color=Colour.random()
            ).set_footer(
                text=str(ctx.author), icon_url=ctx.author.display_avatar.url
            )
        )


async def setup(bot: Bot) -> None:
    await bot.add_cog(InfoCommands(bot))
