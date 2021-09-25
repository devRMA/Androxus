from os import getenv

from discord import Permissions


class Config:
    """
    This class is used to store the configuration of the bot.

    Attributes:
        DEFAULT_PREFIX (str): The default prefix for the bot.
        REQUIRED_PERMISSIONS (discord.Permissions): The permissions necessary for all bot commands to work.

    """
    DEFAULT_PREFIX = getenv('DEFAULT_PREFIX', '!')
    REQUIRED_PERMISSIONS = Permissions(8)
