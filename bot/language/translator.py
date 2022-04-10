# The MIT License (MIT)

# Copyright (c) Taylor Otwell

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Credits to Taylor Otwell. Original PHP code, translated to Python by me
# https://github.com/laravel/framework/blob/8e2d72728d6911816a97843ec3341e28c92af120/src/Illuminate/Translation/Translator.php

from __future__ import annotations

from collections.abc import Sized
from json import load
from os.path import abspath, exists
from typing import Any, Optional

from disnake import CmdInter, Guild
from disnake.ext.commands import Context  # type: ignore

from androxus import Bot
from configs import Configs
from database.repositories.guild_repository import GuildRepository

from .message_selector import MessageSelector


class Translator:
    """
    The class responsible for translations.

    Parameters
    -------
    context : `disnake.ext.commands.Context` or `disnake.CmdInter`, optional
        The context of the command.
    """
    bot: Optional[Bot] = None
    guild: Optional[Guild] = None
    language: str = Configs.language
    texts = dict[str, Any]()
    _selector: MessageSelector

    def __init__(self, context: Optional[Context[Bot] | CmdInter]) -> None:
        # if context is None, will be used the default language
        if context is None:
            self.language = Configs.language
            self._load_texts()
        else:
            self.bot = context.bot  # type: ignore
            self.guild = context.guild

    async def init(self) -> Translator:
        """|coro|

        Initializes the translator.

        Returns
        -------
        `Translator`
            The translator instance.
        """
        if self.bot is not None:
            if self.guild is None:
                self.language = self.bot.configs.language
            else:
                repository = GuildRepository(self.bot.db_session)
                db_guild = await repository.find_or_create(self.guild.id)
                self.language = db_guild.language  # type: ignore
            self._load_texts()
        return self

    def has(self, key: str) -> bool:
        """
        Determine if a translation exists.

        Parameters
        ----------
        key : `str`
            The key of the text to be translated.

        Returns
        -------
        `bool`
            True if the translation exists, False otherwise.
        """
        return self.get(key) != key

    def has_locale(self, locale: str) -> bool:
        """
        Determine if exists a json file for the given locale.

        Parameters
        ----------
        locale : `str`
            The locale to be checked.

        Returns
        -------
        `bool`
            True if the locale exists, False otherwise.
        """
        return exists(self._get_json_path(locale))

    def get(self, key: str, placeholders: dict[str, Any] = {}) -> str:
        """
        Get the translation for the given key.

        Parameters
        ----------
        key : `str`
            The key of the text to be translated.
        placeholders : dict[`str`, `Any`], optional
            The words that will be replaced, by default {}

        Returns
        -------
        `str`
            The translated text.
        """
        return self._make_replacements(self.texts.get(key, key), placeholders)

    def choice(
        self,
        key: str,
        number: int | Sized,
        placeholders: dict[str, Any] = {}
    ) -> str:
        """
        Get a translation according to an integer value.

        Parameters
        ----------
        key : `str`
            The key of the text to be translated.
        number : `int`
            The amount of items, to get the text according to the correct
            plural or the iterable of items.
        placeholders : dict[`str`, `Any`], optional
            The words that will be replaced, by default {}

        Returns
        -------
        `str`
            The translated text, with the plural or singular, correct.
        """
        placeholders = placeholders or {}
        line = self.get(key, placeholders)

        number = len(number) if isinstance(number, Sized) else int(number)

        placeholders['count'] = number
        return self._make_replacements(
            self._get_selector().choose(line, number, self.language),
            placeholders
        )

    def _load_texts(self) -> None:
        """
        Loads the texts from the language file.
        """
        if self.has_locale(self.language):
            with open(
                self._get_json_path(self.language), encoding='utf-8'
            ) as file:
                self.texts = load(file)

    def _get_selector(self) -> MessageSelector:
        """
        Get the selector of the language.
        """
        if self._selector is None:
            self._selector = MessageSelector()
        return self._selector

    @staticmethod
    def _get_json_path(locale: str) -> str:
        """
        Get the path to the json file for the given locale.
        """
        return f'{abspath("./")}/language/json/{locale}.json'

    @staticmethod
    def _make_replacements(line: str, placeholders: dict[str, Any]) -> str:
        """
        Replaces the placeholders in the line.
        """
        should_replace = dict[str, Any]()
        for key, value in placeholders.items():
            should_replace[':' +
                           str(key).capitalize()] = str(value).capitalize()
            should_replace[':' + str(key).upper()] = str(value).upper()
            should_replace[':' + key] = value
        for key, value in should_replace.items():
            line = line.replace(str(key), str(value))
        return line

    # ------------------------------------------------------------
    #                         Aliases
    # ------------------------------------------------------------

    translate = get
    __ = get
