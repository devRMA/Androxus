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

from typing import Any, Callable, Dict, List, Optional

from database.models import Guild
from database.repositories import RepositoryFactory
from database.repositories.guild_repository import GuildRepository
from disnake import (
    ButtonStyle, Colour, Embed, Member, Message, MessageInteraction, User
)
from disnake.ui import Button, Item, View, button
from disnake.utils import utcnow
from enums import RepositoryType

from .base import Base


class ConfigsCommands(Base):
    async def language(self) -> Optional[Message]:
        """
        Changes the language of the bot, for the current guild
        """
        if self.guild is None:
            return None

        def get_embed(guild: Guild) -> Embed:
            return Embed(
                title=self.__('Select the language I will use:'),
                description=self.__(
                    'Current language: **:language**',
                    {'language': guild.language}
                ),
                timestamp=utcnow(),
                color=Colour.random()
            ).set_footer(
                text=str(self.author), icon_url=self.author.display_avatar.url
            )

        class LanguageView(View):
            children: List[Item[View]]

            def __init__(
                self, *, author: Member | User,
                __: Callable[[str, Optional[Dict[str, Any]]], str],
                guild_repository: GuildRepository, guild: Guild
            ):
                self.author = author
                self.__ = __
                self.guild_repository = guild_repository
                self.guild = guild

                super().__init__(timeout=60.0)

            async def interaction_check(
                self, interaction: MessageInteraction
            ) -> bool:
                # will be check if the user can interact with message
                can_use = self.author.id == interaction.author.id
                if not can_use:
                    message = self.__(
                        'You can\'t interact with this message', {}
                    )
                    await interaction.send(
                        content=message, ephemeral=True
                    )
                return can_use

            def _select_button(self, button: Button[View]) -> None:
                for child in self.children:
                    if isinstance(
                        child, Button
                    ) and child.style != ButtonStyle.grey:
                        child.style = ButtonStyle.grey
                        child.disabled = False
                button.style = ButtonStyle.blurple
                button.disabled = True

            async def _change_language(self, new_language: str) -> None:
                self.guild.language = new_language
                await self.guild_repository.update(self.guild)

            async def _on_button_click(
                self, button: Button[View], interaction: MessageInteraction,
                new_language: str
            ) -> None:
                self._select_button(button)
                await self._change_language(new_language)
                await interaction.response.edit_message(
                    content=self.__(
                        ':userMention Language changed to **:language**', {
                            'language': self.guild.language,
                            'userMention': interaction.author.mention
                        }
                    ),
                    view=self,
                    embed=get_embed(self.guild)
                )

            @button(
                style=ButtonStyle.gray,
                emoji='\U0001f1e7\U0001f1f7',
                label="Português"
            )
            async def portuguese(
                self, button: Button[View], interaction: MessageInteraction
            ):
                await self._on_button_click(button, interaction, 'pt_BR')

            @button(
                style=ButtonStyle.blurple,
                emoji='\U0001f1fa\U0001f1f8',
                label="English",
                disabled=True
            )
            async def english(
                self, button: Button[View], interaction: MessageInteraction
            ):
                await self._on_button_click(button, interaction, 'en_US')

        repo = RepositoryFactory.create(RepositoryType.GUILD)
        guild_db = await repo.find_or_create(self.guild.id)
        view = LanguageView(
            author=self.author,
            __=self.__,
            guild_repository=repo,
            guild=guild_db
        )
        for child in view.children:
            if isinstance(child, Button):
                if child.label == 'Português' and guild_db.language == 'pt_BR':
                    child.style = ButtonStyle.blurple
                    child.disabled = True
                elif child.label == 'English' and guild_db.language == 'en_US':
                    child.style = ButtonStyle.blurple
                    child.disabled = True
                else:
                    child.style = ButtonStyle.gray
                    child.disabled = False
        return await self.ctx.send(
            view=view,
            embed=get_embed(guild_db)
        )
