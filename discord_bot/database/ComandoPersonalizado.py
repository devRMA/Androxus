# coding=utf-8
# Androxus bot
# ComandoPersonalizado.py

__author__ = 'Rafael'

from discord_bot.database.Servidor import Servidor


class ComandoPersonalizado:
    def __init__(self,
                 servidor: Servidor,
                 comando: str,
                 resposta: str,
                 inText: bool):
        self._servidor = servidor
        self._comando = comando
        self._resposta = resposta
        self._in_text = inText

    @property
    def servidor(self):
        return self._servidor

    @property
    def comando(self):
        return self._comando

    @property
    def resposta(self):
        return self._resposta

    @property
    def inText(self):
        return self._in_text

    @servidor.setter
    def servidor(self, servidor):
        self._servidor = servidor

    @comando.setter
    def comando(self, comando):
        self._comando = comando

    @resposta.setter
    def resposta(self, resposta):
        self._resposta = resposta

    @inText.setter
    def inText(self, inText):
        self._in_text = inText
