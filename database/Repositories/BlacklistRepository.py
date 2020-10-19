# coding=utf-8
# Androxus bot
# BlacklistRepository.py

__author__ = 'Rafael'

from datetime import datetime

import psycopg2

from database.Conexao import Conexao
from database.Repositories.Interfaces.IBlacklistRepository import IBlacklistRepository


class BlacklistRepository(IBlacklistRepository):

    def create(self, conn: Conexao, pessoaId: int, motivo: str):
        """
        :param conn: Conexão com o banco de dados
        :param pessoaId: Id da pessoa que vai pra blacklist
        :param motivo: Motivo por estar colocando o user na blacklist
        :type conn: Conexao
        :type pessoaId: int
        :type motivo: str
        :return: Vai adicionar a pessoa na blacklist, se foi, vai retornar True
        :rtype: bool
        """
        cursor = conn.cursor()
        try:
            query = 'CALL blacklist_add( %s, %s, %s )'
            cursor.execute(query, (pessoaId, motivo, str(datetime.utcnow())))
            conn.salvar()
            return True  # vai retornar True se tudo ocorrer bem
        except psycopg2.IntegrityError as e:  # se esse item já existir
            if str(e).startswith('UNIQUE constraint failed'):
                raise Exception('blacklisted')
            else:
                raise e
        return False

    def get_pessoa(self, conn: Conexao, pessoaId: int):
        """
        :param conn: Conexão com o banco de dados
        :param pessoaId: Id da pessoa que vai saber se ela está ou não na blacklist
        :type conn: Conexao
        :type pessoaId: int
        :return: Vai ver se a pessoa está na blacklist
        :rtype: bool
        """
        cursor = conn.cursor()
        try:
            query = 'SELECT * FROM blacklist_get_pessoa ( %s );'
            cursor.execute(query, (pessoaId,))
            resps = cursor.fetchone()
            # vai fazer o select, se retorna algo, o id passado está na blacklist
            if resps:
                return [True, resps[1], datetime.strptime(resps[-1], '%Y-%m-%d %H:%M:%S.%f')]
            # se retornou None, é porque a pessoa não está na blacklist
            return [False, None, None]
        except Exception as e:
            return f'error: {str(e)}'

    def delete(self, conn: Conexao, pessoaId: int):
        """
        :param conn: Conexão com o banco de dados
        :param pessoaId: Id da pessoa que vai ser tirada do banco
        :type conn: Conexao
        :type pessoaId: int
        :return: Vai tirar um usuário da blacklist
        :rtype: bool
        """
        cursor = conn.cursor()
        try:
            query = 'CALL blacklist_remove( %s );;'
            cursor.execute(query, (pessoaId,))
            conn.salvar()
            return True
        except Exception as e:
            raise Exception(str(e))
        return False
