# coding=utf-8
# Androxus bot
# Utils.py

__author__ = 'Rafael'


def pegar_o_prefixo(bot, message):
    from discord.dao.ServidorDao import ServidorDao
    if message.guild:
        prefixo = ServidorDao().get_prefix(message.guild.id)[0]
        if prefixo != None:
            return prefixo
    return '--'


def random_color():
    from random import randint
    r = lambda: randint(0, 255)
    return int(f'0x{r():02x}{r():02x}{r():02x}', 16)
