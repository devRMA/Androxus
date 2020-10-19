# coding=utf-8
# Androxus bot
# ComandoPersonalizadoRepository.py

__author__ = 'Rafael'

import psycopg2

from database.ComandoPersonalizado import ComandoPersonalizado
from database.Conexao import Conexao
from database.Repositories.Interfaces.IComandoPersonalizadoRepository import IComandoPersonalizadoRepository
from database.Servidor import Servidor


class ComandoPersonalizadoRepository(IComandoPersonalizadoRepository):

    # método privado
    def __existe(self, conn: Conexao, comandoPersonalizado: ComandoPersonalizado):
        # vai verificar todos os comandos personalizados que tem no servidor
        # pra ver se o comando já existe
        for c in self.get_commands(conn, comandoPersonalizado.servidor):
            if c == comandoPersonalizado:
                return True
        return False

    def create(self, conn: Conexao, comandoPersonalizado: ComandoPersonalizado):
        """
        :param conn: Conexão com o banco de dados
        :param comandoPersonalizado: Comando que vai ser adicionado ao banco
        :type conn: Conexao
        :type comandoPersonalizado: ComandoPersonalizado
        :return: Vai retornar True se tudo ocorrer bem
        :rtype: bool
        """
        cursor = conn.cursor()
        try:
            query = 'CALL cmd_personalizado_add (%s, %s, %s, %s);'
            cursor.execute(query, (comandoPersonalizado.servidor.id,
                                   comandoPersonalizado.comando,
                                   comandoPersonalizado.resposta,
                                   comandoPersonalizado.in_text,))
            conn.salvar()
            return True  # vai retornar True se tudo ocorrer bem
        except psycopg2.IntegrityError as e:
            # se tentar adicionar um item que já existe
            if str(e).startswith('duplicate key value violates unique constraint'):
                raise Exception('comando personalizado duplicado')
            else:
                raise e
        except Exception as e:
            raise Exception(str(e))

    def get_commands(self, conn: Conexao, servidor: Servidor):
        """
        :param conn: Conexão com o banco de dados
        :param servidor: Servidor que vai pegar os comandos personalizados
        :type conn: Conexao
        :type servidor: Servidor
        :return: Vai retornar uma lista com todos os comandos personalizados do servidor
        :rtype: list
        """
        cursor = conn.cursor()
        try:
            query = 'SELECT * FROM get_cmds_personalizados(%s);'
            cursor.execute(query, (servidor.id,))
            tuple_commands = cursor.fetchall()
            list_commands = []
            if tuple_commands:
                for command in tuple_commands:
                    list_commands.append(ComandoPersonalizado(servidor, command[0], command[1], command[-1]))
            return list_commands
        except Exception as e:
            return [f'error: {str(e)}']

    def update(self, conn: Conexao, comandoPersonalizado: ComandoPersonalizado):
        """
        :param conn: Conexão com o banco de dados
        :param comandoPersonalizado: Comando que vai ser atualizado
        :type conn: Conexao
        :type comandoPersonalizado: ComandoPersonalizado
        :return: Vai retornar True se tudo ocorrer bem
        :rtype: bool
        """
        if not self.__existe(conn, comandoPersonalizado):
            return self.create(conn, comandoPersonalizado)
        cursor = conn.cursor()
        try:
            query = 'CALL cmd_personalizado_update(%s, %s, %s, %s);'
            cursor.execute(query, (comandoPersonalizado.resposta,
                                   comandoPersonalizado.in_text,
                                   comandoPersonalizado.servidor.id,
                                   comandoPersonalizado.comando))
            conn.salvar()
            return True
        except Exception as e:
            raise Exception(str(e))
        return False

    def delete(self, conn: Conexao, comandoPersonalizado: ComandoPersonalizado):
        """
        :param conn: Conexão com o banco de dados
        :param comandoPersonalizado: Comando que vai ser deletado do banco
        :type conn: Conexao
        :type comandoPersonalizado: ComandoPersonalizado
        :return: Vai retornar True se tudo ocorrer bem
        :rtype: bool
        """
        cursor = conn.cursor()
        try:
            query = 'CALL cmd_personalizado_remove(%s, %s);'
            cursor.execute(query, (comandoPersonalizado.servidor.id, comandoPersonalizado.comando,))
            conn.salvar()
            return True
        except Exception as e:
            raise Exception(str(e))
        return False
