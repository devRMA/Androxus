# -*- coding: utf-8 -*-
# Androxus bot
# erros.py

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
