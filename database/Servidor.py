# coding=utf-8
# Androxus bot
# Servidor.py

__author__ = 'Rafael'

from utils.Utils import get_configs


class Servidor:
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

    def __init__(self,
                 id,
                 prefix=None,
                 channelIdLog=None,
                 mensagemDeletada=False,
                 mensagemEditada=False,
                 avatarAlterado=False,
                 nomeAlterado=False,
                 tagAlterado=False,
                 nickAlterado=False,
                 roleAlterado=False,
                 sugestaoDeComando=True):
        self.id = id
        self.prefixo = prefix or get_configs()['default_prefix']
        self.channel_id_log = channelIdLog
        self.mensagem_deletada = mensagemDeletada
        self.mensagem_editada = mensagemEditada
        self.avatar_alterado = avatarAlterado
        self.nome_alterado = nomeAlterado
        self.tag_alterado = tagAlterado
        self.nick_alterado = nickAlterado
        self.role_alterado = roleAlterado
        self.sugestao_de_comando = sugestaoDeComando
