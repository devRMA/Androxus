# -*- coding: utf-8 -*-
# Androxus bot
# ComandoPersonalizadoRepository.py

__author__ = 'Rafael'

import asyncpg

from Classes.Erros import DuplicateComandoPersonalizado
from database.Models.ComandoPersonalizado import ComandoPersonalizado
from database.Repositories.Interfaces.IComandoPersonalizadoRepository import IComandoPersonalizadoRepository


class ComandoPersonalizadoRepository(IComandoPersonalizadoRepository):

    # método privado
    async def _existe(self, pool, comandoPersonalizado):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            comandoPersonalizado (ComandoPersonalizado): Comando personalizado que vai ser verificado

        Returns:
            bool: Retorna se o comando personalizado já existe no banco

        """
        # vai verificar todos os comandos personalizados que tem no servidor
        # pra ver se o comando já existe
        for c in await self.get_commands(pool, comandoPersonalizado.servidor):
            if c == comandoPersonalizado:
                return True
        return False

    async def create(self, pool, comandoPersonalizado):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            comandoPersonalizado (ComandoPersonalizado): Comando que vai ser adicionado ao banco

        Returns:
            bool: Vai retornar True se tudo ocorrer bem

        """
        async with pool.acquire() as conn:
            try:
                query = 'CALL cmd_personalizado_add ($1, $2, $3, $4);'
                await conn.execute(query, comandoPersonalizado.servidor.id,
                                   comandoPersonalizado.comando,
                                   comandoPersonalizado.resposta,
                                   comandoPersonalizado.in_text)
                return True  # vai retornar True se tudo ocorrer bem
            except asyncpg.exceptions.UniqueViolationError:
                # se tentar adicionar um item que já existe
                raise DuplicateComandoPersonalizado()

    async def get_commands(self, pool, servidor):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            servidor (Servidor): Servidor que vai pegar os comandos personalizados

        Returns:
            list: Uma lista com todos os comandos personalizados do servidor

        """
        async with pool.acquire() as conn:
            query = 'SELECT * FROM get_cmds_personalizados($1);'
            tuple_commands = tuple(tuple(record) for record in await conn.fetch(query, servidor.id))
            list_commands = []
            if tuple_commands:
                for command in tuple_commands:
                    list_commands.append(ComandoPersonalizado(servidor, command[0], command[1], command[-1]))
            return list_commands

    async def update(self, pool, comandoPersonalizado):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            comandoPersonalizado (ComandoPersonalizado): Comando que vai ser atualizado

        Returns:
            bool: Vai retornar True se tudo ocorrer bem

        """
        if not await self._existe(pool, comandoPersonalizado):
            return await self.create(pool, comandoPersonalizado)
        async with pool.acquire() as conn:
            query = 'CALL cmd_personalizado_update($1, $2, $3, $4);'
            await conn.execute(query, comandoPersonalizado.resposta,
                               comandoPersonalizado.in_text,
                               comandoPersonalizado.servidor.id,
                               comandoPersonalizado.comando)
            return True

    async def delete(self, pool, comandoPersonalizado):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            comandoPersonalizado (ComandoPersonalizado): Comando que vai ser deletado do banco

        Returns:
            bool: Vai retornar True se tudo ocorrer bem

        """
        async with pool.acquire() as conn:
            query = 'CALL cmd_personalizado_remove($1, $2);'
            await conn.execute(query, comandoPersonalizado.servidor.id, comandoPersonalizado.comando)
            return True
