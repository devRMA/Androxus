# coding=utf-8
# Androxus bot
# ComandoPersonalizado.py

__author__ = 'Rafael'

from database.Servidor import Servidor


class ComandoPersonalizado:
    servidor: Servidor
    comando: str
    resposta: str
    in_text: bool

    def __init__(self, servidor, comando, resposta, inText):
        self.servidor = servidor
        self.comando = comando
        self.resposta = resposta
        self.in_text = inText

    def __eq__(self, other):
        if other.__class__ == self.__class__:
            return (other.servidor.id == self.servidor.id) and (other.comando == self.comando)
        return False
