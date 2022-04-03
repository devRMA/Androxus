# MIT License

# Copyright (c) 2021 Caio Alexandre
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
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

import logging
from logging.handlers import RotatingFileHandler
from os.path import abspath
from pathlib import Path

# credits to Caio Alexandre
# https://github.com/webkaiyo/eris/blob/59f2fce4f40bf953065fa357d18a9065d26653a3/bot/launcher.py#L60


class RemoveNoise(logging.Filter):
    def __init__(self) -> None:
        super().__init__(name='discord.state')

    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelname == 'WARNING' and 'referencing an unknown' in record.msg:
            return False
        return True


def setup_logging() -> None:
    # creating the "logs" folder if it doesn't exist
    path = Path(abspath('./') + '/logs')
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    max_bytes = 32 * 1024 * 1024  # 32 MiB

    logging.getLogger('discord').setLevel(logging.INFO)
    logging.getLogger('discord.http').setLevel(logging.WARN)
    logging.getLogger('discord.state').addFilter(RemoveNoise())

    logger = logging.getLogger('androxus')
    logger.setLevel(logging.INFO)

    dt_format = r'%Y-%m-%d %H:%M:%S'
    log_format = '[{asctime}] [{levelname}] {name}: {message}'

    handler = RotatingFileHandler(
        filename=abspath('./') + '/logs/androxus.log',
        encoding='utf-8',
        mode='w',
        maxBytes=max_bytes,
        backupCount=5
    )
    formatter = logging.Formatter(log_format, dt_format, style='{')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
