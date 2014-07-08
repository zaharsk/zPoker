from random import *
from card import *


class Table(object):
    """
    Класс игрового стола.
    Объединяет все игровые объекты: игроков, карты, блайнды, банк и т.д. Все
    манипуляции с объектами осуществляются в классе Game.
    """
    def __init__(self):
        self.players = None  # Массив игроков
        self.deck = None  # Карты для раздачи
        self.cards = None  # Открыте карты

        self.banks = [0]  # Сумма ставок на столе в текущей раздаче

    def create_deck(self, suis, vals):
        self.deck = []

        def rnd_card():
            sui = randint(0, len(suis) - 1)
            val = randint(0, len(vals) - 1)
            name = suis[sui] + vals[val]

            card = Card(sui, val, name)
            return card

        n_of_cards = 5 + 2 * len(self.players)

        new_card = rnd_card()

        for i in range(n_of_cards):
            while new_card.name in [card.name for card in self.deck]:
                new_card = rnd_card()
            self.deck.append(new_card)
        return None
