# -*- coding: utf-8 -*-
# Androxus bot
# InformacoesRepository.py

__author__ = 'Rafael'

from database.Repositories.Interfaces.IInformacoesRepository import IInformacoesRepository


class InformacoesRepository(IInformacoesRepository):

    async def create(self, pool, informacao, dado):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            informacao (str): Informação que vai ser salva no banco
            dado (str): O dado referente a informação

        Returns:
            bool: Se conseguir adicionar o comando ao banco, vai retornar True

        """
        async with pool.acquire() as conn:
            query = 'CALL info_add($1, $2);'  # query
            try:
                await conn.execute(query, informacao, dado)
                return True  # vai retornar True se tudo ocorrer bem
            except:
                return False

    async def get_dado(self, pool, informacao):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            informacao (str): Informação que vai querer pegar o dado

        Returns:
            str: Vai retornar o dado referente a informação passada

        """
        async with pool.acquire() as conn:
            query = 'SELECT * FROM info_get($1);'
            resposta = tuple(tuple(record) for record in await conn.fetch(query, informacao))
            if resposta:
                return resposta[0][0]
            return None

    async def update(self, pool, informacao, dado):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            informacao (str): Informação que vai ser atualizada
            dado (str): O dado que também vai ser atualizado

        Returns:
            bool: Se conseguir atualizar, vai retornar True

        """
        async with pool.acquire() as conn:
            query = 'CALL info_update($1, $2);'
            await conn.execute(query, dado, informacao)
            return True

    async def delete(self, pool, informacao):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados
            informacao (str): Informação que vai ser deletada

        Returns:
            bool: Se conseguiu deletar a informação, retorna True

        """
        async with pool.acquire() as conn:
            query = 'CALL info_remove($1);'
            await conn.execute(query, informacao)
            return True

    async def get_sql_version(self, pool):
        """

        Args:
            pool (asyncpg.pool.Pool): Conexão com o banco de dados

        Returns:
            str: Vai retornar a versão do banco de dados

        """
        async with pool.acquire() as conn:
            query = 'SELECT version();'
            resposta = tuple((await conn.fetch(query))[0])
            return resposta[0]
