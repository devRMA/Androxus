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

from json import load
from os.path import abspath
from typing import Optional, Union

from androxus import Bot
from database.repositories.guild_repository import GuildRepository
from disnake import ApplicationCommandInteraction as Interaction
from disnake import Guild
from disnake.ext.commands.context import Context


class Translator:
    """
    The class responsible for translations.

    Args:
        context (Context or ApplicationCommandInteraction): The context of
        the command.

    """
    bot: Bot
    guild: Optional[Guild]
    language: str
    texts: dict

    def __init__(self, context: Union[Context, Interaction]):
        self.bot = context.bot
        self.guild = context.guild

    async def init(self):
        """
        Initializes the translator.

        Returns:
            self

        """
        if self.guild is None:
            self.language = self.bot.configs.language
        else:
            repository = GuildRepository(self.bot.db_session)
            db_guild = await repository.find_or_create(self.guild.id)
            self.language = db_guild.language
        path_to_json = abspath('./') + f'/language/json/{self.language}.json'
        with open(path_to_json) as file:
            self.texts = load(file)
        return self

    def translate(self, text: str, placeholders: dict = {}) -> str:
        """
        Translates the text.

        Args:
            text (str): The text to be translated.
            placeholders (dict): The words that will be replaced.

        Returns:
            str: The translated text.

        """
        translated_text = self.texts.get(text, text)
        for key, value in placeholders.items():
            translated_text = translated_text.replace(f':{key}', value)
        return translated_text

    """
    ------------------------------------------------------------
                            Aliases
    ------------------------------------------------------------
    """

    def get(self, text: str, placeholders: dict = {}) -> str:
        """
        Translates the text.

        Args:
            text (str): The text to be translated.
            placeholders (dict): The words that will be replaced.

        Returns:
            str: The translated text.

        """
        return self.translate(text, placeholders)
