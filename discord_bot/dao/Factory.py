# coding=utf-8
# Androxus bot
# Factory.py

__author__ = 'Rafael'

from psycopg2 import connect
from os import environ
from discord_bot.utils.Utils import get_configs


class Factory:

    def getConnection(self):
        if get_configs()['connection_string'] == 'connection string of db':
            self.db_path = environ.get('DATABASE_URL')
        else:
            self.db_path = get_configs()['connection_string']
        return connect(self.db_path)
