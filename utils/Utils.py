# coding=utf-8
# Androxus bot
# Utils.py

__author__ = 'Rafael'

import datetime
from re import sub
from typing import List


def pegar_o_prefixo(bot, message, open_con=True, conn=None) -> str:
    """
    :param bot: Pode passar None, esse parâmetro não é usado
    :param message: A mensagem que quer saber o prefixo do bot
    :param open_con: Parâmetro que servir como flag, para saber se é ou não para abrir uma conexão nova
    :param conn: Conexão com o banco, caso o "open_con" esteja como False
    :type bot: discord.ext.commands.Bot
    :type message: discord.Message
    :type open_con: bool
    :type conn: Conexao
    :return: o prefixo do bot, para está mensagem
    :rtype: str
    """
    # pega a classe que mexe com a table dos servidores
    from database.Repositories.ServidorRepository import ServidorRepository
    # classe servidor em si
    from database.Servidor import Servidor
    # classe que vai abrir a conexão com o banco
    from database.Conexao import Conexao
    # função que vai ler as informações do json
    from utils.Utils import get_configs
    if message.guild:  # se a mensagem tiver um servidor, é porque ela não foi enviada no privado
        if open_con:  # se for para abrir a conexão:
            conexao = Conexao()
        else:  # se não for, vai pegar a conexão que for passada
            conexao = conn
        # vai no banco de dados, e faz um select para ver qual o prefixo
        servidor = ServidorRepository().get_servidor(conexao, message.guild.id)
        prefixo = None
        if servidor:
            prefixo = servidor.prefixo
        if prefixo is not None:  # se achou um prefixo, retorna o que achou
            if open_con:  # se a conexão foi aberta aqui, vai ser fechada
                conexao.fechar()
            return prefixo
        if servidor is None:  # se o banco disse que não tem esse servidor cadastrado, vai criar um
            servidor = Servidor(message.guild.id)  # vai criar um objeto Servidor
            ServidorRepository().create(conexao, servidor)  # e vai mandar ele para o banco
            if open_con:  # se a conexão foi aberta aqui, vai ser fechada
                conexao.fechar()
            # se acabou de criar o registro, o prefixo vai ser o padrão
            return get_configs()['default_prefix']
    return ''  # se a mensagem foi enviado no privado, não vai ter prefixo


def random_color() -> hex:
    """
    :return: uma cor "aleatoria" em hexadecimal
    :rtype: hex
    """
    from random import randint  # função que pega números aleatórios
    r = lambda: randint(0, 255)  # lambda que vai pegar os números
    # vai escolher os números, e depois transformar em hexadecimal 0x000000
    return int(f'0x{r():02x}{r():02x}{r():02x}', 16)


def get_emoji_dance() -> str:
    """
    :return: um emoji de dança aleatório
    :rtype: str
    """
    from random import choice
    # lista com os emojis
    emojis = [c[-1] for c in get_configs()['emojis']['dances'].items()]
    return choice(emojis)  # retorna o emoji escolhido da lista


def get_last_update() -> datetime.datetime:
    """
    :return: vai retornar o datetime do último commit que teve no github
    :rtype: datetime.datetime
    """
    # função que vai pegar o último update que o bot teve
    # como o bot está no github, a ultima atualização que teve no github, vai ser a ultima atualização do bot
    from requests import get  # função que vai pegar o html da página
    from json import loads  # função que vai converter de json pra dicionario
    from datetime import datetime  # como vai vim uma str do site, vamos converter para um objeto datetime
    url = 'https://api.github.com/repositories/294764564'  # url do repositório do bot
    html = get(url).text  # vai pegar o texto da página
    json = loads(html)  # transformar de json para dicionario
    data_do_update = json['updated_at']  # aqui, ainda vai estar como string
    # esse é um exemplo de como vai chegar a string: 2020-09-19T04:37:37Z
    # da para observer que a formatação é: ano-mes-diaThora:minuto:segundoZ
    data_do_update = datetime.strptime(data_do_update, '%Y-%m-%dT%H:%M:%SZ')  # conversão de string para datetime
    return data_do_update  # retorna o objeto datetime


def get_last_commit() -> str:
    """
    :return: vai retornar a mensagem do último commit que teve no github do bot
    :rtype: str
    """
    # função que vai pegar o último commit do github do bot
    from requests import get  # função que vai pegar o html da página
    from json import loads  # função que vai converter de json pra dicionario
    url = 'https://api.github.com/repositories/294764564/commits'  # url onde ficam todos os commits do bot
    html = get(url).text  # vai pegar o texto da página
    json = loads(html)  # transformar de json para dicionario
    return json[0]['commit']['message']  # vai pegar o último commit que teve, e retornar a mensagem


def get_configs() -> dict:
    """
    :return: vai retornar um dicionário com as configurações do arquivo configs.json
    :rtype: dict
    """
    from json import load  # função que vai transformar de json para dict e vice versa
    from os.path import exists  # função que vai verificar se existe o arquivo json
    path = None  # Se não entrar em nenhum if, vai continuar como None
    # lista de possiveis paths do configs.json
    paths = [
        'discord_bot/',
        './',
        '../',
        '../../',
        '../../../',
        '../../../../'
    ]
    # laço que vai verificar em qual path está o configs.json
    for c in paths:
        if exists(f'{c}configs.json'):
            path = f'{c}configs.json'  # se achar, salva o path
            break
    if path:
        with open(path) as file:
            configs = load(file)
        return configs
    else:
        exit('Não achei o arquivo de configurações!\nBaixe o arquivo configs.json!\nhttps://github.com/devRMA/Androxus')


def capitalize(string) -> str:
    """
    :param string: string que vai ser formatada
    :type string: str
    :return: vai deixar apenas a primeira letra em maiúscula da string
    :rtype: str
    """
    from string import ascii_lowercase
    # aqui, vamos pegar o alfabeto em minusculo e adicionar alguma letras com acentuação, que têm maiusculo
    ascii_lowercase += 'éŕýúíóṕḉĺḱj́ǵśáźçǘńḿẁỳùìòàǜǹm̀ẽỹũĩõãṽñŵêŷûîôâŝĝĥĵẑĉ'
    if string == '':
        return ''
    new_string = ''
    foi = False
    for char in string:
        if (char.lower() in ascii_lowercase) and (not foi):
            new_string += char.upper()
            foi = True
        else:
            new_string += char.lower()
    return new_string


def datetime_format(date1, date2=None) -> str:
    """
    :param date1: objeto datetime que vai ser subtraido pelo date2
    :param date2: Parâmetro opcional, se não for passado nada, vai pegar o datetime utc atual
    :type date1: datetime utc
    :type date2: datetime utc
    :return: vai retornar a string formatada, da diferença da date2 pela date1
    :rtype: str
    """
    from dateutil.relativedelta import relativedelta
    from datetime import datetime
    if date2 is None:
        date2 = datetime.utcnow()
    time = relativedelta(date2, date1)
    years = abs(time.years)
    months = abs(time.months)
    days = abs(time.days)
    hours = abs(time.hours)
    minutes = abs(time.minutes)
    seconds = abs(time.seconds)
    """
        variável que vai controlar quantos dados já foram mostrados
        para evitar que a string saia muito grande, como:
        2 anos, 5 meses, 1 dia, 2 horas, 3 minutos e 2 segundos.
        com a variável limitando, vai sair assim:
        2 anos, 5 meses e 1 dia.
    """
    dados = 0
    dt_str = ''
    if (years == 0) and (months == 0) and (days <= 1):
        if days == 0:
            d_str = 'Hoje'
        elif days == 1:
            d_str = 'Ontem'
        else:
            d_str = ''
        if hours > 1:
            h_str = f'{hours} horas'
        elif hours == 1:
            h_str = f'{hours} hora'
        else:
            h_str = ''
        if minutes > 1:
            m_str = f'{minutes} minutos'
        elif minutes == 1:
            m_str = f'{minutes} minuto'
        else:
            m_str = ''
        if seconds > 1:
            s_str = f'{seconds} segundos'
        elif seconds == 1:
            s_str = f'{seconds} segundo'
        else:
            s_str = ''
        if h_str and m_str and s_str:
            dt_str = f'{d_str} há {h_str}, {m_str} e {s_str}.'
        elif h_str and m_str:
            dt_str = f'{d_str} há {h_str} e {m_str}.'
        elif h_str and s_str:
            dt_str = f'{d_str} há {h_str} e {s_str}.'
        elif m_str and s_str:
            dt_str = f'{d_str} há {m_str} e {s_str}.'
        elif h_str:
            dt_str = f'{d_str} há {h_str}.'
        elif m_str:
            dt_str = f'{d_str} há {m_str}.'
        elif s_str:
            dt_str = f'{d_str} há {s_str}.'
        elif (h_str == '') and (m_str == '') and (s_str == ''):
            dt_str = f'{d_str}.'
        return dt_str
    if years > 1:
        dt_str += f'{years} anos'
        dados += 1
    elif years == 1:
        dt_str += f'{years} ano'
        dados += 1
    if months > 1:
        if years >= 1:
            dt_str += ', '
        dt_str += f'{months} meses'
        dados += 1
    elif months == 1:
        if years >= 1:
            dt_str += ', '
        dt_str += f'{months} mês'
        dados += 1
    if days > 1:
        if (years >= 1) or (months >= 1):
            dt_str += ', '
        dt_str += f'{days} dias'
        dados += 1
    elif days == 1:
        if (years >= 1) or (months >= 1):
            dt_str += ', '
        dt_str += f'{days} dia'
        dados += 1
    if dados < 3:
        if hours > 1:
            if (years >= 1) or (months >= 1) or (days >= 1):
                dt_str += ', '
            dt_str += f'{hours} horas'
            dados += 1
        elif hours == 1:
            if (years >= 1) or (months >= 1) or (days >= 1):
                dt_str += ', '
            dt_str += f'{hours} hora'
            dados += 1
        if dados < 3:
            if minutes > 1:
                if (years >= 1) or (months >= 1) or (days >= 1) or (hours >= 1):
                    dt_str += ', '
                dt_str += f'{minutes} minutos'
                dados += 1
            elif minutes == 1:
                if (years >= 1) or (months >= 1) or (days >= 1) or (hours >= 1):
                    dt_str += ', '
                dt_str += f'{minutes} minuto'
                dados += 1
            if dados < 3:
                if seconds > 1:
                    if (years >= 1) or (months >= 1) or (days >= 1) or (hours >= 1) or (minutes >= 1):
                        dt_str += ', '
                    dt_str += f'{seconds} segundos'
                elif seconds == 1:
                    if (years >= 1) or (months >= 1) or (days >= 1) or (hours >= 1) or (minutes >= 1):
                        dt_str += ', '
                    dt_str += f'{seconds} segundo'
    dt_str += '.'
    if dt_str.rfind(',') != -1:
        dt_str = dt_str[:dt_str.rfind(',')] + ' e' + dt_str[dt_str.rfind(',') + 1:]
    return dt_str


def inverter_string(string) -> str:
    """
    :param string: a string que vai ser virada de cabeça para baixo
    :type string: str
    :return: a string de cabeça para baixo
    :rtype: str
    """
    letras = {
        'a': 'ɐ',
        'b': 'q',
        'c': 'ɔ',
        'd': 'p',
        'e': 'ǝ',
        'f': 'ɟ',
        'g': 'ƃ',
        'h': 'ɥ',
        'i': 'ı',
        'j': 'ɾ',
        'k': 'ʞ',
        'l': 'ן',
        'm': 'ɯ',
        'n': 'u',
        'o': 'o',
        'p': 'd',
        'q': 'b',
        'r': 'ɹ',
        's': 's',
        't': 'ʇ',
        'u': 'n',
        'v': 'ʌ',
        'w': 'ʍ',
        'x': 'x',
        'y': 'ʎ',
        'z': 'z',
        '?': '¿',
        '!': '¡',
        '&': '⅋',
        '(': ')',
        ')': '(',
        '_': '‾',
        "'": ',',
        '"': '„',
        '.': '˙',
        '>': '<',
        '<': '>',
        ',': "'",
        ':': ':',
        '[': ']',
        ']': '[',
        '{': '}',
        '}': '{'
    }
    string = string.lower()
    string_invertida = ''
    for c in string:
        encontrou = False
        for i in letras.items():
            if i[0] == c:
                encontrou = True
                string_invertida += i[-1]
                break
        if not encontrou:
            string_invertida += c
            encontrou = True
    return string_invertida[::-1]


def is_number(string) -> bool:
    """
    :param string: A string que vai ser verificada
    :type string: str
    :return: Vai retornar se a string pode ser convertida para float ou int
    :rtype: bool
    """
    from string import ascii_lowercase
    try:
        if string.find(',') != -1:
            # se a string vier assim: 2,2
            # vai converter para: 2.2
            string = string.replace(',', '.')
        # remove espaços
        string = string.replace(' ', '')
        # a função isalpha verifica se a string é inteiramente de leras
        if string.isalpha():
            return False
        # aqui vai verificar se tem alguma letra no meio dos números
        for char in ascii_lowercase:
            if char in string.lower():
                return False
        float(string)
        return True
    except ValueError:
        return False


def convert_to_bool(argument: str) -> bool or None:
    """
    :param argument: A string que vai ser convertida para bool
    :type argument: str
    :return: Vai retornar o boolean correspondente a string passada
    :rtype: bool or None
    """
    lowered = argument.lower()
    strings_true = ('sim', 'yes', 'true', '1', 'ativo', 'on')
    strings_false = ('não', 'nao', 'no', 'false', '0', 'desativo', 'off')
    for string in strings_true:
        if string.startswith(lowered):
            return True
    for string in strings_false:
        if string.startswith(lowered):
            return False
    return None


def convert_to_string(argument: bool or None) -> str:
    """
    :param argument: O bool que vai ser convertido para string
    :type argument: bool or None
    :return: Vai retornar "sim" ou "não" ou "nulo" de acordo com o parâmetro
    :rtype: bool
    """
    if argument is None:
        return 'nulo'
    elif argument:
        return 'sim'
    else:
        return 'não'


def string_similarity(string1, string2) -> float:
    """
    :param string1: Primeira string que vai ser comparada
    :param string2: Segunda string que vai ser comparada
    :type string1: str
    :type string2: str
    :return: Vai retornar o quão similar, são as strings, podendo ir de 0.0 a 1.0
    :rtype: float
    """
    import jellyfish
    difference = jellyfish.levenshtein_distance(string1, string2)
    if difference == 0:
        return 1.0
    max_value = max([len(string1), len(string2)])
    result = 100 - ((100 * difference) / max_value)
    return result / 100


def get_most_similar_item(string: str, list_items: List[str]) -> str or None:
    """
    :param string: String que vai ser comparada com a lista
    :param list_items: Uma lista de strings que vão ser comparadas com a primeira string
    :type string: str
    :type list_items: List[str]
    :return: Vai retornar o item da lista mais parecido com a string do parâmetro
    :rtype: str or None
    """
    # lista que vai guardar o item e o score mais alto que teve
    highest_score = [0.0, '']
    for item in list_items:
        # vai pegar o quão similar a string é do item
        similatity = string_similarity(string, item)
        # se a similaridade for maior do que a registrada
        # vai atualizar
        if similatity > highest_score[0]:
            highest_score[0] = similatity
            highest_score[-1] = item
    # se algum item ser pelo menos 50% parecido com a string, vai retornar ele
    if highest_score[0] >= 0.5:
        return highest_score[-1]
    # caso contrario, não retorna nada
    return None


def get_most_similar_items(string: str, list_items: List[str]) -> list:
    """
    :param string: String que vai ser comparada com a lista
    :param list_items: Uma lista de strings que vão ser comparadas com a primeira string
    :type string: str
    :type list_items: List[str]
    :return: Vai retornar uma lista com os itens mais parecidos com a string base
    :rtype: list
    """
    list_items_cp = list_items.copy()
    ms = []
    for _ in list_items:
        most_similar = get_most_similar_item(string, list_items_cp)
        if most_similar is not None:
            list_items_cp.remove(most_similar)
            ms.append(most_similar)
        else:
            break
    return ms


def get_most_similar_items_with_similarity(string: str, list_items: List[str]) -> list:
    """
    :param string: String que vai ser comparada com a lista
    :param list_items: Uma lista de strings que vão ser comparadas com a primeira string
    :type string: str
    :type list_items: List[str]
    :return: Vai retornar uma lista com os itens mais parecidos com a string base e também qual o grau de similaridade
    :rtype: list
    """
    list_items_cp = list_items.copy()
    ms = []
    for c in range(len(list_items)):
        most_similar = get_most_similar_item(string, list_items_cp)
        if most_similar is not None:
            list_items_cp.remove(most_similar)
            ms.append([most_similar, string_similarity(string, most_similar)])
        else:
            break
    return ms


def difference_between_lists(list1: list, list2: list) -> list:
    """
    :param list1: Primeira lista
    :param list2: Segunda lista
    :type list1: list
    :type list2: list
    :return: Vai retornar uma lista, com os itens que não se repetiram nas listas
    :rtype: list
    """
    return list(set(list1) - set(list2)) + list(set(list2) - set(list1))


def prettify_number(number: not (not float and not int and not str), br: bool = True, truncate: bool = False) -> str:
    """
    :param truncate: Parâmetro que vai definir se é ou não para cortar as casas decimais
    :param number: O valor que vai ser deixado "bonito"
    :param br: Flag que vai ativar ou não o padrão br: "100.000,00". Se tiver desativado, vai sair assim "100,000.00"
    :return: A string com o número formatado
    :type number: float or int or str
    :type br: bool
    :type truncate: bool
    :rtype: str
    """
    # se a pessoa não passou um número
    if not is_number(str(number)):
        return number  # simplesmente não faz nada
    # se for para cortar as casas decimais:
    if truncate:
        number = sub(r'^(\d+\.\d{,2})\d*$', r'\1', str(number))
    # vai dividir a string onde tiver um ponto
    number = str(number).split('.')
    # se a lista tiver mais de 1 item, vai jogar o último item para a variável, se não tiver, fica com ''
    decimal = number[-1] if len(number) > 1 else ''
    # se o decimal for apenas zeros, vai cortar ele
    decimal = decimal if decimal.strip('0') else ''
    # e a variável 'number' vai ficar apenas com o primeiro item
    number = number[0]
    # o separador, se o parâmetro 'br' for True, vai ser '.' se ele estiver off, vai ser ','
    separator = '.' if br else ','
    # por padrão, o separador das casas decimais vai ser ''
    decimal_separator = ''
    # se veio algum decimal
    if decimal != '':
        # vai colocar ',' caso o 'br' esteja on, e '.' quando ele estiver off
        decimal_separator = ',' if br else '.'
    # depois, vai formatar os números
    number = f'{int(number):_}'.replace('_', separator)
    # depois, é só retornar a string com o número, o separador de casa decimal, e as casas decimais
    return f'{number}{decimal_separator}{decimal}'
