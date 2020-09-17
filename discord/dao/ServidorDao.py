# coding=utf-8
# Androxus bot
# ServidorDao.py

__author__ = 'Rafael'

from .Factory import Factory
import psycopg2

# CRUD da table servidor
class ServidorDao:
    def __init__(self):
        self.connection = Factory().getConnection() # inicia a conexão com o banco
        self.cursor = self.connection.cursor() # cria o cursor

    def create(self, serverId):
        if isinstance(serverId, int):  # verifica se o id é int
            try:
                query = 'INSERT INTO servers (serverId, prefixo) VALUES(%s, \'--\');'  # query
                self.cursor.execute(query, (serverId,))  # o cursor, vai colocar o "id" no lugar do "%s" e executar a query
                self.connection.commit()  # se tudo ocorrer bem, ele vai salvar as alterações
            except psycopg2.IntegrityError as e:
                if str(e).startswith('UNIQUE constraint failed'):
                    raise Exception('duplicate key value violates unique constraint')
                else:
                    raise Exception(str(e))
            except Exception as e:
                raise Exception(str(e))
            finally:
                self.cursor.close()  # se der erro, ou não, vai fechar o cursor com o banco
                self.connection.close()  # se der erro, ou não, vai fechar a conexão com o banco
        else:
            raise Exception('Erro no tipo do(s) parametro(s)')

    def get_prefix(self, serverId):
        if isinstance(serverId, int):  # verifica se o Id passado, é do tipo int
            try:  # se for, vai tentar fazer o select
                query = 'SELECT prefixo FROM servers WHERE serverId = %s;'  # select para pegar o prefixo
                self.cursor.execute(query, (serverId,))  # vai trocar ^ esse %s pelo id do servidor
                resposta = self.cursor.fetchone()  # e depois, vai pegar o resultado do select
                return resposta  # e retornar este resultado
            except Exception as e:
                return f'error: {str(e)}'  # se acontecer algum outro erro...
            finally:  # independete de acontecer ou não erro, vai executar isso
                self.cursor.close()  # chega a conexão do cursor
                self.connection.close()  # fecha a conexão com o banco
        else:  # se o id for de outro tipo, vai disparar um erro
            raise Exception('Erro no tipo do(s) parametro(s)')

    def update(self, serverId, prefixo):
        if isinstance(serverId, int) and isinstance(prefixo, str):
            try:
                query = 'UPDATE servers SET prefixo = %s WHERE serverId = %s;'
                self.cursor.execute(query, (prefixo, serverId,))
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

    def delete(self, serverId):
        if isinstance(serverId, int):
            try:
                query = 'DELETE FROM servers WHERE serverId = %s;'
                self.cursor.execute(query, (serverId,))
                query = 'DELETE FROM comandos_personalizados WHERE serverId = %s;'
                self.cursor.execute(query, (serverId,))
                query = 'DELETE FROM comandos_desativados WHERE serverId = %s;'
                self.cursor.execute(query, (serverId,))
                self.connection.commit()
            except Exception as e:
                raise Exception(str(e))
            finally:
                self.cursor.close()
                self.connection.close()
        else:
            raise Exception('Erro no tipo do(s) parametro(s)')
