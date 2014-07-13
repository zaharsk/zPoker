import sys


class GameConfig(object):
    """Первоначальные настройки для класса Game"""
    n_of_players = 6
    all_players_bank = 6000
    states = ['pre_flop', 'flop', 'turn', 'river']
    double_blinds = True
    double_blinds_interval = n_of_players
    start_sb = 50
    start_bb = start_sb * 2
    players_names = [
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

    def __init__(self):
        super(GameConfig, self).__init__()


class PlayerConfig(object):
    """docstring for Player_Config"""
    def __init__(self):
        super(PlayerConfig, self).__init__()


class CardConfig(object):
    """Первоначальные настройки для класса Card"""
    if sys.stdout.encoding == 'cp866':  # Консоль windows
        suits = [chr(3), chr(4), chr(5), chr(6)]
    elif sys.stdout.encoding == 'UTF-8':  # unix
        suits = [chr(0x2665), chr(0x2666), chr(0x2663), chr(0x2660)]
    elif sys.stdout.encoding == 'cp1251':  # GUI windows
        suits = ['h', 'd', 'c', 's']
    vals = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        super(CardConfig, self).__init__()


class ComboConfig(object):
    """Первоначальные настройки для класса Combo"""

    def __init__(self):
        super(ComboConfig, self).__init__()

if __name__ == '__main__':
    main()
