# coding=utf-8
# Androxus bot
# ConnectionFactory.py

__author__ = 'Rafael'

from os import environ

from psycopg2 import connect

from discord_bot.utils.Utils import get_configs


class ConnectionFactory:

    # método estatico, para que ele consiga ser acessado sem instanciar um objeto
    @staticmethod
    def get_connection():
        """
        :return: Uma conexão com o banco de dados
        :rtype: psycopg2.extensions.connection
        """
        # se o configs.json não for alterado, vai tentar pegar a variável do sistema
        configs = get_configs()
        if configs['connection_string'] == 'connection string of db':
            db_path = environ.get('DATABASE_URL')
        else:
            db_path = configs['connection_string']
        return connect(db_path)  # retorna a conexão
