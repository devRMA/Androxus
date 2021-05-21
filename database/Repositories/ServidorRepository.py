# -*- coding: utf-8 -*-
# Androxus bot
# ServidorRepository.py

__author__ = 'Rafael'

import asyncpg

from Classes.erros import DuplicateServidor
from database.Models.Servidor import Servidor
from database.Repositories.Interfaces.IServidorRepository import IServidorRepository


class ServidorRepository(IServidorRepository):

    # método privado
    async def _existe(self, pool, servidor):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            servidor (Servidor): Servidor que vai ser verificado

        Returns:
            bool: Se o servidor existe no banco

        """
        if await self.get_servidor(pool, servidor.id) is None:
            return False  # se ele não existir, retorna False
        return True  # se ele não passou pelo return False, vai retornar True

    async def create(self, pool, servidor):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            servidor (Servidor): Servidor que vai ser criado no banco

        Returns:
            bool: Vai retornar True se conseguir criar o servidor

        """
        async with pool.acquire() as conn:
            try:
                query = 'CALL server_add($1, $2);'  # query sql
                await conn.execute(query, servidor.id, servidor.prefixo)
                return True
            except asyncpg.exceptions.UniqueViolationError:
                # se tentar adicionar um item que já existe
                raise DuplicateServidor()

    async def get_servidor(self, pool, serverId):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            serverId (int): Id do servidor

        Returns:
            Servidor: Vai retornar um objeto Servidor com todas as informações que estiverem salvas no banco

        """
        async with pool.acquire() as conn:
            query = 'SELECT * FROM get_server($1);'  # select para pegar o prefixo
            resposta = tuple(tuple(record) for record in await conn.fetch(query, serverId))
            if resposta:  # se vier alguma coisa:
                # apenas encurtando a variavel, para que a linha do return não fique muito grande
                r = resposta[0]
                return Servidor(serverId, r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10])
            return None  # se não veio nada, retorna Nulo

    async def update(self, pool, servidor):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            servidor (Servidor): O servidor que vai ser alterado

        Returns:
            bool: Vai sincronizar o objeto Servidor passado, com o servidor que existir no banco

        """
        # se o servidor não existir no banco, vai criar ele
        if not await self._existe(pool, servidor):
            return await self.create(pool, servidor)
        async with pool.acquire() as conn:
            query = 'CALL server_update($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12);'
            await conn.execute(query, servidor.prefixo,
                               servidor.channel_id_log,
                               servidor.mensagem_deletada,
                               servidor.mensagem_editada,
                               servidor.avatar_alterado,
                               servidor.nome_alterado,
                               servidor.tag_alterado,
                               servidor.nick_alterado,
                               servidor.role_alterado,
                               servidor.sugestao_de_comando,
                               servidor.lang,
                               servidor.id)
            return True

    async def delete(self, pool, servidor):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            servidor (Servidor): O servidor que vai ser deletado

        Returns:
            bool: Vai deletar o servidor e tudo que estiver atrelados a ele do banco e se foi, retorna True

        """
        async with pool.acquire() as conn:
            query = 'CALL server_remove($1);'
            await conn.execute(query, servidor.id)
            return True
