# coding=utf-8
# Androxus bot
# ComandoDesativado.py

__author__ = 'Rafael'

from discord_bot.database.Servidor import Servidor


class ComandoDesativado:
    servidor: Servidor
    comando: str

    def __init__(self, servidor, comando):
        self.servidor = servidor
        self.comando = comando
