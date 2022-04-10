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

from typing import Any, Optional, Sized

from discord import Client, Guild, Interaction, Member, User
from discord.ext.commands import Context

from androxus import Bot
from language import Translator


class Base:
    """
    The base class, for commands.

    Parameters
    -------
        context : `discord.ext.commands.Context` or `discord.Interaction`
            The context of the command.

    Attributes
    -------
        bot : `Client`
            The bot instance.
        ctx : `discord.ext.commands.Context` or `discord.Interaction`
            The context of the command.
        author : `discord.Member` or `discord.User`
            The author of the command.
        guild : `Guild`, optional
            The guild in which the command was used.
        translator : `Translator`
            The translator instance.
        is_interaction : `bool`
            If the context is an interaction.

    """
    bot: Client
    ctx: Context[Bot] | Interaction
    author: Member | User
    guild: Optional[Guild]
    translator: Translator
    is_interaction: bool

    def __init__(self, context: Context[Bot] | Interaction) -> None:
        self.bot = context.bot if isinstance(
            context, Context
        ) else context.client
        self.ctx = context
        self.author = context.author if isinstance(
            context, Context
        ) else context.user
        self.guild = context.guild
        self.is_interaction = isinstance(context, Interaction)

    async def init(self) -> Base:
        """
        Initialize the class.

        Returns
        -------
            `Base`
                The self instance.

        """
        self.translator = await Translator(self.ctx).init()
        return self

    def __(self, key: str, placeholders: dict[str, Any] = {}) -> str:
        """
        Get the translation for the given key.

        Parameters
        -------
            key : `str`
                The key of the text to be translated.
            placeholders : dict[`str`, `Any`], optional
                The words that will be replaced.

        Returns
        -------
            str: The translated text.

        """
        return self.translator.get(key, placeholders)

    def _choice(
        self,
        key: str,
        number: int | Sized,
        placeholders: dict[str, Any] = {}
    ) -> str:
        """
        Get a translation according to an integer value.

        Parameters
        -------
            key : `str`
                The key of the text to be translated.
            number : `int` or `Sized`
                The amount of items, to get the text according to the correct
                plural or the iterable of items.
            placeholders : dict[`str`, `Any`], optional
                The words that will be replaced.

        Returns
        -------
            str: The translated text, with the plural or singular, correct.

        """
        return self.translator.choice(key, number, placeholders)
