# coding=utf-8
# Androxus bot
# IComandoPersonalizadoRepository.py

__author__ = 'Rafael'

from abc import ABCMeta, abstractmethod

from database.ComandoPersonalizado import ComandoPersonalizado
from database.Conexao import Conexao
from database.Servidor import Servidor


class IComandoPersonalizadoRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, conn: Conexao, comandoPersonalizado: ComandoPersonalizado):
        """ Insert into da table comando personalizado """

    @abstractmethod
    def get_commands(self, conn: Conexao, servidor: Servidor):
        """ Select que vai trazer todos os comandos personalizados do servidor """

    @abstractmethod
    def update(self, conn: Conexao, comandoPersonalizado: ComandoPersonalizado):
        """ Update da table comando personalizado """

    @abstractmethod
    def delete(self, conn: Conexao, comandoPersonalizado: ComandoPersonalizado):
        """ Delete da table comando personalizado """
