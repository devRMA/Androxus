# coding=utf-8
# Androxus bot
# IComandoDesativadoRepository.py

__author__ = 'Rafael'

from abc import ABCMeta, abstractmethod

from discord_bot.database.ComandoDesativado import ComandoDesativado
from discord_bot.database.Conexao import Conexao
from discord_bot.database.Servidor import Servidor


class IComandoDesativadoRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, conn: Conexao, comandoDesativado: ComandoDesativado):
        """ Insert into da table comandos desativados """

    @abstractmethod
    def get_commands(self, conn: Conexao, servidor: Servidor):
        """ Select que vai pegar todos os comandos desativados """

    @abstractmethod
    def delete(self, conn: Conexao, comandoDesativado: ComandoDesativado):
        """ Delete da table comandos desativados """
