# -*- coding: utf-8 -*-
# Androxus bot
# Languages.py

__author__ = 'Rafael'

from abc import ABCMeta
from json import load
from os import walk
from typing import List, Union, Dict

from colorama import Fore, Style


class Language(metaclass=ABCMeta):
    __slots__ = ('display_name', 'name', 'aliases', 'erros', 'help', 'others', 'commands')
    display_name: str
    name: str
    aliases: List[str]
    erros: Dict[str, Union[dict, list]]
    help: Dict[str, Union[dict, list]]
    others: Dict[str, Union[dict, list]]
    commands: Dict[str, Union[dict, list]]

    def __init__(self):
        self.commands = {}
        self.erros = {}
        self.others = {}
        self.help = {}
        for path, _, files in walk(f'json/languages/{self.name}'):
            for filename in files:
                if filename.endswith('.json'):
                    full_path = f'{path}/{filename}'
                    filename = filename.removesuffix('.json')
                else:
                    continue
                with open(full_path, encoding='utf-8') as file:
                    json_loaded = load(file)
                if path.endswith('commands'):
                    self.commands[filename] = json_loaded
                elif path.endswith('erros'):
                    self.erros[filename] = json_loaded
                elif path.endswith('others'):
                    self.others[filename] = json_loaded
                elif path.endswith('help'):
                    self.help[filename] = json_loaded
        print(f'{Style.BRIGHT}{Fore.GREEN}[LANGUAGE  LOADED]' +
              f'{Fore.LIGHTMAGENTA_EX}{self.display_name}{Style.RESET_ALL}'.rjust(50))

    def get_translations(self, *, command=None, erro=None, help_=None, others=None):
        mode = 'commands'
        file = command
        if erro:
            mode = 'erros'
            file = erro
        elif help_:
            mode = 'help'
            file = help_
        elif others:
            mode = 'others'
            file = others
        dicts = getattr(self, mode)
        return dicts.get(file)


class Portuguese(Language):
    """ Classe base para o português """


class English(Language):
    """ Classe base para o inglês """


class Brazilian(Portuguese):
    def __init__(self):
        self.display_name = 'Português Brasileiro'
        self.name = 'pt_br'
        self.aliases = ['pt-br', 'português_br', 'portugues_br',
                        'portugues_brasileiro', 'português_brasileiro',
                        'pt_brasileiro', 'português-br', 'portugues-br',
                        'portugues-brasileiro', 'português-brasileiro',
                        'pt-brasileiro']
        super().__init__()


class USA(English):
    def __init__(self):
        self.display_name = 'English United States of America'
        self.name = 'en_us'
        self.aliases = ['en-us', 'en_usa', 'en-usa', 'english_united_states_of_america',
                        'english-united-states-of-america', 'english_usa', 'english-usa',
                        'english-us', 'english-us']
        super().__init__()


class Translations:
    __slots__ = ('all_languages', 'pt_br', 'en_us', 'supported_languages')
    all_languages: Dict[str, Language]
    pt_br: Brazilian
    en_us: USA
    supported_languages: List[Language]

    def __init__(self):
        self.pt_br = Brazilian()
        self.en_us = USA()
        self.supported_languages = [self.pt_br, self.en_us]
        self.all_languages = {
            'pt_br': self.pt_br,
            'en_us': self.en_us
        }
        for alias in self.pt_br.aliases:
            self.all_languages[alias] = self.pt_br
        for alias in self.en_us.aliases:
            self.all_languages[alias] = self.en_us

    def get(self, key):
        return self.all_languages.get(key)
