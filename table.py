from random import *
from player import *
from card import *

class Table(object):
    """
    Класс игрового стола.
    Объединяет все игровые объекты: игроков, карты, блайнды, банк и т.д. Все 
    манипуляции с объектами осуществляются в классе Game.
    """
    def __init__(self, n_of_players, start_bank, player_names):
        self.banks = [0]  # Сумма ставок на столе в текущей раздаче
        self.cards_pool = []  # Карты, выбранные для раздчи
        self.cards = []  # Открыте карты
        self.players = []  # Массив игроков

        self.n_of_players = n_of_players
        self.start_bank = start_bank
        self.player_names = player_names

    def create_players(self):
        """
        Проверяем настройки и создаём игроков.
        """
        if self.n_of_players < 2: self.n_of_players = 2
        if self.n_of_players > 6: self.n_of_players = 6

        plrs_bank = self.start_bank // self.n_of_players


        for x in range(self.n_of_players):  # Создаём игроков
            name_index = randint(0, len(self.player_names) - 1)
            plr_name = self.player_names[name_index]
            self.player_names.remove(plr_name)

            self.players.append(Player(plr_name, plrs_bank))

        human_index = randint(0, len(self.players) - 1)
        self.players[human_index].human = True

        user_name = input('Введите Ваше имя [Игрок]:')

        if user_name:
            self.players[human_index].name = user_name
        else:
            self.players[human_index].name = 'Игрок'

        return None