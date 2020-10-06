# coding=utf-8
# Androxus bot
# ComandoPersonalizado.py

__author__ = 'Rafael'

from discord_bot.database.Servidor import Servidor


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
