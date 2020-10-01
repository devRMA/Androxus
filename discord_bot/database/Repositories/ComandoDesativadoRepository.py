# coding=utf-8
# Androxus bot
# ComandoDesativadoRepository.py

__author__ = 'Rafael'

import psycopg2

from discord_bot.database.ComandoDesativado import ComandoDesativado
from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.Interfaces.IComandoDesativadoRepository import IComandoDesativadoRepository
from discord_bot.database.Servidor import Servidor


class ComandoDesativadoRepository(IComandoDesativadoRepository):

    # método privado
    def __existe(self, conn: Conexao, comandoDesativado: ComandoDesativado):
        # vai pegar todos os comandos desativados deste servidor
        comandos = self.get_commands(conn, comandoDesativado.servidor)
        for c in comandos:
            # se o comando desativado do servidor for igual ao comando passado
            if c.comando == comandoDesativado.comando:
                # segnifica que ele existe, então retorna True
                return True
        return False  # se ele não passou pelo return dentro do for, vai retornar False

    def create(self, conn: Conexao, comandoDesativado: ComandoDesativado):
        """
        :param conn: Conexão com o banco de dados
        :param comandoDesativado: Comando desativado que vai ser adicionado ao banco
        :type conn: Conexao
        :type comandoDesativado: ComandoDesativado
        :return: Se conseguir adicionar o comando ao banco, vai retornar True
        :rtype: bool
        """
        cursor = conn.cursor()  # pega o cursor
        try:
            query = 'CALL cmd_desativado_add(%s, %s);'  # query
            cursor.execute(query, (comandoDesativado.servidor.id, comandoDesativado.comando.lower(),))
            conn.salvar()  # se tudo ocorrer bem, ele vai salvar as alterações
            return True  # se chegar até aqui, retorna True
        except psycopg2.IntegrityError as e:
            # se tentar adicionar um item que já existe
            if str(e).startswith('duplicate key value violates unique constraint'):
                raise Exception('duplicate comando desativado')
            else:
                raise e
        except Exception as e:
            raise Exception(str(e))
        return False

    def get_commands(self, conn: Conexao, servidor: Servidor):
        """
        :param conn: Conexão com o banco de dados
        :param servidor: Servidor que quer saber todos os comandos desativados
        :type conn: Conexao
        :type servidor: Servidor
        :return: Vai retornar a lista com todos os ComandoDesativado que o servidor tem
        :rtype: list
        """
        cursor = conn.cursor()
        try:
            query = 'SELECT * FROM cmd_desativado_get_comandos(%s);'  # function que está banco
            cursor.execute(query, (servidor.id,))
            tuple_comandos_desativados = cursor.fetchall()
            list_comandos_desativados = []
            for comando in tuple_comandos_desativados:
                list_comandos_desativados.append(ComandoDesativado(servidor, comando[0]))
            return list_comandos_desativados
        except Exception as e:
            return [f'error: {str(e)}']

    def delete(self, conn: Conexao, comandoDesativado: ComandoDesativado):
        """
        :param conn: Conexão com o banco de dados
        :param comandoDesativado: Comando desativado que vai ser removido do banco
        :type conn: Conexao
        :type comandoDesativado: ComandoDesativado
        :return: Se conseguir remover o comando do banco, vai retornar True
        :rtype: bool
        """
        # se o comando não existir no banco:
        if not self.__existe(conn, comandoDesativado):
            # é porque ele não está desativado
            raise Exception('Este comando já está ativo!')
        cursor = conn.cursor()
        try:
            query = 'CALL cmd_desativado_remove(%s, %s);'
            cursor.execute(query, (comandoDesativado.servidor.id, comandoDesativado.comando.lower(),))
            conn.salvar()
            return True
        except Exception as e:
            raise Exception(str(e))
