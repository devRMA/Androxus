# -*- coding: utf-8 -*-
# Androxus bot
# ConnectionFactory.py

__author__ = 'Rafael'

import ssl
from os import environ

from asyncpg import create_pool
from asyncpg.exceptions import InvalidAuthorizationSpecificationError

from utils.Utils import get_configs, get_path_from_file


class ConnectionFactory:

    # método estatico, para que ele consiga ser acessado sem instanciar um objeto
    @staticmethod
    async def get_connection(connection_string=None):
        """

        Args:
            connection_string (str or dict): A string de conexão, caso não seja passado, vai tentar achar

        Returns:
            asyncpg.pool.Pool: Uma conexão com o banco de dados

        """
        # se o configs.json não for alterado, vai tentar pegar o que tiver no .env
        configs = get_configs()
        conn = None
        if connection_string is None:
            # vai pegar a string de conexão do "configs.json" se ele
            # foi alterado, senão, vai tentar pegar a string de conexão do environ
            connection_string = environ.get('DATABASE_URL') if configs['connection_string'] == \
                                                               'connection string of db' else configs[
                'connection_string']
        try:
            # tenta abrir a conexão com o banco sem ssl
            conn = await create_pool(**connection_string) if isinstance(connection_string, dict) else await create_pool(
                connection_string)
        except InvalidAuthorizationSpecificationError:
            # se der erro, tenta passar o ssl com o certificado que está na pasta database/Factories/certificate/
            cert_path = get_path_from_file('*.pem', 'database/Factories/certificate/')
            if cert_path is not None:
                # se tiver certificado
                ssl_cert = ssl.create_default_context(cafile=cert_path)
                ssl_cert.check_hostname = False
                ssl_cert.verify_mode = ssl.CERT_NONE
                # vai tentar se conectar com o certificado
                conn = await create_pool(**connection_string, ssl=ssl_cert) if isinstance(connection_string,
                                                                                          dict) else await create_pool(
                    connection_string, ssl=ssl_cert)
            else:
                exit('Certificado não foi encontrado! Baixe em '
                     'https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem\n'
                     'E deixe na pasta database/Factories/certificate !')

        return conn
