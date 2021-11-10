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

from random import randint

from disnake import Embed, Message
from disnake.utils import utcnow

from .base import Base


class InfoCommands(Base):
    async def ping(self) -> Message:
        embed = Embed(
            title=self.__('Translation test'),
            description=self.__('Latency'),
            timestamp=utcnow()
        )

        minutes = randint(2, 50)
        await self.send(f'{self._choice("{1} Há um minuto.|[2,*] Há :value minutos!", 1, {"value": 1})}\n'
                        f'{self._choice("{1} Há um minuto.|[2,*] Há :value minutos!", minutes, {"value": minutes})}\n')
