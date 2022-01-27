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

from typing import Any, Coroutine, Dict, Iterable, Optional, Union

from androxus import Bot
from disnake import ApplicationCommandInteraction as Interaction
from disnake import Guild, Member, Message, User
from disnake.ext.commands.bot_base import BotBase  # type: ignore
from disnake.ext.commands.context import Context  # type: ignore
from language import Translator


class Base:
    """
    The base class, for commands.

    Args:
        context (Context or ApplicationCommandInteraction): The context of
        the command.

    Attributes:
        bot (Bot): The bot instance.
        ctx (Context or ApplicationCommandInteraction): The context of the
            command.
        author (Member or User): The author of the command.
        guild (Guild or None): The guild in which the command was used.
        translator (Translator): The translator instance.
        send (Coroutine): The coroutine to send messages.
        is_interaction (bool): If the context is an interaction.

    """
    bot: BotBase
    ctx: Union[Context[Bot], Interaction]
    author: Union[Member, User]
    guild: Optional[Guild]
    translator: Translator
    send: Coroutine[Any, Any, Message]
    is_interaction: bool

    def __init__(self, context: Context[Bot] | Interaction) -> None:
        self.bot = context.bot
        self.ctx = context
        self.author = context.author
        self.guild = context.guild
        if isinstance(context, Context):
            self.send = context.send  # type: ignore
            self.is_interaction = False
        else:
            self.send = context.response.send_message  # type: ignore
            self.is_interaction = True

    async def init(self) -> 'Base':
        """
        Initialize the class.

        Returns:
            Base: The self instance.

        """
        self.translator = await Translator(self.ctx).init()
        return self

    def __(self, key: str, placeholders: Dict[str, Any] = {}) -> str:
        """
        Get the translation for the given key.

        Args:
            key (str): The key of the text to be translated.
            placeholders (dict): The words that will be replaced.

        Returns:
            str: The translated text.

        """
        return self.translator.get(key, placeholders)

    def _choice(self, key: str, number: int | Iterable[Any],
                placeholders: Dict[str, Any] = {}) -> str:
        """
        Get a translation according to an integer value.

        Args:
            key (str): The key of the text to be translated.
            number (int or Iterable): The amount of items, to get the text
            according to the correct plural or the iterable of items.
            placeholders (dict): The words that will be replaced.

        Returns:
            str: The translated text, with the plural or singular, correct.

        """
        return self.translator.choice(key, number, placeholders)
