# -*- coding: utf-8 -*-
# Androxus bot
# test.py

__author__ = 'Rafael'

import asyncio

import testing.postgresql

from Classes.Test import Test, executar_testes
from Classes.Erros import *
from database.Factories.ConnectionFactory import ConnectionFactory
from database.Models.ComandoDesativado import ComandoDesativado
from database.Models.ComandoPersonalizado import ComandoPersonalizado
from database.Models.Servidor import Servidor
from database.Repositories.BlacklistRepository import BlacklistRepository
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.InformacoesRepository import InformacoesRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils.Utils import get_path_from_file


async def setup_connection():
    # cria um banco de dados, apenas na ram, para executar os testes
    globals()['pgsql'] = testing.postgresql.Postgresql()
    # abre a conexão com o banco
    globals()['con'] = await ConnectionFactory.get_connection(globals()['pgsql'].dsn())

    # e vamos criar as tables, procedures e functions

    # primeiro, tem que pegar a localização do arquivo onde tem os creates
    path = get_path_from_file('database.pgsql', 'database/')
    with open(path, 'r') as file:
        # depois, abre o arquivo e executar o conteúdo no banco
        query_creates = file.read()
        await globals()['con'].execute(query_creates)


async def clone_connection():
    # fecha a conexão
    await globals()['con'].close()
    # e deleta a conexão e o banco
    del globals()['con']
    del globals()['pgsql']


class TestDb(Test):
    pass


# Classe que vai testar o CRUD (Create Read Update Delete) da table Blacklist
class CRUDBlacklist(TestDb):
    def __init__(self):
        self.repository = BlacklistRepository()
        self.con = globals()['con']

    async def test_1_blacklist_add(self):
        result = await self.repository.create(self.con, 999888, 'motivo teste')
        self.assert_true(result)

    async def test_2_blacklist_duplicate_value(self):
        try:
            await self.repository.create(self.con, 999888, 'motivo teste')
        except Exception as error:
            self.assert_is_instance(error, DuplicateBlacklist)

    async def test_3_blacklist_get(self):
        result = await self.repository.get_pessoa(self.con, 999888)
        self.assert_in(True, result)
        self.assert_in('motivo teste', result)
        self.assert_not_in(None, result)
        self.assert_not_in(False, result)

    async def test_4_blacklist_get_fail(self):
        result = await self.repository.get_pessoa(self.con, 999887)
        self.assert_in(None, result)
        self.assert_in(False, result)

    async def test_5_blacklist_delete(self):
        result = await self.repository.delete(self.con, 999888)
        self.assert_true(result)

    async def test_6_blacklist_delete_confirm(self):
        await self.test_4_blacklist_get_fail()


# Classe que vai testar o CRUD (Create Read Update Delete) da table ComandoDesativado
class CRUDComandoDesativado(TestDb):
    def __init__(self):
        self.repository = ComandoDesativadoRepository()
        self.servidor = Servidor(999888, 'prefixo teste')
        self.con = globals()['con']

    async def test_1_comando_desativado_add(self):
        await ServidorRepository().create(self.con, self.servidor)
        cd = ComandoDesativado(self.servidor, 'comando desativado teste')
        result = await self.repository.create(self.con, cd)
        self.assert_true(result)

    async def test_2_comando_desativado_duplicate_value(self):
        try:
            cd = ComandoDesativado(self.servidor, 'comando desativado teste')
            await self.repository.create(self.con, cd)
        except Exception as error:
            self.assert_is_instance(error, DuplicateComandoDesativado)

    async def test_3_comando_desativado_get(self):
        results = await self.repository.get_commands(self.con, self.servidor)
        self.assert_equal(len(results), 1)
        result = results[0]
        self.assert_equal(result.servidor, self.servidor)
        self.assert_equal(result.comando, 'comando desativado teste')

    async def test_4_comando_desativado_get_fail(self):
        s = Servidor(1, '1')
        results = await self.repository.get_commands(self.con, s)
        self.assert_equal(len(results), 0)

    async def test_5_comando_desativado_delete(self):
        cd = (await self.repository.get_commands(self.con, self.servidor))[0]
        result = await self.repository.delete(self.con, cd)
        self.assert_true(result)

    async def test_6_comando_desativado_delete_confirm(self):
        results = await self.repository.get_commands(self.con, self.servidor)
        self.assert_equal(len(results), 0)


# Classe que vai testar o CRUD (Create Read Update Delete) da table ComandoPersonalizado
class CRUDComandoPersonalizado(TestDb):
    def __init__(self):
        self.repository = ComandoPersonalizadoRepository()
        self.servidor = Servidor(123, 'prefixo teste')
        self.con = globals()['con']

    async def test_01_comando_personalizado_add(self):
        await ServidorRepository().create(self.con, self.servidor)
        cp = ComandoPersonalizado(self.servidor, 'comando desativado teste', 'resposta do comando teste', False)
        result = await self.repository.create(self.con, cp)
        self.assert_true(result)

    async def test_02_comando_personalizado_duplicate_value(self):
        try:
            cp = ComandoPersonalizado(self.servidor, 'comando desativado teste', 'resposta do comando teste', False)
            await self.repository.create(self.con, cp)
        except Exception as error:
            self.assert_is_instance(error, DuplicateComandoPersonalizado)

    async def test_03_comando_personalizado_get(self):
        results = await self.repository.get_commands(self.con, self.servidor)
        self.assert_equal(len(results), 1)
        result = results[0]
        self.assert_equal(result.servidor, self.servidor)
        self.assert_equal(result.comando, 'comando desativado teste')
        self.assert_equal(result.resposta, 'resposta do comando teste')
        self.assert_false(result.in_text)

    async def test_04_comando_personalizado_get_fail(self):
        s = Servidor(1, '1')
        results = await self.repository.get_commands(self.con, s)
        self.assert_equal(len(results), 0)

    async def test_05_comando_personalizado_update(self):
        cp = (await self.repository.get_commands(self.con, self.servidor))[0]
        cp.resposta = 'resposta do comando teste update'
        cp.in_text = True
        result = await self.repository.update(self.con, cp)
        self.assert_true(result)

    async def test_06_comando_personalizado_update_confirm(self):
        results = await self.repository.get_commands(self.con, self.servidor)
        self.assert_equal(len(results), 1)
        result = results[0]
        self.assert_equal(result.servidor, self.servidor)
        self.assert_equal(result.comando, 'comando desativado teste')
        self.assert_equal(result.resposta, 'resposta do comando teste update')
        self.assert_true(result.in_text)

    async def test_07_comando_personalizado_delete(self):
        cp = (await self.repository.get_commands(self.con, self.servidor))[0]
        result = await self.repository.delete(self.con, cp)
        self.assert_true(result)

    async def test_08_comando_personalizado_delete_confirm(self):
        results = await self.repository.get_commands(self.con, self.servidor)
        self.assert_equal(len(results), 0)

    async def test_09_comando_personalizado_update(self):
        cp = ComandoPersonalizado(self.servidor, 'comando desativado teste 2', 'resposta do comando teste 2', True)
        result = await self.repository.update(self.con, cp)
        self.assert_true(result)

    async def test_10_comando_personalizado_delete(self):
        await self.test_07_comando_personalizado_delete()


# Classe que vai testar o CRUD (Create Read Update Delete) da table Informacoes
class CRUDInformacoes(TestDb):
    def __init__(self):
        self.repository = InformacoesRepository()
        self.con = globals()['con']

    async def test_1_informacao_add(self):
        result = await self.repository.create(self.con, 'Informação teste', 'Dado da informação teste')
        self.assert_true(result)

    async def test_2_informacao_duplicate_value(self):
        result = await self.repository.create(self.con, 'Informação teste', 'Dado da informação teste')
        self.assert_false(result)

    async def test_3_informacao_get(self):
        result = await self.repository.get_dado(self.con, 'Informação teste')
        self.assert_equal(result, 'Dado da informação teste')

    async def test_4_informacao_get_fail(self):
        result = await self.repository.get_dado(self.con, 'Sem informação teste')
        self.assert_is_none(result)

    async def test_5_informacao_update(self):
        result = await self.repository.update(self.con, 'Informação teste', 'Dado da informação teste update')
        self.assert_true(result)

    async def test_6_informacao_update_confirm(self):
        result = await self.repository.get_dado(self.con, 'Informação teste')
        self.assert_equal(result, 'Dado da informação teste update')

    async def test_7_informacao_delete(self):
        result = await self.repository.delete(self.con, 'Informação teste')
        self.assert_true(result)

    async def test_8_informacao_delete_confirm(self):
        result = await self.repository.get_dado(self.con, 'Informação teste')
        self.assert_is_none(result)


# Classe que vai testar o CRUD (Create Read Update Delete) da table Servidor
class CRUDServidor(TestDb):
    def __init__(self):
        self.repository = ServidorRepository()
        self.con = globals()['con']

    async def test_01_servidor_add(self):
        await self.repository.delete(self.con, Servidor(999888, 'a'))
        s = Servidor(999888, 'prefixo qualquer')
        result = await self.repository.create(self.con, s)
        self.assert_true(result)

    async def test_02_servidor_duplicate_value(self):
        try:
            s = Servidor(999888, 'prefixo qualquer')
            await self.repository.create(self.con, s)
        except Exception as error:
            self.assert_is_instance(error, DuplicateServidor)

    async def test_03_servidor_get(self):
        result = await self.repository.get_servidor(self.con, 999888)
        self.assert_is_not_none(result)
        self.assert_equal(result.id, 999888)
        self.assert_equal(result.prefixo, 'prefixo qualquer')
        self.assert_true(result.sugestao_de_comando)

    async def test_04_servidor_get_fail(self):
        result = await self.repository.get_servidor(self.con, 987654321)
        self.assert_is_none(result)

    async def test_05_servidor_update(self):
        s = await self.repository.get_servidor(self.con, 999888)
        s.prefixo = 'prefixo qualquer update'
        s.channel_id_log = 123
        s.sugestao_de_comando = False
        result = await self.repository.update(self.con, s)
        self.assert_true(result)

    async def test_06_servidor_update_confirm(self):
        result = await self.repository.get_servidor(self.con, 999888)
        self.assert_is_not_none(result)
        self.assert_equal(result.id, 999888)
        self.assert_equal(result.prefixo, 'prefixo qualquer update')
        self.assert_equal(result.channel_id_log, 123)
        self.assert_false(result.sugestao_de_comando)

    async def test_07_servidor_delete(self):
        s = await self.repository.get_servidor(self.con, 999888)
        result = await self.repository.delete(self.con, s)
        self.assert_true(result)

    async def test_08_servidor_delete_confirm(self):
        result = await self.repository.get_servidor(self.con, 999888)
        self.assert_is_none(result)

    async def test_09_servidor_update(self):
        s = Servidor(999888, 'prefixo qualquer 2')
        result = await self.repository.update(self.con, s)
        self.assert_true(result)

    async def test_10_servidor_delete(self):
        await self.test_07_servidor_delete()


async def tests_db():
    # inicia e abre a conexão com o banco fake
    await setup_connection()
    result_obj = await executar_testes(TestDb)
    # e fecha o banco
    await clone_connection()
    # e se o teste foi iniciado por este arquivo
    if __name__ == '__main__':
        # se o resultado for True
        if result_obj.result:
            print(f'Todos os {len(result_obj.tests)} testes foram executados com sucesso em'
                  f' {result_obj.execution_time} !')
        else:
            for erro in result_obj.erros:
                print(erro)
    # return para saber dos resultados de outro lugar
    return result_obj


if __name__ == '__main__':
    # iniciando o teste de forma async
    asyncio.get_event_loop().run_until_complete(tests_db())
