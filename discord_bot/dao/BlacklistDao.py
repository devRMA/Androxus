# coding=utf-8
# Androxus bot
# BlacklistDao.py

__author__ = 'Rafael'


import psycopg2
from .Factory import Factory


class BlacklistDao:
    def __init__(self):
        self.connection = Factory().getConnection()  # inicia a conexão com o banco
        self.cursor = self.connection.cursor()  # cria o cursor

    def create(self, pessoaId):
        if isinstance(pessoaId, int):  # verifica se o id é int
            try:
                # function do banco
                query = 'CALL blacklist_add( %s )'  # query
                self.cursor.execute(query,
                                    (pessoaId,))  # o cursor, vai colocar o "id" no lugar do "%s" e executar a query
                self.connection.commit()  # se tudo ocorrer bem, ele vai salvar as alterações
                return True  # vai retornar True se tudo ocorrer bem
            except psycopg2.IntegrityError as e:  # se esse item já existir
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
        return False  # Se o return True não for executado, vai chegar aqui

    def get_pessoa(self, pessoaId):
        if isinstance(pessoaId, int):
            try:
                query = 'SELECT * FROM blacklist_get_pessoa ( %s );'
                self.cursor.execute(query, (pessoaId,))
                # vai fazer o select, se retornal algo, o id passado está na blacklist
                if self.cursor.fetchone() is not None:
                    return True
                else:  # se retornou None, é porque a pessoa não está na blacklist
                    return False
            except Exception as e:
                return f'error: {str(e)}'
            finally:
                self.cursor.close()
                self.connection.close()
        else:
            raise Exception('Erro no tipo do(s) parametro(s)')

    def delete(self, pessoaId):
        if isinstance(pessoaId, int):
            try:
                query = 'CALL blacklist_remove( %s );;'
                self.cursor.execute(query, (pessoaId,))
                self.connection.commit()
            except Exception as e:
                raise Exception(str(e))
            finally:
                self.cursor.close()
                self.connection.close()
        else:
            raise Exception('Erro no tipo do(s) parametro(s)')
        return False
