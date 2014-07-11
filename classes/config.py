import sys


class GameConfig(object):
    """Первоначальные настройки для класса Game"""
    def __init__(self):
        super(GameConfig, self).__init__()

    n_of_players = 6


class CardConfig(object):
    """Первоначальные настройки для класса Card"""
    def __init__(self):
        super(CardConfig, self).__init__()

    if sys.stdout.encoding == 'cp866':  # Консоль windows
        suits = [chr(3), chr(4), chr(5), chr(6)]
    elif sys.stdout.encoding == 'UTF-8':  # unix
        suits = [chr(0x2665), chr(0x2666), chr(0x2663), chr(0x2660)]
    elif sys.stdout.encoding == 'cp1251':  # GUI windows
        suits = ['h', 'd', 'c', 's']
    vals = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class PlayerConfig(object):
    """docstring for Player_Config"""
    def __init__(self):
        super(PlayerConfig, self).__init__()

    names = [
        'Андрей',
        'Василий',
        'Пётр',
        'Сергей',
        'Ольга',
        'Мария',
        'Вадим',
        'Дмитрий',
        'Антон',
    ]
