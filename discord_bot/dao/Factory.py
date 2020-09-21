# coding=utf-8
# Androxus bot
# Factory.py

__author__ = 'Rafael'

class Factory:
    def getConnection(self):
        from psycopg2 import connect
        from os import environ
        self.path_do_banco = environ.get('DATABASE_URL')
        return connect(self.path_do_banco)
