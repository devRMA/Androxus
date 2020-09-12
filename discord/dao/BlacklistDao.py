# coding=utf-8
# Androxus bot
# BlacklistDao.py

__author__ = 'Rafael'


import psycopg2
from discord.dao.Factory import Factory

# CRUD da table blacklist


class BlacklistDao:
    def __init__(self):
        self.connection = Factory().getConnection()  # inicia a conexão com o banco
        self.cursor = self.connection.cursor()  # cria o cursor

    def create(self, pessoaId):
        if isinstance(pessoaId, int):  # verifica se o id é int
            try:
                self.query = 'INSERT INTO blacklist (pessoaId) VALUES(%s);'  # query
                self.cursor.execute(self.query,
                                    (pessoaId,))  # o cursor, vai colocar o "id" no lugar do "%s" e executar a query
                self.connection.commit()  # se tudo ocorrer bem, ele vai salvar as alterações
                return True  # vai retornar True se tudo ocorrer bem
            except psycopg2.IntegrityError as e:
                if str(e).startswith('UNIQUE constraint failed'):
                    raise Exception('Esse id já está registrado!')
                else:
                    raise e
            finally:
                self.cursor.close()  # se der erro, ou não, vai fechar o cursor com o banco
                self.connection.close()  # se der erro, ou não, vai fechar a conexão com o banco
        else:
            raise Exception('Id passado não é do tipo int!')
        return False  # Se o return True não for executado, vai chegar aqui

    def get_pessoa(self, pessoaId):
        if isinstance(pessoaId, int):
            try:
                self.query = 'SELECT * FROM blacklist WHERE pessoaId = %s;'
                self.cursor.execute(self.query, (pessoaId,))
                if self.cursor.fetchone() != None:  # vai fazer o select, se retornal algo, o id passado está na blacklist
                    return True
                else:  # se retornou None, é porque a pessoa não está na blacklist
                    return False
            except Exception as e:
                return f'error: {str(e)}'
            finally:
                self.cursor.close()
                self.connection.close()
        else:
            raise Exception('Erro no tipo dos parametros')

    def delete(self, pessoaId):
        if isinstance(pessoaId, int):
            try:
                self.query = 'DELETE FROM blacklist WHERE pessoaId = %s;'
                self.cursor.execute(self.query, (pessoaId,))
                self.connection.commit()
            except Exception as e:
                raise Exception(str(e))
            finally:
                self.cursor.close()
                self.connection.close()
        else:
            raise Exception('Erro no tipo dos parametros')
