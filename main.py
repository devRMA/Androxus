# -*- coding: utf-8 -*-
# Androxus bot
# main.py

__author__ = 'Rafael'

from os import environ

from Classes.Androxus import Androxus

if __name__ == '__main__':
    bot = Androxus()
    token = environ.get('TOKEN') if bot.configs['token'] == 'token_bot' else bot.configs['token']
    bot.run(token)
