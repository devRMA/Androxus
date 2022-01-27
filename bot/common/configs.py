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

from typing import Callable, List, Union

from database.repositories import RepositoryFactory
from disnake import (
    Colour, Embed, Member, Message, MessageInteraction, SelectOption, User
)
from disnake.ui import Select, View
from disnake.utils import utcnow
from enums import RepositoryType

from .base import Base


class ConfigsCommands(Base):
    async def language(self) -> Message:
        """
        Changes the language of the bot, for the current guild
        """
        repo = RepositoryFactory.create(RepositoryType.GUILD)
        guild_db = await repo.find_by_id(self.guild.id)

        class LanguageSelect(Select):
            def __init__(self, *, languages: List[str], __: Callable):
                self.__ = __

                options = [
                    SelectOption(
                        label=language,
                        value=language,
                        default=language == guild_db.language
                    ) for language in languages
                ]

                super().__init__(
                    placeholder=self.__("Languages:"),
                    min_values=1,
                    max_values=1,
                    options=options,
                )

            async def callback(self, inter: MessageInteraction):
                guild_db.language = self.values[0]
                await repo.save(guild_db)

                message = self.__(
                    ':userMention Language changed to **:language**', {
                        'language': self.values[0],
                        'userMention': inter.user.mention
                    }
                )
                await inter.response.send_message(content=message)

        class LanguageView(View):
            def __init__(
                self, *, author: Union[Member, User], languages: List[str],
                __: Callable
            ):
                self.author = author
                self.__ = __

                super().__init__(timeout=60.0)

                self.add_item(LanguageSelect(languages=languages, __=self.__))

            async def interaction_check(
                self, inter: MessageInteraction
            ) -> bool:
                # will be check if the user can interact with message
                can_use = self.author.id == inter.user.id
                if not can_use:
                    message = self.__('You can\'t interact with this message')
                    await inter.response.send_message(
                        content=message, ephemeral=True
                    )
                return can_use

        # creating the view and sending the message
        view = LanguageView(
            author=self.author, languages=self.bot.get_languages(), __=self.__
        )
        return await self.send(
            view=view,
            embed=Embed(
                title=self.__('Select the language I will use:'),
                description=self.__(
                    'Current language: **:language**',
                    {'language': guild_db.language}
                ),
                timestamp=utcnow(),
                color=Colour.random()
            ).set_footer(
                text=str(self.author), icon_url=self.author.display_avatar.url
            )
        )
