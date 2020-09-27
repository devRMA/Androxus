# coding=utf-8
# Androxus bot
# Utils.py

__author__ = 'Rafael'


def pegar_o_prefixo(bot, message):
    """
    :param bot: Pode passar None, esse parâmetro não é usado
    :param message: A mensagem que quer saber o prefixo do bot
    :type bot: discord.ext.commands.Bot
    :type message: discord.Message
    :return: o prefixo do bot, para está mensagem
    :rtype: discord.ext.commands.Bot
    """
    from discord_bot.dao.ServidorDao import ServidorDao  # pega a classe que mexe com a table dos servidores
    if message.guild:  # se a mensagem tiver um servidor, é porque ela não foi enviada no privado
        prefixo = ServidorDao().get_prefix(
            message.guild.id)  # vai no banco de dados, e faz um select para ver qual o prefixo
        if prefixo is not None:  # se achou um prefixo, retorna o que achou
            return prefixo[0]
        else:  # se o banco disse que não tem esse servidor cadastrado, vai criar um
            ServidorDao().create(message.guild.id)  # vai criar o servidor no banco, com o prefixo padrão
            return '--'  # se acabou de criar o registro, o prefixo vai ser o padrão
    return ''  # se a mensagem foi enviado no privado, não vai ter prefixo


def random_color():
    """
    :return: uma cor "aleatoria "em hexadecimal
    :rtype: hex
    """
    from random import randint  # função que pega números aleatórios
    r = lambda: randint(0, 255)  # lambda que vai pegar os números
    # vai escolher os números, e depois transformar em hexadecimal 0x000000
    return int(f'0x{r():02x}{r():02x}{r():02x}', 16)


def get_emoji_dance():
    """
    :return: um emoji de dança aleatório
    :rtype: str
    """
    from random import choice
    # lista com os emojis
    emojis = ['<a:doguinho2:755843996437446686>',
              '<a:dance_bear:755843929592692886>',
              '<a:whitewobble:755843847619346433>',
              '<a:wobble:755843848542093483>',
              '<a:wobble2:755843848575647864>',
              '<a:wobbleblack:755843848717991956>',
              '<a:wobblered:755843848399225023>',
              '<a:aeeee:755774677678555307>',
              '<a:bob:755774679377117184>',
              '<a:cute_dance:755774679020601535>',
              '<a:cute_dance2:755774678764617750>',
              '<a:maluko_dancando:755774681440583680>',
              '<a:mario_e_luigi:755774681059033178>',
              '<a:parrot_dancando:755774679670718575>',
              '<a:pato:755774683348992060>',
              '<a:penguim_doidao:755774679557603360>',
              '<a:pepo_dance:755774680291344454>',
              '<a:SquidwardMilos:755774682174586890>']
    return choice(emojis)  # retorna o emoji escolhido da lista


def get_last_update():
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


def get_last_commit():
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


def get_configs():
    """
    :return: vai retornar um dicionário com as configurações do arquivo configs.json
    :rtype: dict
    """
    from json import load, dumps  # função que vai transformar de json para dict e vice versa
    from os.path import exists  # função que vai verificar se existe o arquivo json
    if exists('discord_bot/configs.json'):
        path = 'discord_bot/configs.json'  # se achar, salva o path
    elif exists('./configs.json'):
        path = './configs.json'
    else:
        path = None
    if path is not None:
        with open(path) as file:
            configs = load(file)
        return configs
    else:
        exit('Não achei o arquivo de configurações!\nBaixe o arquivo configs.json!\nhttps://github.com/devRMA/Androxus')


def capitalize(string):
    """
    :param string: string que vai ser formatada
    :type string: str
    :return: vai deixar apenas a primeira letra em maiúscula da string
    :rtype: str
    """
    new_string = ''
    foi = False
    for char in string:
        if (char.upper() != char) and (not foi):
            new_string += char.upper()
            foi = True
        else:
            new_string += char.lower()
    return new_string


def datetime_format(date1, date2=None):
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
    years = time.years
    months = time.months
    days = time.days
    hours = time.hours
    minutes = time.minutes
    seconds = time.seconds
    dt_str = ''
    if years > 1:
        dt_str += f'{years} anos'
    elif years == 1:
        dt_str += f'{years} ano'
    if months > 1:
        if years >= 1:
            dt_str += ', '
        dt_str += f'{months} meses'
    elif months == 1:
        if years >= 1:
            dt_str += ', '
        dt_str += f'{months} mês'
    if days > 1:
        if years >= 1 or months >= 1:
            dt_str += ', '
        dt_str += f'{days} dias'
    elif days == 1:
        if years >= 1 or months >= 1:
            dt_str += ', '
        dt_str += f'{days} dia'
    if hours > 1:
        if years >= 1 or months >= 1 or days >= 1:
            dt_str += ', '
        dt_str += f'{hours} horas'
    elif hours == 1:
        if years >= 1 or months >= 1 or days >= 1:
            dt_str += ', '
        dt_str += f'{hours} hora'
    if minutes > 1:
        if years >= 1 or months >= 1 or days >= 1:
            dt_str += ', '
        dt_str += f'{minutes} minutos'
    elif minutes == 1:
        if years >= 1 or months >= 1 or days >= 1:
            dt_str += ', '
        dt_str += f'{minutes} minuto'
    if seconds > 1:
        if years >= 1 or months >= 1 or days >= 1:
            dt_str += ', '
        dt_str += f'{seconds} segundos'
    elif seconds == 1:
        if years >= 1 or months >= 1 or days >= 1:
            dt_str += ', '
        dt_str += f'{seconds} segundo'
    dt_str += '.'
    dt_str = dt_str[:dt_str.rfind(',')] + ' e' + dt_str[dt_str.rfind(',') + 1:]
    return dt_str
