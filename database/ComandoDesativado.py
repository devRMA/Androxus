# coding=utf-8
# Androxus bot
# ComandoDesativado.py

__author__ = 'Rafael'

from database.Servidor import Servidor


class ComandoDesativado:
    servidor: Servidor
    comando: str

    def __init__(self, servidor, comando):
        self.servidor = servidor
        self.comando = comando

    def __eq__(self, other):
        if other.__class__ == self.__class__:
            return (other.servidor.id == self.servidor.id) and (other.comando == self.comando)
        return False
