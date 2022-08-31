import logging
from logging.handlers import RotatingFileHandler
from os.path import abspath
from pathlib import Path

# Example taken from discord.py docs
# https://discordpy.readthedocs.io/en/v2.0.1/logging.html


def setup_logging() -> None:

    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    logging.getLogger('discord.http').setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename=abspath('./') + '/logs/androxus.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB,
        backupCount=5,  # Rotate through 5 files
    )

    dt_format = r'%Y-%m-%d %H:%M:%S'
    log_format = '[{asctime}] [{levelname:<8}] {name}: {message}'

    formatter = logging.Formatter(log_format, dt_format, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
