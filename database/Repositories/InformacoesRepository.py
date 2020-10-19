# coding=utf-8
# Androxus bot
# InformacoesRepository.py

__author__ = 'Rafael'

from database.Conexao import Conexao
from database.Repositories.Interfaces.IInformacoesRepository import IInformacoesRepository


class InformacoesRepository(IInformacoesRepository):

    def create(self, conn: Conexao, informacao: str, dado: str):
        """
        :param conn: Conexão com o banco de dados
        :param informacao: Informação que vai ser salva no banco
        :param dado: O dado referente a informação
        :type conn: Conexao
        :type informacao: str
        :type dado: dado
        :return: Se conseguir adicionar o comando ao banco, vai retornar True
        :rtype: bool
        """
        cursor = conn.cursor()
        try:
            query = 'CALL info_add(%s, %s);'  # query
            cursor.execute(query, (informacao, dado,))
            conn.salvar()
            return True  # vai retornar True se tudo ocorrer bem
        except:
            return False

    def get_dado(self, conn: Conexao, informacao: str):
        """
        :param conn: Conexão com o banco de dados
        :param informacao: Informação que vai querer pegar o dado
        :type conn: Conexao
        :type informacao: str
        :return: Vai retornar o dado referente a informação passada
        :rtype: str
        """
        cursor = conn.cursor()
        try:
            query = 'SELECT * FROM info_get(%s);'
            cursor.execute(query, (informacao,))
            resposta = cursor.fetchone()
            if resposta:
                return resposta[0]
            return resposta
        except Exception as e:
            return f'error: {str(e)}'

    def update(self, conn: Conexao, informacao: str, dado: str):
        """
        :param conn: Conexão com o banco de dados
        :param informacao: Informação que vai ser atualizada
        :param dado: O dado que também vai ser atualizado
        :type conn: Conexao
        :type informacao: str
        :type dado: dado
        :return: Se conseguir atualizar, vai retornar True
        :rtype: bool
        """
        cursor = conn.cursor()
        try:
            query = 'CALL info_update(%s, %s);'
            cursor.execute(query, (dado, informacao,))
            conn.salvar()
            return True
        except Exception as e:
            raise Exception(str(e))
        return False

    def delete(self, conn: Conexao, informacao: str):
        """
        :param conn: Conexão com o banco de dados
        :param informacao: Informação que vai ser deletada
        :type conn: Conexao
        :type informacao: str
        :return: None
        :rtype: None
        """
        cursor = conn.cursor()
        try:
            query = 'CALL info_remove(%s);'
            cursor.execute(query, (informacao,))
            conn.salvar()
            return True
        except Exception as e:
            raise Exception(str(e))
        return False

    def get_sql_version(self, conn: Conexao):
        """
        :param conn: Conexão com o banco de dados
        :type conn: Conexao
        :return: Vai retornar a versão do banco de dados
        :rtype: str
        """
        cursor = conn.cursor()
        try:
            query = 'SELECT version()'
            cursor.execute(query)
            resposta = cursor.fetchone()
            return resposta[0]
        except Exception as e:
            return f'error: {str(e)}'
