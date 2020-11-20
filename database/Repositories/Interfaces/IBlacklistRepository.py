# -*- coding: utf-8 -*-
# Androxus bot
# IBlacklistRepository.py

__author__ = 'Rafael'

from abc import ABCMeta, abstractmethod
from datetime import datetime

import asyncpg


class IBlacklistRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, conn: asyncpg.pool.Pool, pessoaId: int, motivo: str) -> bool:
        """ Insert into da table blacklist """

    @abstractmethod
    def get_pessoa(self, conn: asyncpg.pool.Pool, pessoaId: int) -> [bool, str, datetime]:
        """ Select que vai pegar todos os blacklist """

    @abstractmethod
    def delete(self, conn: asyncpg.pool.Pool, pessoaId: int) -> bool:
        """ Delete da table blacklist """
