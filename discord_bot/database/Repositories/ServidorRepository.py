# coding=utf-8
# Androxus bot
# ServidorRepository.py

__author__ = 'Rafael'

import psycopg2

from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.Interfaces.IServidorRepository import IServidorRepository
from discord_bot.database.Servidor import Servidor


class ServidorRepository(IServidorRepository):

    # método privado
    def __existe(self, conn: Conexao, servidor: Servidor):
        # vai tentar pegar o prefixo, se não vier um prefixo
        # é porque o servidor não existe no banco
        if self.get_prefix(conn, servidor.id) is None:
            return False  # se ele não existir, retorna False
        return True  # se ele não passou pelo return False, vai retornar True

    def create(self, conn: Conexao, servidor: Servidor):
        """
        :param conn: Conexão com o banco de dados
        :param servidor: Servidor que vai ser criado no banco
        :type conn: Conexao
        :type servidor: Servidor
        :return: None
        :rtype: None
        """
        cursor = conn.cursor()  # pega o cursor
        try:
            query = 'CALL server_add(%s, %s);'  # query sql
            # o cursor vai colocar o id do servidor no lugar do primeiro "%s"
            # e o prefixo no lugar do segundos "%s" e executar a query
            cursor.execute(query, (servidor.id, servidor.prefix,))
            conn.salvar()  # se tudo ocorrer bem, ele vai salvar as alterações
        except psycopg2.IntegrityError as e:
            # se tentar adicionar um item que já existe
            if str(e).startswith('duplicate key value violates unique constraint'):
                raise Exception('duplicate servidor')
            else:  # se acontecer outro erro:
                raise Exception(e)
        except Exception as e:  # se acontecer outro erro:
            raise Exception(e)

    def get_prefix(self, conn: Conexao, serverId: int):
        """
        :param conn: Conexão com o banco de dados
        :param serverId: Id do servidor
        :type conn: Conexao
        :type serverId: int
        :return: Vai retornar o prefixo que esta salvo no banco, atrelado ao Id passado (se tiver)
        :rtype: str
        """
        cursor = conn.cursor()  # pega o cursor
        try:
            query = 'SELECT * FROM server_get_prefix(%s);'  # select para pegar o prefixo
            cursor.execute(query, (serverId,))  # vai trocar ^ esse %s pelo id do servidor
            resposta = cursor.fetchone()  # e depois, vai pegar o resultado do select
            # como o fetchone vai retornar uma tupla, vamos retornar apenas o
            # primeiro valor dessa tupla
            if resposta:  # se vier alguma coisa:
                return resposta[0]
            return None  # se não veio nada, retorna Nulo
        except Exception as e:
            return f'error: {str(e)}'  # se acontecer algum outro erro...

    def update(self, conn: Conexao, servidor: Servidor):
        """
        :param conn: Conexão com o banco de dados
        :param servidor: O servidor que vai ser alterado
        :type conn: Conexao
        :type servidor: Servidor
        :return: Vai sincronizar o objeto Servidor passado, com o servidor que existir no banco
        :rtype: bool
        """
        cursor = conn.cursor()  # pega o cursor
        # se o servidor não existir no banco, vai criar ele
        if not self.__existe(conn, servidor):
            self.create(conn, servidor)
            return True  # vai retornar True, pra dizer que não houve nenhum erro
        try:  # se ele já existe, vai atualizar
            query = 'CALL server_update(%s, %s);'
            # vai colocar o prefixo e o id no lugar dos %s, respectivamente
            cursor.execute(query, (servidor.prefix, servidor.id,))
            conn.salvar()
            return True
        except Exception as e:
            raise Exception(str(e))
        return False

    def delete(self, conn: Conexao, servidor: Servidor):
        """
        :param conn: Conexão com o banco de dados
        :param servidor: O servidor que vai ser alterado
        :type conn: Conexao
        :type servidor: Servidor
        :return: Vai deletar o servidor e tudo que estiver atrelados a ele do banco
        :rtype: bool
        """
        cursor = conn.cursor()  # pega o cursor
        try:
            query = 'CALL server_remove(%s);'
            cursor.execute(query, (servidor.id,))
            conn.salvar()
            return True
        except Exception as e:
            raise Exception(str(e))
