# coding=utf-8
# Androxus bot
# IServidorRepository.py

__author__ = 'Rafael'

from abc import ABCMeta, abstractmethod

from discord_bot.database.Conexao import Conexao
from discord_bot.database.Servidor import Servidor


class IServidorRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, conn: Conexao, servidor: Servidor):
        """ Insert into da table servidor """

    @abstractmethod
    def get_servidor(self, conn: Conexao, serverId: int):
        """ Select que vai pegar o prefixo """

    @abstractmethod
    def update(self, conn: Conexao, servidor: Servidor):
        """ Update da table servidor """

    @abstractmethod
    def delete(self, conn: Conexao, servidor: Servidor):
        """ Delete da table servidor """
