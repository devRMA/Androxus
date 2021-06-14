# -*- coding: utf-8 -*-
# Androxus bot
# Erros.py

__author__ = 'Rafael'


class InvalidArgument(Exception):
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
        self.args = args
        self.kwargs = kwargs


class DuplicateBlacklist(Exception):
    pass


class DuplicateComandoDesativado(Exception):
    pass


class ComandoDesativadoNotFound(Exception):
    pass


class DuplicateComandoPersonalizado(Exception):
    pass


class DuplicateServidor(Exception):
    pass


class MultipleResults(Exception):
    results: list

    def __init__(self, results):
        self.results = results


class Stop(Exception):
    """
    Classe usada para parar laços de repetição
    """
