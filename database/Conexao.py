# coding=utf-8
# Androxus bot
# Conexao.py

__author__ = 'Rafael'

from database.Factories.ConnectionFactory import ConnectionFactory


class Conexao:
    def __init__(self):
        self.conn = ConnectionFactory.get_connection()
        self.cur = self.conn.cursor()

    def cursor(self):
        return self.cur

    def salvar(self):
        self.conn.commit()

    def fechar(self):
        self.cur.close()
        self.conn.close()
