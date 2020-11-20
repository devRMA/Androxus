# -*- coding: utf-8 -*-
# Androxus bot
# BlacklistRepository.py

__author__ = 'Rafael'

from datetime import datetime

import asyncpg

from Classes.erros import DuplicateBlacklist
from database.Repositories.Interfaces.IBlacklistRepository import IBlacklistRepository


class BlacklistRepository(IBlacklistRepository):

    async def create(self, pool, pessoaId, motivo):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            pessoaId (int): Id da pessoa que vai pra blacklist
            motivo (str): Motivo por estar colocando o user na blacklist

        Returns:
            bool: Vai adicionar a pessoa na blacklist, se foi, vai retornar True

        Raises:
            DuplicateBlacklist: Se o valor já existir no banco

        """
        async with pool.acquire() as conn:
            try:
                query = 'CALL blacklist_add( $1, $2, $3 );'
                await conn.execute(query, pessoaId, motivo, str(datetime.utcnow()))
                return True  # vai retornar True se tudo ocorrer bem
            except asyncpg.exceptions.UniqueViolationError:  # se esse item já existir
                raise DuplicateBlacklist()

    async def get_pessoa(self, pool, pessoaId):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            pessoaId (int): Id da pessoa que vai ser verificada no banco

        Returns:
            list: Retorna se a pessoa está na blacklist, o motivo e quando foi

        """
        async with pool.acquire() as conn:
            query = 'SELECT * FROM blacklist_get_pessoa ( $1 );'
            # vai fazer o select, se retorna algo, é porque o id passado está na blacklist
            resps = tuple(tuple(record) for record in await conn.fetch(query, pessoaId))
            if resps:
                resps = resps[0]
                return [True, resps[1], datetime.strptime(resps[-1], '%Y-%m-%d %H:%M:%S.%f')]
            # se retornou None, é porque a pessoa não está na blacklist
            return [False, None, None]

    async def delete(self, pool, pessoaId):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            pessoaId (int): Id da pessoa que vai ser tirada do banco

        Returns:
            bool: Se o usuário foi removido com sucesso, vai retornar True, se não, False

        """
        async with pool.acquire() as conn:
            query = 'CALL blacklist_remove( $1 );;'
            await conn.execute(query, pessoaId)
            return True
