# -*- coding: utf-8 -*-
# Androxus bot
# ComandoPersonalizado.py

__author__ = 'Rafael'

from database.Models.Servidor import Servidor


class ComandoPersonalizado:
    __slots__ = ('servidor', 'comando', 'resposta', 'in_text')
    servidor: Servidor
    comando: str
    resposta: str
    in_text: bool

    def __init__(self, servidor, comando, resposta, in_text):
        self.servidor = servidor
        self.comando = comando
        self.resposta = resposta
        self.in_text = in_text

    def __eq__(self, other):
        if other.__class__ == self.__class__:
            return (other.servidor.id == self.servidor.id) and (other.comando == self.comando)
        return False
