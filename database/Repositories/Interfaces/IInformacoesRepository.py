# coding=utf-8
# Androxus bot
# IInformacoesRepository.py

__author__ = 'Rafael'

from abc import ABCMeta, abstractmethod

from database.Conexao import Conexao


class IInformacoesRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, conn: Conexao, informacao: str, dado: str):
        """ Insert into da table informacoes """

    @abstractmethod
    def get_dado(self, conn: Conexao, informacao: str):
        """ Select que vai trazer o dado daquela informação """

    @abstractmethod
    def update(self, conn: Conexao, informacao: str, dado: str):
        """ Update da table comando informacoes """

    @abstractmethod
    def delete(self, conn: Conexao, informacao: str):
        """ Delete da table informacoes """
