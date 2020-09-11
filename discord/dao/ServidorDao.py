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
                self.query = 'INSERT INTO servers (serverId, prefixo) VALUES(%s, \'--\');'  # query
                self.cursor.execute(self.query, (serverId,))  # o cursor, vai colocar o "id" no lugar do "%s" e executar a query
                self.connection.commit()  # se tudo ocorrer bem, ele vai salvar as alterações
                return True  # vai retornar True se tudo ocorrer bem
            except psycopg2.IntegrityError as e:
                if str(e).startswith('UNIQUE constraint failed'):
                    raise Exception('Esse id já está registrado!')
                else:
                    raise e
            finally:
                self.connection.close()  # se der erro, ou não, vai fechar a conexão com o banco
        else:
            raise Exception('Id passado não é do tipo int!')
        return False  # Se o return True não for executado, vai chegar aqui

    def get_all(self):
        try:
            self.query = 'SELECT * FROM servers;'
            self.cursor.execute(self.query)
            self.resposta = self.cursor.fetchall()
            return self.resposta
        except Exception as e:
            return [f'error {e}']
        finally:
            self.connection.close()

    def get_prefix(self, serverId):
        if isinstance(serverId, int):
            try:
                self.query = 'SELECT prefixo FROM servers WHERE serverId = %s;'
                self.cursor.execute(self.query, (serverId,))
                self.resposta = self.cursor.fetchone()
                return self.resposta
            except Exception as e:
                return f'error: {str(e)}'
            finally:
                self.cursor.close()
                self.connection.close()
        else:
            raise Exception('Erro no tipo dos parametros')

    def update(self, serverId, prefixo):
        if isinstance(serverId, int) and isinstance(prefixo, str):
            try:
                self.query = 'UPDATE servers SET prefixo = %s WHERE serverId = %s;'
                self.cursor.execute(self.query, (prefixo, serverId,))
                self.connection.commit()
                return True
            except Exception as e:
                raise Exception(str(e))
            finally:
                self.connection.close()
        else:
            raise Exception('Erro no tipo dos parametros')

    def delete(self, serverId):
        if isinstance(serverId, int):
            try:
                self.query = 'DELETE FROM servers WHERE serverId = %s;'
                self.cursor.execute(self.query, (serverId,))
                self.query = 'DELETE FROM comandos_personalizados WHERE serverId = %s;'
                self.cursor.execute(self.query, (serverId,))
                self.query = 'DELETE FROM comandos_desativados WHERE serverId = %s;'
                self.cursor.execute(self.query, (serverId,))
                self.connection.commit()
                return True
            except Exception as e:
                raise Exception(str(e))
            finally:
                self.connection.close()
        else:
            raise Exception('Erro no tipo dos parametros')
