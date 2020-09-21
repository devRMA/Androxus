# coding=utf-8
# Androxus bot
# ComandoDesativadoDao.py

__author__ = 'Rafael'

import psycopg2
from .Factory import Factory


class ComandoDesativadoDao:
    def __init__(self):
        self.connection = Factory().getConnection()  # inicia a conexão com o banco
        self.cursor = self.connection.cursor()  # cria o cursor

    def create(self, serverId, comando):
        if isinstance(serverId, int) and isinstance(comando, str):  # verifica se os tipos das variaveis
            try:
                query = 'CALL cmd_desativado_add(%s, %s);'  # query
                self.cursor.execute(query, (serverId, comando.lower(),))
                self.connection.commit()  # se tudo ocorrer bem, ele vai salvar as alterações
                return True  # vai retornar True se tudo ocorrer bem
            except psycopg2.IntegrityError:
                raise Exception('duplicate key value violates unique constraint')
            except Exception as e:
                raise Exception(str(e))
            finally:
                self.cursor.close()
                self.connection.close()  # se der erro, ou não, vai fechar a conexão com o banco
        else:
            raise Exception('Erro no tipo do(s) parametro(s)')
        return False  # Se o return True não for executado, vai chegar aqui

    def get_comandos(self, serverId):
        if isinstance(serverId, int):
            try:
                query = 'SELECT * FROM cmd_desativado_get_comandos(%s);'  # funcion que está banco
                self.cursor.execute(query, (serverId,))  # vai coloc
                resposta = self.cursor.fetchall()
                return resposta
            except Exception as e:
                return f'error: {str(e)}'
            finally:
                self.cursor.close()
                self.connection.close()
        else:
            raise Exception('Erro no tipo do(s) parametro(s)')

    def delete(self, serverId, comando):
        if isinstance(serverId, int) and isinstance(comando, str):
            try:
                query = 'CALL cmd_desativado_remove(%s, %s);'
                self.cursor.execute(query, (serverId, comando,))
                self.connection.commit()
                return True
            except Exception as e:
                raise Exception(str(e))
            finally:
                self.cursor.close()
                self.connection.close()
        else:
            raise Exception('Erro no tipo do(s) parametro(s)')
        return False
