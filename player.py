from random import *


class Player(object):
    """
    Класс игрока.
    При инициализации стола создаётся массив объектов этого класса
    в количестве, указанном в классе Config.
    """
    def __init__(self, index, name, bank):
        self.cards = None  # Карты игрока
        self.dealer = False  # Является ли игрок дилером
        self.act = None  # Текущее действие/ставка игрока
        self.dealer = None  # Является ли игрок дилером
        self.bit = None

        self.combo = None  # Сильнейшая комбинация игрока
        self.human = None  # Человек или компьютер.

        self.index = index
        self.name = name  # Имя игрока
        self.bank = bank  # Текущий банк игрока

    def action(self, players, full_log, b_round, min_bit, bb):
        actions = ['Fold', 'Check', 'Call', 'Raise', 'All-in']

        #log = [line['act'] for line in full_log if line['bits_round'] == b_round]

        if min_bit > 0 and self.act != 'BB' or self.bank < min_bit:
                actions.remove('Check')

        if self.bank < min_bit or self.bank < min_bit + bb:
            actions.remove('Raise')

        if self.bank < min_bit or min_bit == 0 or self.bank == min_bit:
            actions.remove('Call')

        if self.bank == max([plr.bank for plr in players]):
            actions.remove('All-in')

        if min_bit == 0:
            actions.remove('Fold')

        act = choice(actions)  # Принятие решения о ставке

        if act == 'Fold':
            bit = 0
        elif act == 'Check':
            bit = 0
        elif act == 'Call':
            bit = min_bit
        elif act == 'Raise':
            bit = min_bit + bb
        elif act == 'All-in':
            bit = self.bank

        self.act = act
        self.bit = bit
        self.bank -= bit
        return act
