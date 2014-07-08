from table import *
from random import *
from player import *
from combo import *


class Game(object):
    """
    Класс игры.
    """
    def __init__(self):
        self.state = None
        self.active_player_index = None
        self.hand_number = None
        self.acts_log = []  # Лог действий игроков
        self.min_bit = 0  # Минимальная ставка

    def create_table(self):
        self.tbl = Table()  # Создаём пустой стол
        return None

    def create_players(self, n_of_players, names, start_bank):
        if n_of_players < 2:
            n_of_players = 2  # Проверяем настройки
        if n_of_players > 6:
            n_of_players = 6  # Проверяем настройки

        self.tbl.players = []

        for x in range(n_of_players):
            name = names[randint(0, len(names) - 1)]  # Выбираем случаное имя

            plr_bank = start_bank // n_of_players
            player = Player(x, name, plr_bank)  # Создаём игрока
            names.remove(name)  # Удаляем имя из пула
            self.tbl.players.append(player)  # Добавляем игрока за стол
        return None

    def select_dealer(self):
        dealer_index = randint(0, len(self.tbl.players) - 1)
        self.tbl.players[dealer_index].dealer = True
        self.active_player_index = dealer_index
        return None

    def give_cards(self, suits, values):
        self.tbl.create_deck(suits, values)
        for plr in self.tbl.players:
            plr.cards = self.tbl.deck[:2]
            for card in plr.cards:
                self.tbl.deck.remove(card)
        return None

    def remove_loosers(self):
        for plr in self.tbl.players:
            if plr.bank == 0:
                self.tbl.players.remove(plr)
        return None

    def active_players(self, no_fold=False, no_all_in=False):
        if no_fold and no_all_in:
            pass
        elif no_fold:
            pass
        elif no_all_in:
            pass
        else:
            players = self.tbl.players
        return players

    def next_player(self):
        self.active_player_index += 1

        if self.active_player_index == len(self.active_players()):
            self.active_player_index = 0

        player = self.tbl.players[self.active_player_index]
        return player

    def clear_log(self):
        self.acts_log = []
        return None

    def clear_plrs_acts(self, full=False):
        if full:
            for plr in self.active_players():
                plr.act = None
        else:
            pass
        return None

    def clear_plrs_bits(self):
        for plr in self.active_players():
            plr.bit = 0
        return None

    def move_dealer(self):
        old_dealer_index = [plr.index for plr in self.active_players() if plr.dealer][0]
        self.active_player_index = old_dealer_index

        old_dealer = self.active_players()[old_dealer_index]
        old_dealer.dealer = False

        new_dealer = self.next_player()
        new_dealer.dealer = True
        self.active_player_index = new_dealer.index
        print(old_dealer.name, '->', new_dealer.name)
        return None

    def change_state(self, state, states, start_sb, start_bb, d_blinds, d_int):
        self.clear_log()
        self.clear_plrs_acts('full')
        self.clear_plrs_bits()

        def take_blinds():
            if d_blinds:  # Вычисление блайндов если умножаются
                double_index = (self.hand_number - 1) // d_int  # Делим без остатка номер раздачи (от 0) на промежуток

                sb = start_sb * (2 ** double_index)  # Умножаем стартовый блайнд на 2 в степени double_index
                bb = start_bb * (2 ** double_index)
            else:
                sb = start_sb
                bb = start_bb

            sb_player = self.next_player()
            if sb_player.bank > sb:
                self.tbl.banks[0] += sb
                sb_player.bank -= sb
                act = 'SB ' + str(sb)
            else:
                self.tbl.banks[0] += sb_player.bank
                sb_player.bank = 0
                act = 'SB ' + str(sb) + 'All-in'
            sb_player.act = act
            sb_player.bit = sb
            self.acts_log.append({'plr': sb_player.name, 'act': act})

            bb_player = self.next_player()
            if bb_player.bank > bb:
                self.tbl.banks[0] += bb
                bb_player.bank -= bb
                act = 'BB ' + str(bb)
            else:
                self.tbl.banks[0] += bb_player.bank
                bb_player.bank = 0
                act = 'BB ' + str(bb) + 'All-in'
            bb_player.act = act
            bb_player.bit = bb
            self.acts_log.append({'plr': bb_player.name, 'act': act})

        if state == states[0]:
            take_blinds()
            self.tbl.cards = []
        elif state == states[1]:
            self.tbl.cards = self.tbl.deck[:3]
        elif state == states[2]:
            self.tbl.cards = self.tbl.deck[:4]
        elif state == states[3]:
            self.tbl.cards = self.tbl.deck
