# coding=utf-8
# Androxus bot
# IComandoDesativadoRepository.py

__author__ = 'Rafael'

from abc import ABCMeta, abstractmethod

from database.ComandoDesativado import ComandoDesativado
from database.Conexao import Conexao
from database.Servidor import Servidor


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
