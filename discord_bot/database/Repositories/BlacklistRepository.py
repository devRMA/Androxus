# coding=utf-8
# Androxus bot
# BlacklistRepository.py

__author__ = 'Rafael'

import psycopg2

from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.Interfaces.IBlacklistRepository import IBlacklistRepository


class BlacklistRepository(IBlacklistRepository):

    def create(self, conn: Conexao, pessoaId: int):
        """
        :param conn: Conexão com o banco de dados
        :param pessoaId: Id da pessoa que vai pra blacklist
        :type conn: Conexao
        :type pessoaId: int
        :return: Vai adicionar a pessoa na blacklist, se foi, vai retornar True
        :rtype: bool
        """
        cursor = conn.cursor()
        try:
            query = 'CALL blacklist_add( %s )'
            cursor.execute(query, (pessoaId,))
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
            # vai fazer o select, se retorna algo, o id passado está na blacklist
            if cursor.fetchone():
                return True
            # se retornou None, é porque a pessoa não está na blacklist
            return False
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
