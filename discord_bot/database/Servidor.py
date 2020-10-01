# coding=utf-8
# Androxus bot
# Servidor.py

__author__ = 'Rafael'

from discord_bot.utils.Utils import get_configs


class Servidor:
    id: int
    prefix: str

    def __init__(self, id, prefix=None):
        self._id = id
        self._prefix = prefix or get_configs()['default_prefix']

    @property
    def id(self):
        return self._id

    @property
    def prefix(self):
        return self._prefix

    @id.setter
    def id(self, value):
        raise Exception('Não é possivel alterar o id depois de ter criado o objeto')

    @prefix.setter
    def prefix(self, value):
        self._prefix = value
