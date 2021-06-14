# -*- coding: utf-8 -*-
# Androxus bot
# main.py

__author__ = 'Rafael'

from os import environ

from colorama import init

from Classes.General import Androxus

if __name__ == '__main__':
    init()
    bot = Androxus()
    token = environ.get('TOKEN') if bot.configs.token == 'token_bot' else bot.configs.token
    bot.run(token)
