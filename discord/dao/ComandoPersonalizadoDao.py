# coding=utf-8
# Androxus bot
# ComandoPersonalizadoDao.py

__author__ = 'Rafael'

import psycopg2
from discord.dao.Factory import Factory


class ComandoPersonalizadoDao:
    def __init__(self):
        self.connection = Factory().getConnection()  # inicia a conexão com o banco
        self.cursor = self.connection.cursor()  # cria o cursor

    def create(self, serverId, comando, resposta, inText=False):
        if isinstance(serverId, int) and isinstance(comando, str) and isinstance(resposta, str) and isinstance(inText,
                                                                                                               bool):  # verifica se os tipos dos parametros
            try:
                query = 'INSERT INTO comandos_personalizados(serverId, comando, resposta, inText) VALUES(%s,' + \
                        '%s, %s, %s);'
                self.cursor.execute(query, (serverId, comando, resposta, inText,))
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
                query = 'SELECT comando FROM comandos_personalizados WHERE serverId = %s;'
                self.cursor.execute(query, (serverId,))
                resposta = self.cursor.fetchall()
                return resposta
            except Exception as e:
                return f'error: {str(e)}'
            finally:
                self.cursor.close()
                self.connection.close()
        else:
            raise Exception('Erro no tipo do(s) parametro(s)')

    def get_resposta(self, serverId, comando):
        if isinstance(serverId, int) and isinstance(comando, str):
            try:
                query = 'SELECT resposta, inText FROM comandos_personalizados WHERE serverId = %s AND comando = %s;'
                self.cursor.execute(query, (serverId, comando,))
                resposta = self.cursor.fetchone()
                return resposta
            except Exception as e:
                return f'error: {str(e)}'
            finally:
                self.cursor.close()
                self.connection.close()
        else:
            raise Exception('Erro no tipo do(s) parametro(s)')

    def update(self, serverId, comando, resposta, inText):
        if isinstance(serverId, int) and isinstance(comando, str) and isinstance(resposta, str) and isinstance(inText,
                                                                                                               bool):
            try:
                query = 'UPDATE comandos_personalizados SET resposta = %s, inText = %s WHERE serverId = %s AND comando = %s;'
                self.cursor.execute(query, (resposta, inText, serverId, comando))
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

    def delete(self, serverId, comando):
        if isinstance(serverId, int) and isinstance(comando, str):
            try:
                query = 'DELETE FROM comandos_personalizados WHERE serverId = %s AND comando = %s;'
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
