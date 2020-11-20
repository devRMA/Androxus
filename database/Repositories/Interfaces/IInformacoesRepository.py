# -*- coding: utf-8 -*-
# Androxus bot
# IInformacoesRepository.py

__author__ = 'Rafael'

from abc import ABCMeta, abstractmethod

import asyncpg


class IInformacoesRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, conn: asyncpg.pool.Pool, informacao: str, dado: str) -> bool:
        """ Insert into da table informacoes """

    @abstractmethod
    def get_dado(self, conn: asyncpg.pool.Pool, informacao: str) -> str:
        """ Select que vai trazer o dado daquela informação """

    @abstractmethod
    def update(self, conn: asyncpg.pool.Pool, informacao: str, dado: str) -> bool:
        """ Update da table comando informacoes """

    @abstractmethod
    def delete(self, conn: asyncpg.pool.Pool, informacao: str) -> bool:
        """ Delete da table informacoes """
