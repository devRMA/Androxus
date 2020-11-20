# -*- coding: utf-8 -*-
# Androxus bot
# Test.py

__author__ = 'Rafael'

from inspect import iscoroutinefunction
from traceback import format_exc

from stopwatch import Stopwatch

from database.Models.TestResult import TestResult


class Test:
    # classe que vai ser usada para listar todas as classes de teste
    @staticmethod
    def assert_equal(a, b):
        assert a == b

    @staticmethod
    def assert_not_equal(a, b):
        assert a != b

    @staticmethod
    def assert_true(x):
        assert x is True

    @staticmethod
    def assert_false(x):
        assert x is False

    @staticmethod
    def assert_is(a, b):
        assert a is b

    @staticmethod
    def assert_is_not(a, b):
        assert a is not b

    @staticmethod
    def assert_is_none(x):
        assert x is None

    @staticmethod
    def assert_is_not_none(x):
        assert x is not None

    @staticmethod
    def assert_in(a, b):
        assert a in b

    @staticmethod
    def assert_not_in(a, b):
        assert a not in b

    @staticmethod
    def assert_is_instance(a, b):
        assert isinstance(a, b)

    @staticmethod
    def assert_not_is_instance(a, b):
        assert not isinstance(a, b)


async def executar_testes(class_base):
    """

    Args:
        class_base (class): A classe de teste, que vai ser executada

    Returns:

    """
    erros = []
    # começa a contar o tempo de execução dos testes
    stopwatch = Stopwatch()
    all_tests = []
    # Pega todas as classes que herdam da classe base
    for test_class in class_base.__subclasses__():
        # e vai pegar todos os métodos que começam com "test_"
        tests = sorted(func for func in dir(test_class) if func.startswith('test_'))
        # armazena quantos testes tem
        all_tests += tests
        # cria o objeto da classe
        obj = test_class()
        for test in tests:
            try:
                method = obj.__getattribute__(test)
                if iscoroutinefunction(method):
                    await method()
                else:
                    method()
            except:
                # se der erro, vamos salvar o erro na lista "erros" e parar os testes dessa classe
                erros.append('=' * 35 +
                             '\n'
                             f'Erro in {test_class.__name__}.{test}\n{format_exc()}')
                break
    # para de contar o tempo de execução
    stopwatch.stop()
    return TestResult(erros=erros, tests=all_tests, execution_time=stopwatch)
