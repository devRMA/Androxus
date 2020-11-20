# -*- coding: utf-8 -*-
# Androxus bot
# test.py

__author__ = 'Rafael'

import asyncio

from Classes.Test import Test, executar_testes
from utils.Utils import *


class TestUtils(Test):
    pass


class TestMain(TestUtils):

    def test_capitalize(self):
        self.assert_equal(capitalize(';;ABC'), ';;Abc')
        self.assert_equal(capitalize('´ABC'), '´Abc')
        self.assert_equal(capitalize('12345AB  __+=12llaksamC'), '12345Ab  __+=12llaksamc')
        self.assert_equal(capitalize('9Ç12Opa'), '9Ç12opa')
        self.assert_equal(capitalize('12É987G654U012A!'), '12É987g654u012a!')

    def test_datetime_format(self):
        self.assert_equal('Hoje há 2 horas, 1 minuto e 1 segundo.',
                          datetime_format(datetime(2020, 10, 21, 16, 43, 48), datetime(2020, 10, 21, 14, 42, 47)))
        self.assert_equal('Ontem há 20 minutos e 30 segundos.',
                          datetime_format(datetime(2020, 10, 21, 16, 43, 48), datetime(2020, 10, 20, 16, 23, 18)))
        self.assert_equal('1 mês, 11 dias e 5 horas.',
                          datetime_format(datetime(2020, 10, 21, 16, 43, 48), datetime(2020, 9, 10, 10, 59, 59)))
        self.assert_equal('Ontem há 6 horas.',
                          datetime_format(datetime(2020, 10, 20, 22, 43, 48), datetime(2020, 10, 21, 4, 43, 48)))
        self.assert_equal('12 anos, 9 meses e 18 dias.',
                          datetime_format(datetime(2008, 1, 2, 16, 49, 1), datetime(2020, 10, 21, 4, 43, 48)))

    def test_inverter_string(self):
        self.assert_equal('ɐdo', inverter_string('opa'))
        self.assert_equal('ɔqɐ4321ǝʇsǝʇ', inverter_string('teste1234abc'))
        self.assert_equal('ǝʇsǝʇṕóãçããá', inverter_string('áããçãóṕteste'))
        self.assert_equal('ǝnɹʇ', inverter_string('True'))
        self.assert_equal('1', inverter_string('1'))

    def test_is_number(self):
        self.assert_true(is_number('123'))
        self.assert_false(is_number('99999a'))
        self.assert_true(is_number('3.1415'))
        self.assert_false(is_number('3.1415a'))
        self.assert_false(is_number('teste'))

    def test_convert_to_bool(self):
        self.assert_true(convert_to_bool('SIm'))
        self.assert_true(convert_to_bool('sim'))
        self.assert_true(convert_to_bool('1'))
        self.assert_true(convert_to_bool('ye'))
        self.assert_true(convert_to_bool('aTIvo'))
        self.assert_true(convert_to_bool('aTIvo'))
        self.assert_true(convert_to_bool('on'))
        self.assert_is_none(convert_to_bool('yep'))
        self.assert_is_none(convert_to_bool('ava'))
        self.assert_is_none(convert_to_bool('teste'))
        self.assert_is_none(convert_to_bool('2'))
        self.assert_is_none(convert_to_bool('+-='))
        self.assert_false(convert_to_bool('não'))
        self.assert_false(convert_to_bool('nao'))
        self.assert_false(convert_to_bool('No'))
        self.assert_false(convert_to_bool('0'))
        self.assert_false(convert_to_bool('faLse'))
        self.assert_false(convert_to_bool('FALSE'))
        self.assert_false(convert_to_bool('desaTIvo'))
        self.assert_false(convert_to_bool('off'))

    def test_convert_to_string(self):
        self.assert_equal(convert_to_string(True), 'sim')
        self.assert_equal(convert_to_string(None), 'nulo')
        self.assert_equal(convert_to_string(False), 'não')

    def test_string_similarity(self):
        self.assert_equal(string_similarity('a', 'a'), 1.0)
        self.assert_equal(string_similarity('a', 'ab'), 0.8333333333333334)
        self.assert_equal(string_similarity('falei', 'falar'), 0.8133333333333334)
        self.assert_equal(string_similarity('falei', 'falar'), 0.8133333333333334)
        self.assert_equal(string_similarity('123', '456'), 0)

    def test_get_most_similar_item(self):
        self.assert_equal(get_most_similar_item('123', ['123', '234', '321', '679']), '123')
        self.assert_equal(get_most_similar_item('234', ['123', '234', '321', '679']), '234')
        self.assert_equal(get_most_similar_item('5679', ['1234', '2345', '3210', '5679']), '5679')
        self.assert_equal(get_most_similar_item('5679', ['1234', '2345', '3210', '5679']), '5679')
        self.assert_equal(get_most_similar_item('9234', ['1234', '2345', '3210', '5679']), '1234')

    def test_get_most_similar_items(self):
        self.assert_equal(get_most_similar_items('9234', ['1234', '2345', '3210', '5679']), ['1234', '2345', '3210'])
        self.assert_equal(get_most_similar_items('5678', ['1234', '2345', '3210', '5679']), ['5679'])
        self.assert_equal(get_most_similar_items('5678', ['1234', '2345', '3210', '5679']), ['5679'])
        self.assert_equal(get_most_similar_items('123', ['1234', '2345', '3210', '5679']), ['1234', '2345', '3210'])
        self.assert_equal(get_most_similar_items('9999', ['1234', '2345', '3210', '5679']), ['5679'])

    def test_get_most_similar_items_with_similarity(self):
        self.assert_equal(get_most_similar_items_with_similarity('5678', ['1234', '2345', '3210', '5679']),
                          [
                              ['5679', 0.8333333333333334]
                          ])
        self.assert_equal(get_most_similar_items_with_similarity('1243', ['1234', '2345', '3210', '5679']),
                          [
                              ['1234', 0.9166666666666666],
                              ['2345', 0.6666666666666666],
                              ['3210', 0.5]
                          ])
        self.assert_equal(get_most_similar_items_with_similarity('9234', ['1234', '2345', '3210', '5679']),
                          [
                              ['1234', 0.8333333333333334],
                              ['2345', 0.8333333333333334],
                              ['3210', 0.5]
                          ])
        self.assert_equal(get_most_similar_items_with_similarity('14', list(map(lambda x: str(x), range(0, 30, 2)))),
                          [
                              ['14', 1.0],
                              ['10', 0.6666666666666666],
                              ['12', 0.6666666666666666],
                              ['16', 0.6666666666666666],
                              ['18', 0.6666666666666666],
                              ['24', 0.6666666666666666]
                          ])
        self.assert_equal(get_most_similar_items_with_similarity('99', list(map(lambda x: str(x), range(0, 30, 2)))),
                          [])

    def test_difference_between_lists(self):
        self.assert_equal(difference_between_lists(list(range(0, 20)), list(range(0, 21))), [20])
        self.assert_equal(difference_between_lists(['a', 'b'], ['b', 'c']), ['a', 'c'])
        self.assert_equal(difference_between_lists('abc', 'cbd'), ['a', 'd'])

    def test_prettify_number(self):
        self.assert_equal(prettify_number(123), '123')
        self.assert_equal(prettify_number(1234), '1.234')
        self.assert_equal(prettify_number(123456), '123.456')
        self.assert_equal(prettify_number(123456, br=False), '123,456')
        self.assert_equal(prettify_number(123456.999, truncate=False), '123.456,999')
        self.assert_equal(prettify_number(123456.999, truncate=True), '123.456,99')
        self.assert_equal(prettify_number(123456.000000000001, truncate=True), '123.456')
        self.assert_equal(prettify_number(123456.01, truncate=True), '123.456,01')


async def test_utils():
    result_obj = await executar_testes(TestUtils)
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
    asyncio.get_event_loop().run_until_complete(test_utils())
