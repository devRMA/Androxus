# coding=utf-8
# Androxus bot
# IBlacklistRepository.py

__author__ = 'Rafael'

from abc import ABCMeta, abstractmethod

from discord_bot.database.Conexao import Conexao


class IBlacklistRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, conn: Conexao, pessoaId: int):
        """ Insert into da table blacklist """

    @abstractmethod
    def get_pessoa(self, conn: Conexao, pessoaId: int):
        """ Select que vai pegar todos os blacklist """

    @abstractmethod
    def delete(self, conn: Conexao, pessoaId: int):
        """ Delete da table blacklist """
