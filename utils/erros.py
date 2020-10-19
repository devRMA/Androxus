# coding=utf-8
# Androxus bot
# erros.py

__author__ = 'Rafael'


class InvalidArgument(Exception):
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
        self.args = args
        self.kwargs = kwargs
