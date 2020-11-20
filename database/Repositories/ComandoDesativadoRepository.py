# -*- coding: utf-8 -*-
# Androxus bot
# ComandoDesativadoRepository.py

__author__ = 'Rafael'

import asyncpg

from Classes.erros import DuplicateComandoDesativado, ComandoDesativadoNotFound
from database.Models.ComandoDesativado import ComandoDesativado
from database.Models.Servidor import Servidor
from database.Repositories.Interfaces.IComandoDesativadoRepository import IComandoDesativadoRepository


class ComandoDesativadoRepository(IComandoDesativadoRepository):

    # método privado
    async def _existe(self, pool, comandoDesativado):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            comandoDesativado (ComandoDesativado): Comando a ser verificado

        Returns:
            bool: Verifica se o comando existe no banco

        """
        # vai pegar todos os comandos desativados deste servidor
        comandos = await self.get_commands(pool, comandoDesativado.servidor)
        for c in comandos:
            # se o comando desativado do servidor for igual ao comando passado
            if c.comando == comandoDesativado.comando:
                # significa que ele existe, então retorna True
                return True
        return False  # se ele não passou pelo return dentro do for, vai retornar False

    async def create(self, pool, comandoDesativado):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            comandoDesativado (ComandoDesativado): Comando que vai ser adicionado ao banco

        Returns:
            bool: Se conseguir adicionar o comando ao banco, vai retornar True

        """
        async with pool.acquire() as conn:
            try:
                query = 'CALL cmd_desativado_add($1, $2);'  # query
                await conn.execute(query, comandoDesativado.servidor.id, comandoDesativado.comando.lower())
                return True  # se chegar até aqui, retorna True
            except asyncpg.exceptions.UniqueViolationError:
                # se tentar adicionar um item que já existe
                raise DuplicateComandoDesativado()

    async def get_commands(self, pool, servidor):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            servidor (Servidor): Servidor que quer saber todos os comandos desativados

        Returns:
            list: Lista com todos os ComandoDesativado que o servidor tem

        """
        async with pool.acquire() as conn:
            query = 'SELECT * FROM cmd_desativado_get_comandos($1);'  # function que está banco
            # vai executar a query e transformar o resultado em tuple
            tupla_comandos_desativados = tuple(tuple(record) for record in await conn.fetch(query, servidor.id))
            # depois, transformar os resultados do banco em objetos
            lista_comandos_desativados = [ComandoDesativado(servidor, comando[0]) for comando in
                                          tupla_comandos_desativados]
            # e retornar a lista com esses objetos
            return lista_comandos_desativados

    async def delete(self, pool, comandoDesativado):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            comandoDesativado (ComandoDesativado): Comando desativado que vai ser removido do banco

        Returns:
            bool: Se conseguir remover o comando do banco, vai retornar True

        """
        # se o comando não existir no banco:
        if not await self._existe(pool, comandoDesativado):
            # é porque ele não está desativado
            raise ComandoDesativadoNotFound()
        async with pool.acquire() as conn:
            query = 'CALL cmd_desativado_remove($1, $2);'
            await conn.execute(query, comandoDesativado.servidor.id, comandoDesativado.comando.lower())
            return True
