# -*- coding: utf-8 -*-
# Androxus bot
# IServidorRepository.py

__author__ = 'Rafael'

from abc import ABCMeta, abstractmethod

import asyncpg

from database.Models.Servidor import Servidor


class IServidorRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, conn: asyncpg.pool.Pool, servidor: Servidor) -> bool:
        """ Insert into da table servidor """

    @abstractmethod
    def get_servidor(self, conn: asyncpg.pool.Pool, serverId: int) -> Servidor:
        """ Select que vai pegar o prefixo """

    @abstractmethod
    def update(self, conn: asyncpg.pool.Pool, servidor: Servidor) -> bool:
        """ Update da table servidor """

    @abstractmethod
    def delete(self, conn: asyncpg.pool.Pool, servidor: Servidor) -> bool:
        """ Delete da table servidor """
