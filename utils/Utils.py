# -*- coding: utf-8 -*-
# Androxus bot
# Utils.py

__author__ = 'Rafael'

import datetime
import string as string_lib
from datetime import datetime
from functools import reduce
from glob import glob
from json import loads, load
from random import choice
from re import compile
from re import sub
from typing import List

from dateutil.relativedelta import relativedelta
from jellyfish import jaro_winkler_similarity
from requests import get

from database.Models.Servidor import Servidor
from database.Repositories.ServidorRepository import ServidorRepository


async def pegar_o_prefixo(bot, message):
    """

    Args:
        bot (Classes.Androxus.Androxus): Instância do bot
        message (discord.Message or discord.ext.commands.context.Context): A mensagem que quer saber o prefixo do bot

    Returns:
        str: o prefixo do bot, para está mensagem

    """
    if message.guild:  # se a mensagem tiver um servidor, é porque ela não foi enviada no privado
        # vai no banco de dados, e faz um select para ver qual o prefixo
        servidor = await ServidorRepository().get_servidor(bot.db_connection, message.guild.id)
        prefixo = None
        if servidor:
            prefixo = servidor.prefixo
        if prefixo is not None:  # se achou um prefixo, retorna o que achou
            return prefixo
        if servidor is None:  # se o banco disse que não tem esse servidor cadastrado, vai criar um
            servidor = Servidor(message.guild.id, get_configs()['default_prefix'])
            await ServidorRepository().create(bot.db_connection, servidor)
            # se acabou de criar o registro, o prefixo vai ser o padrão
            return get_configs()['default_prefix']
    return ''  # se a mensagem foi enviado no privado, não vai ter prefixo


def get_emoji_dance():
    """

    Returns:
        str: Um emoji de dança aleatório

    """
    # lista com os emojis
    emojis = [c[-1] for c in get_emojis_json()['dances'].items()]
    return choice(emojis)  # retorna o emoji escolhido da lista


def get_last_update():
    """

    Returns:
        datetime.datetime: O datetime do último commit que teve no github

    """
    # função que vai pegar o último update que o bot teve
    # como o bot está no github, a ultima atualização que teve no github, vai ser a ultima atualização do bot
    url = 'https://api.github.com/repositories/294764564/commits'  # url do repositório do bot
    html = get(url).text  # vai pegar o texto da página
    json = loads(html)  # transformar de json para dicionario
    data_do_update = json[0]['commit']['committer']['date']  # aqui, ainda vai estar como string
    # esse é um exemplo de como vai chegar a string: 2020-09-19T04:37:37Z
    # da para observer que a formatação é: ano-mes-diaThora:minuto:segundoZ
    data_do_update = datetime.strptime(data_do_update, '%Y-%m-%dT%H:%M:%SZ')  # conversão de string para datetime
    return data_do_update  # retorna o objeto datetime


def get_last_commit():
    """

    Returns:
        str: A mensagem do último commit que teve no github do bot

    """
    # função que vai pegar o último commit do github do bot
    url = 'https://api.github.com/repositories/294764564/commits'  # url onde ficam todos os commits do bot
    html = get(url).text  # vai pegar o texto da página
    json = loads(html)  # transformar de json para dicionario
    return json[0]['commit']['message']  # vai pegar o último commit que teve, e retornar a mensagem


def get_configs():
    """

    Returns:
        dict: Um dicionário com as configurações do arquivo configs.json

    """
    path = get_path_from_file('configs.json', 'json/')
    if path is not None:
        with open(path) as file:
            configs = load(file)
        return configs
    else:
        exit('Não achei o arquivo de configurações!\nBaixe o arquivo configs.json e coloque na pasta json!\n'
             'https://github.com/devRMA/Androxus')


def get_emojis_json():
    """

    Returns:
        dict: Um dicionário com os emojis emojis do emojis.json

    """
    path = get_path_from_file('emojis.json', 'json/')
    if path is not None:
        with open(path) as file:
            configs = load(file)
        return configs
    else:
        exit('Não achei o arquivo de configurações!\nBaixe o arquivo emojis.json e coloque na pasta json!\n'
             'https://github.com/devRMA/Androxus')


def capitalize(string):
    """

    Args:
        string (str): String que vai ser formatada

    Returns:
        str: Vai deixar apenas a primeira letra em maiúscula da string

    """
    # aqui, vamos pegar o alfabeto em minusculo e adicionar alguma letras com acentuação, que têm maiusculo
    char_lowercase = string_lib.ascii_lowercase
    char_lowercase += 'éŕýúíóṕḉĺḱj́ǵśáźçǘńḿẁỳùìòàǜǹm̀ẽỹũĩõãṽñŵêŷûîôâŝĝĥĵẑĉ'
    if string == '':
        return ''
    new_string = ''
    foi = False
    for char in string:
        if (char.lower() in char_lowercase) and (not foi):
            new_string += char.upper()
            foi = True
        else:
            new_string += char.lower()
    return new_string


def datetime_format(date1, date2=None):
    """

    Args:
        date1 (datetime.datetime): Objeto datetime que vai ser subtraido pelo date2
        date2 (datetime.datetime): Parâmetro opcional, se não for passado, vai pegar o datetime utc atual (Default value = None)

    Returns:
        str: A string formatada, da diferença da date2 pela date1

    """
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
        if date1.day == date2.day:
            d_str = 'Hoje'
        elif (days == 1) or (abs(date2.day - date1.day) == 1):
            d_str = 'Ontem'
        elif days == 0:
            d_str = 'Hoje'
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


def inverter_string(string):
    """

    Args:
        string (str): A string que vai ser virada de cabeça para baixo

    Returns:
        str: A string de cabeça para baixo

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


def is_number(string):
    """

    Args:
        string (str): A string que vai ser verificada

    Returns:
        bool: Vai retornar se a string pode ser convertida para float ou int

    """
    if len(string) == 0:
        return False
    if not isinstance(string, str):
        string = str(string)
    if string.isdecimal() or string.isnumeric():
        return True
    try:
        float(string)
        return True
    except ValueError:
        try:
            float(string.replace(',', '.'))
        except ValueError:
            return False


def convert_to_bool(argument):
    """

    Args:
        argument (str): A string que vai ser convertida para bool

    Returns:
        bool or None: Vai retornar o boolean correspondente a string passada

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


def convert_to_string(argument):
    """

    Args:
        argument (bool or None): O bool que vai ser convertido para string

    Returns:
        str: Vai retornar sim/não ou nulo de acordo com o parâmetro

    """
    if argument is None:
        return 'nulo'
    elif argument:
        return 'sim'
    else:
        return 'não'


def string_similarity(string1, string2):
    """

    Args:
        string1 (str): Primeira string que vai ser comparada
        string2 (str): Segunda string que vai ser comparada

    Returns:
        float: O quão similar são as strings, podendo ir de 0.0 a 1.0

    Examples:
        >>> string_similarity('string 1', 'string 1')
        1.0
        >>> string_similarity('string 1', 'string 2')
        0.95
        >>> string_similarity('abc', 'bcd')
        0.0
        >>> string_similarity('apple', 'appel')
        0.9533333333333333

    """
    return jaro_winkler_similarity(str(string1), str(string2))


def get_most_similar_item(string, list_items, key=lambda x: str(x)):
    """

    Args:
        string (str): String que vai ser comparada com a lista
        list_items (List[str]): Uma lista de strings que vão ser comparadas com a primeira string
        key: Função que vai determinar como vai ser comparado os itens da lista (Default value = str(item))

    Returns:
        str: O item da lista mais parecido com a string do parâmetro

    """
    # lista que vai guardar o item e o score mais alto que teve
    highest_score = [0.0, '']
    for item in list_items:
        # vai pegar o quão similar a string é do item
        similarity = string_similarity(string, key(item))
        # se a similaridade for maior do que a registrada
        # vai atualizar
        if similarity > highest_score[0]:
            highest_score[0] = similarity
            highest_score[-1] = item
    # se algum item ser pelo menos 50% parecido com a string, vai retornar ele
    if highest_score[0] >= 0.5:
        return highest_score[-1]
    # caso contrario, retorna nada
    return None


def get_most_similar_items(string, list_items, key=lambda x: str(x)):
    """

    Args:
        string (str): String que vai ser comparada com a lista
        list_items (List[str]): Uma lista de strings que vão ser comparadas com a primeira string
        key: Função que vai determinar como vai ser comparado os itens da lista (Default value = str(item))

    Returns:
        list: Uma lista com os itens mais parecidos com a string base

    """
    list_items_cp = list_items.copy()
    ms = []
    for _ in list_items:
        most_similar = get_most_similar_item(string, list_items_cp, key)
        if most_similar is not None:
            list_items_cp.remove(most_similar)
            ms.append(most_similar)
        else:
            break
    return ms


def get_most_similar_items_with_similarity(string, list_items, key=lambda x: str(x)):
    """

    Args:
        string (str): String que vai ser comparada com a lista
        list_items (List[str]): Uma lista de strings que vão ser comparadas com a primeira string
        key: Função que vai determinar como vai ser comparado os itens da lista (Default value = str(item))

    Returns:
        list: Uma lista com os itens mais parecidos com a string base e também qual o grau de similaridade

    """
    list_items_cp = list_items.copy()
    ms = []
    for _ in range(len(list_items)):
        most_similar = get_most_similar_item(string, list_items_cp, key)
        if most_similar is not None:
            list_items_cp.remove(most_similar)
            ms.append([most_similar, string_similarity(string, key(most_similar))])
        else:
            break
    return ms


def difference_between_lists(list1, list2):
    """

    Args:
        list1 (list): Primeira lista
        list2 (list): Segunda lista

    Returns:
        list: Uma lista com os itens que não se repetiram nas listas passadas

    Examples:
        >>> difference_between_lists([2, 3, 4, 5], [1, 2, 3, 4])
        [5, 1]
        >>> difference_between_lists([print, sorted, str], [int, str, sorted])  # funciona com lista de qualquer coisa
        [<function print>, int]
        >>> difference_between_lists('abc', 'bcd')  # funciona com string, já que é uma lista de char
        ['a', 'd']

    """
    return list(set(list1) - set(list2)) + list(set(list2) - set(list1))


def prettify_number(number, br=True, truncate=False):
    """

    Args:
        number (Any): O valor que vai ser deixado "bonito"
        br (bool): Flag que vai ativar ou não o padrão br: "100.000,00". Se tiver desativado, vai sair assim "100,000.00"
        truncate (bool): Parâmetro que vai definir se é ou não para cortar as casas decimais

    Returns:
        str: A string com o número formatado

    Examples:
        >>> prettify_number(123456789)
        '123.456.789'
        >>> prettify_number(3.141592)
        '3,1415'
        >>> prettify_number(3.141592, truncate=True)
        '3,14'

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


def get_path_from_file(filename, directory=''):
    """

    Args:
        filename (str): Nome do arquivo que quer procurar
        directory (str): Pastas onde o arquivo vai estar (Default value = '')

    Returns:
        str: A localização do arquivo

    Examples:
        # como depende de onde a função está sendo chamada, o mesmo arquivo pode ter diferentes paths
        >>> get_path_from_file('Utils', 'utils/')
        '../utils/Utils.py'
        >>> get_path_from_file('*.py', 'utils/')
        '../utils/permissions.py'
        >>> get_path_from_file('Utils.py', '**/')
        '../utils/Utils.py'

    """
    path = ''
    while True:
        files = glob(f'{path}{directory}{filename}')
        if len(files) != 0:
            return files[0]
        if path == '':
            path = './'
        elif path == './':
            path = '../'
        else:
            path += '../'
        if path.count('../') >= 5:
            return None


def to_utf8(string):
    """

    Args:
        string: A string que vai ser filtrada

    Returns:
        str: A string inicial apenas com caracteres utf-8

    """
    return ''.join(filter(lambda x: str(x) in string_lib.printable, list(str(string))))


async def find_user(user_input, ctx, accuracy=0.6, API_search=True):
    """

    Args:
        user_input (str): O input que vai ser procurado na collection de membros/users
        ctx (discord.ext.commands.Context): Contexto da mensagem
        accuracy (float): O quão parecido vai precisar ser o input com o usuário, para selecionar ele (Default value = 0.6)
        API_search (bool): Se é ou não para pegar o user pela API do discord, caso o input seja um id (Default value = True)

    Returns:
        List[discord.User]: O(s) usuário/membro(s) encontrado(s)

    """

    class ItemSimilarity:
        def __init__(self, value, similarity):
            self.item = value
            self.similarity = similarity

        def __eq__(self, other):
            return isinstance(other, ItemSimilarity) and other.item == self.item

        def __ne__(self, other):
            return not self.__eq__(other)

        def __hash__(self):
            return hash(self.item)

    user_input = to_utf8(user_input).lower()
    if user_input == '':
        return []
    user_input_int = None
    if is_number(user_input):
        try:
            user_input_int = int(user_input)
        except ValueError:
            pass
    # se o input for '<@123456789123456>' vai entrar no regex
    mention_regex = compile(r'<@!?([0-9]{16,20})>')
    mention_match = mention_regex.match(user_input)
    if mention_match is not None:
        try:
            # extraindo o id da mention
            user_input_int = int(mention_match.group(1))
        except ValueError:
            pass
    exact_items = []
    most_similar_items = []
    endswith_items = []
    startswith_items = []
    collection = []
    bot = ctx.bot
    if ctx.guild:
        collection = ctx.guild.members
    collection += bot.users
    collection = list(set(collection))
    for item in collection:
        if user_input_int is not None:
            if item.id == user_input_int:
                return [item]
            continue
        name = to_utf8(item.name).lower()
        display_name = to_utf8(item.display_name).lower()
        name_tag = to_utf8(str(item)).lower()
        sim_name = string_similarity(name, user_input)
        if sim_name == 1.0:
            exact_items.append(item)
            continue
        sim_display_name = string_similarity(display_name, user_input)
        if sim_display_name == 1:
            exact_items.append(item)
            continue
        sim_name_tag = string_similarity(name_tag, user_input)
        if sim_name_tag == 1.0:
            exact_items.append(item)
            continue
        most_similarity = reduce(lambda x, y: x if x > y else y, [sim_name, sim_display_name, sim_name_tag])
        if most_similarity >= accuracy:
            most_similar_items.append(ItemSimilarity(item, most_similarity))
        elif name.startswith(user_input) or display_name.startswith(user_input) or name_tag.startswith(user_input):
            startswith_items.append(item)
        elif name.endswith(user_input) or display_name.endswith(user_input) or name_tag.endswith(user_input):
            endswith_items.append(item)
    if len(exact_items) > 0:
        return exact_items
    elif API_search and user_input_int is not None:
        try:
            return [await bot.fetch_user(user_input_int)]
        except:
            pass
    if len(most_similar_items) > 0:
        most_similar_items.sort(key=lambda k: k.similarity,
                                reverse=True)
        if most_similar_items[0].similarity >= 0.8 or len(most_similar_items) <= 4:
            return [reduce(lambda x, y: x if x.similarity > y.similarity else y, most_similar_items).item]
        else:
            return list(map(lambda x: x.item, most_similar_items))
    elif len(startswith_items) > 0:
        return [startswith_items[0]]
    elif len(endswith_items) > 0:
        return [endswith_items[0]]
    return []


# https://stackoverflow.com/questions/3229419/how-to-pretty-print-nested-dictionaries
def pretty_i(iterable, indent_char='\t', new_line_char='\n', indent=0):
    """

    Args:
        iterable (any): Iterable que vai ser formatado. (não funciona com generators).
        indent_char (str): Char que vai ser usado na indentação (Default value = '\t')
        new_line_char (str): Char que vai ser usado para quebrar as linhas  (Default value = '\n')
        indent (int): Parâmetro que é usado internamente na recursão  (Default value = 0)

    Returns:
        str: Uma string, com o iterable formatado.

    """
    new_line = new_line_char + indent_char * (indent + 1)
    extremities = ''
    if isinstance(iterable, dict):
        items = []
        for key, value in iterable.items():
            items.append(f'{new_line}{repr(key)}: {pretty_i(value, indent_char, new_line_char, indent + 1)}')
        extremities = '{}'
    elif isinstance(iterable, (list, tuple, set, frozenset)):
        items = [new_line + pretty_i(item, indent_char, new_line_char, indent + 1) for item in iterable]
        if isinstance(iterable, list):
            extremities = '[]'
        elif isinstance(iterable, tuple):
            extremities = '()'
        elif isinstance(iterable, set):
            extremities = '{}'
        elif isinstance(iterable, frozenset):
            extremities = 'frozenset()'
    else:
        return repr(iterable)
    return extremities[:-1] + (','.join(items) + new_line_char + indent_char * indent) + extremities[-1:]


def info(object_):
    """

    Args:
        object_: O objeto que vai ser extraido, as informações

    Returns:
        dict: As informações extraidas

    """
    import inspect
    methods = []
    magic_methods = []
    functions = []
    async_functions = []
    attributes = []
    classes = []
    all_attrs = {}
    try:
        all_attrs['classes'] = inspect.getmro(object_)
    except AttributeError:
        all_attrs['class'] = str(type(object_)).split("'")[1]
    if isinstance(object_, (int, float, bool, str)):
        all_attrs['type'] = 'built-in type'
        del all_attrs['class']
    elif isinstance(object_, (list, tuple, set, dict, frozenset)):
        all_attrs['type'] = 'data structure'
        all_attrs['length'] = len(object_)
    elif inspect.ismodule(object_):
        del all_attrs['class']
        all_attrs['type'] = 'module'
        if hasattr(all_attrs, 'version'):
            all_attrs['version'] = object_.__version__
        if hasattr(all_attrs, 'author'):
            all_attrs['author'] = object_.__author__
    elif inspect.isclass(object_):
        all_attrs['type'] = 'class'
    elif inspect.isbuiltin(object_):
        all_attrs['type'] = 'built-in function or method'
    elif inspect.isgeneratorfunction(object_):
        all_attrs['type'] = 'generator function'
    elif inspect.isgenerator(object_):
        all_attrs['type'] = 'generator'
    elif inspect.isasyncgenfunction(object_):
        all_attrs['type'] = 'async generator function'
    elif inspect.isasyncgen(object_):
        all_attrs['type'] = 'async generator'
    elif callable(object_):
        all_attrs['type'] = 'function'
        try:
            all_attrs['signature'] = f'{object_.__qualname__}{inspect.signature(object_)}'
        except ValueError:
            pass
        except TypeError:
            pass
    else:
        all_attrs['type'] = 'object'
    for attr_name in dir(object_):
        try:
            attr = getattr(object_, attr_name)
        except AttributeError:
            continue
        if inspect.iscoroutinefunction(attr):
            async_functions.append(f'{attr_name}{inspect.signature(attr)}')
        elif inspect.isfunction(attr):
            if all_attrs['type'] == 'module' and inspect.getmodule(attr) != object_: continue
            if attr_name.startswith('__') and attr_name.endswith('__'):
                magic_methods.append(f'{attr_name}{inspect.signature(attr)}')
            else:
                functions.append(f'{attr_name}{inspect.signature(attr)}')
        elif inspect.ismethod(attr):
            if all_attrs['type'] == 'module' and inspect.getmodule(attr) != object_: continue
            if attr_name.startswith('__') and attr_name.endswith('__'):
                magic_methods.append(attr_name)
            else:
                methods.append(f'{attr_name}{inspect.signature(attr)}')
        elif inspect.isclass(attr) and all_attrs['type'] == 'module':
            classes.append(attr_name)
        elif callable(attr):
            if all_attrs['type'] == 'module' and inspect.getmodule(attr) != object_: continue
            if attr_name.startswith('__') and attr_name.endswith('__'):
                magic_methods.append(attr_name)
            else:
                functions.append(attr_name)
        else:
            attributes.append(attr_name)
    if len(functions) > 0:
        all_attrs['functions'] = tuple(functions)
    if len(async_functions) > 0:
        all_attrs['async functions'] = tuple(async_functions)
    if len(methods) > 0:
        all_attrs['methods'] = tuple(methods)
    if len(magic_methods) > 0:
        all_attrs['magic methods'] = tuple(magic_methods)
    if len(classes) > 0:
        all_attrs['classes'] = tuple(classes)
    if len(attributes) > 0:
        all_attrs['attributes'] = tuple(attributes)
    return all_attrs
