# coding=utf-8
# Androxus bot
# ComandoDesativado.py

__author__ = 'Rafael'

from discord_bot.database.Servidor import Servidor


class ComandoDesativado:
    servidor: Servidor
    comando: str

    def __init__(self, servidor, comando):
        self._servidor = servidor
        self._comando = comando

    @property
    def servidor(self):
        return self._servidor

    @property
    def comando(self):
        return self._comando

    @servidor.setter
    def servidor(self, servidor):
        self._servidor = servidor

    @comando.setter
    def comando(self, comando):
        self._comando = comando
