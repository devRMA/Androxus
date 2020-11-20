# -*- coding: utf-8 -*-
# Androxus bot
# IComandoDesativadoRepository.py

__author__ = 'Rafael'

from abc import ABCMeta, abstractmethod
from typing import List

import asyncpg

from database.Models.ComandoDesativado import ComandoDesativado
from database.Models.Servidor import Servidor


class IComandoDesativadoRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, conn: asyncpg.pool.Pool, comandoDesativado: ComandoDesativado) -> bool:
        """ Insert into da table comandos desativados """

    @abstractmethod
    def get_commands(self, conn: asyncpg.pool.Pool, servidor: Servidor) -> List[ComandoDesativado]:
        """ Select que vai pegar todos os comandos desativados """

    @abstractmethod
    def delete(self, conn: asyncpg.pool.Pool, comandoDesativado: ComandoDesativado) -> bool:
        """ Delete da table comandos desativados """
