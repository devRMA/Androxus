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

from typing import TYPE_CHECKING, Any, TypeAlias

import i18n
from discord.ext import commands

if TYPE_CHECKING:
    from androxus import Bot
    TBot: TypeAlias = Bot
else:
    TBot: TypeAlias = None


class Context(commands.Context[TBot]):
    def translate(self, key: str, **kwargs: Any) -> str:
        """
        Get the translation for the given key.

        Parameters
        ----------
        key : `str`
            The key of the text to be translated.
        kwargs : dict[`str`, `Any`], optional
            The optional keyword arguments.

        Returns
        -------
        `str`
            The translated text.
        """
        locale = self.bot.configs.default_language
        if self.interaction is not None:
            locale = str(self.interaction.locale)
        elif self.guild is not None:
            locale = str(self.guild.preferred_locale)
        i18n.set('locale', locale)
        return i18n.t(key, **kwargs)

    __ = translate
