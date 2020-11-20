# -*- coding: utf-8 -*-
# Androxus bot
# IComandoPersonalizadoRepository.py

__author__ = 'Rafael'

from abc import ABCMeta, abstractmethod
from typing import List

import asyncpg

from database.Models.ComandoPersonalizado import ComandoPersonalizado
from database.Models.Servidor import Servidor


class IComandoPersonalizadoRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, conn: asyncpg.pool.Pool, comandoPersonalizado: ComandoPersonalizado) -> bool:
        """ Insert into da table comando personalizado """

    @abstractmethod
    def get_commands(self, conn: asyncpg.pool.Pool, servidor: Servidor) -> List[ComandoPersonalizado]:
        """ Select que vai trazer todos os comandos personalizados do servidor """

    @abstractmethod
    def update(self, conn: asyncpg.pool.Pool, comandoPersonalizado: ComandoPersonalizado) -> bool:
        """ Update da table comando personalizado """

    @abstractmethod
    def delete(self, conn: asyncpg.pool.Pool, comandoPersonalizado: ComandoPersonalizado) -> bool:
        """ Delete da table comando personalizado """
