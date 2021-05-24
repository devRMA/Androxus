# -*- coding: utf-8 -*-
# Androxus bot
# Servidor.py

__author__ = 'Rafael'

try:
    from utils.Utils import get_configs
except ImportError:
    pass


class Servidor:
    __slots__ = ('id', 'prefixo', 'channel_id_log', 'mensagem_deletada', 'mensagem_editada',
                 'avatar_alterado', 'nome_alterado', 'tag_alterado', 'nick_alterado',
                 'role_alterado', 'sugestao_de_comando', 'lang')
    id: int
    prefixo: str
    channel_id_log: int
    mensagem_deletada: bool
    mensagem_editada: bool
    avatar_alterado: bool
    nome_alterado: bool
    tag_alterado: bool
    nick_alterado: bool
    role_alterado: bool
    sugestao_de_comando: bool
    lang: str

    def __init__(self, id_, prefix=None, channel_id_log=None, mensagem_deletada=False,
                 mensagem_editada=False, avatar_alterado=False, nome_alterado=False,
                 tag_alterado=False, nick_alterado=False, role_alterado=False,
                 sugestao_de_comando=True, lang='en_us'):
        self.id = id_
        self.prefixo = prefix
        self.channel_id_log = channel_id_log
        self.mensagem_deletada = mensagem_deletada
        self.mensagem_editada = mensagem_editada
        self.avatar_alterado = avatar_alterado
        self.nome_alterado = nome_alterado
        self.tag_alterado = tag_alterado
        self.nick_alterado = nick_alterado
        self.role_alterado = role_alterado
        self.sugestao_de_comando = sugestao_de_comando
        self.lang = lang
