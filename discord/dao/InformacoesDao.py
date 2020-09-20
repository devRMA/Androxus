# coding=utf-8
# Androxus bot
# InformacoesDao.py

__author__ = 'Rafael'

import psycopg2
from discord.dao.Factory import Factory


class InformacoesDao:
    def __init__(self):
        self.connection = Factory().getConnection()  # inicia a conexão com o banco
        self.cursor = self.connection.cursor()  # cria o cursor

    def create(self, informacao, dado):
        if isinstance(informacao, str) and isinstance(dado, str):  # verifica se os tipos das variaveis
            try:
                query = 'CALL info_add(%s, %s);'  # query
                self.cursor.execute(query, (informacao, dado,))
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

    def get(self, informacao):
        if isinstance(informacao, str):
            try:
                query = 'SELECT * FROM info_get(%s);'
                self.cursor.execute(query, (informacao,))
                resposta = self.cursor.fetchone()
                return resposta
            except Exception as e:
                return f'error: {str(e)}'
            finally:
                self.cursor.close()
                self.connection.close()
        else:
            raise Exception('Erro no tipo do(s) parametro(s)')

    def update(self, informacao, dado):
        if isinstance(informacao, str) and isinstance(dado, str):
            try:
                query = 'CALL info_update(%s, %s);'
                self.cursor.execute(query, (dado, informacao,))
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

    def delete(self, informacao):
        if isinstance(informacao, str):
            try:
                query = 'CALL info_remove(%s);'
                self.cursor.execute(query, (informacao,))
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

    def get_version(self):
        try:
            query = 'SELECT version()'
            self.cursor.execute(query)
            resposta = self.cursor.fetchone()
            return resposta[0]
        except Exception as e:
            return f'error: {str(e)}'
        finally:
            self.cursor.close()
            self.connection.close()
