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

from .colors import CYAN, LBLUE, BRIGHT, RESET
from logging import getLogger


def log(tag: str, text: str, level: str = 'info', *,
        first_color: str = CYAN, second_color: str = LBLUE):
    print(f'{BRIGHT}{first_color}[{tag:^16}]' +
          f'{second_color}{text}{RESET}'.rjust(60))
    logger = getLogger('androxus')
    match level:
        case 'info':
            logger.info(text)
        case 'warning':
            logger.warning(text)
        case 'error':
            logger.error(text)
        case 'critical':
            logger.critical(text)
        case _:
            logger.debug(text)
