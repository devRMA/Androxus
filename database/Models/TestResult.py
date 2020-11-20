# -*- coding: utf-8 -*-
# Androxus bot
# TestResult.py

__author__ = 'Rafael'

from stopwatch import Stopwatch


class TestResult:
    erros: list
    tests: list
    execution_time: Stopwatch
    result: bool

    def __init__(self, erros, tests, execution_time):
        """

        Args:
            erros (list): Lista de string, com todos os erros que deram
            tests (list): Lista de string, com todos os testes realizados
            execution_time (Stopwatch): O stopwatch com o tempo de execução dos testes

        """
        deu_erro = len(erros) != 0
        self.result = False if deu_erro else True
        self.erros = erros
        self.tests = tests
        self.execution_time = execution_time

    def __repr__(self):
        return '< deu_erro={0.deu_erro} result={0.result} erros={0.erros} tests={0.tests} ' \
               'execution_time={0.execution_time.duration} >'.format(self)

    def __str__(self):
        if self.result:
            return f'{len(self.tests)} teste realizados com sucesso em {self.execution_time}!'
        return f'{len(self.erros)} erro(s) na hora de executar o teste!'
