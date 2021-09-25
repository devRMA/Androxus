from os import getenv


class Config:
    DEFAULT_PREFIX = getenv('DEFAULT_PREFIX', '!')
