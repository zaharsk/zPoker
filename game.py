from table import *
from random import *
from player import *
from combo import *


class Game(object):
    """
    Класс игры.
    """
    def __init__(self, n_of_players):
        self.state = None
        self.active_player_index = None
        self.hand_number = None
        self.acts_log = []  # Лог действий игроков
        self.min_bit = 0  # Минимальная ставка
        self.n_of_players = n_of_players
        self.bits_round = 0
        self.bb = 0
        self.tbl = Table()  # Создаём пустой стол
        self.finish_min_bit = 0  # Ставка в конце раунда. Необходима для отрисовки.

    def create_players(self, names, start_bank):
        if self.n_of_players < 2:
            self.n_of_players = 2  # Проверяем настройки
        if self.n_of_players > 6:
            self.n_of_players = 6  # Проверяем настройки

        self.tbl.players = []

        for x in range(self.n_of_players):
            name = names.pop(randint(0, len(names) - 1))  # Выбираем случаное имя

            plr_bank = start_bank // self.n_of_players
            player = Player(x, name, plr_bank)  # Создаём игрока

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
            plr.cards = [self.tbl.deck.pop(0)]
            plr.cards.append(self.tbl.deck.pop(0))
        return None

    def remove_loosers(self):
        self.tbl.players = [plr for plr in self.tbl.players if plr.bank > 0]
        return None

    def active_players(self, no_fold=False, no_all_in=False):
        if no_fold and no_all_in:
            players = [plr for plr in self.tbl.players if plr.act != 'Fold' and plr.act != 'All-in']
        elif no_fold:
            players = [plr for plr in self.tbl.players if plr.act != 'Fold']
        elif no_all_in:
            players = [plr for plr in self.tbl.players if plr.act != 'All-in']
        else:
            players = self.tbl.players
        return players

    def next_player(self, for_bit=False):
        if for_bit:
            act_indexes = [plr.index for plr in self.active_players('no_fold', 'no_all_in')]
        else:
            act_indexes = [plr.index for plr in self.active_players()]

        self.active_player_index += 1

        while self.active_player_index not in act_indexes:
            self.active_player_index += 1

            if self.active_player_index >= self.n_of_players:
                self.active_player_index = 0

        player, = [plr for plr in self.active_players() if plr.index == self.active_player_index]
        return player

    def clear_log(self):
        self.acts_log = []
        return None

    def clear_plrs_acts(self, full=False):
        if full == 'full':
            for plr in self.active_players():
                plr.act = None
        elif full == 'no_all_in':
            for plr in self.active_players():
                if plr.act != 'All-in':
                    plr.act = None
        return None

    def clear_plrs_bits(self):
        for plr in self.active_players():
            plr.bit = 0
        return None

    def move_dealer(self):
        old_dealer_index, = [plr.index for plr in self.active_players() if plr.dealer]
        old_dealer, = [plr for plr in self.active_players() if plr.index == old_dealer_index]
        old_dealer.dealer = False

        self.active_player_index = old_dealer_index

        self.remove_loosers()

        new_dealer = self.next_player()
        new_dealer.dealer = True
        self.active_player_index = new_dealer.index
        return None

    def hand_result(self):
        combo_indexes = [plr.combo.index for plr in self.active_players('no_fold')]
        winners = [plr for plr in self.active_players('no_fold') if plr.combo.index == max(combo_indexes)]

        combo_powers = [plr.combo.power for plr in winners]
        winners = [plr for plr in winners if plr.combo.power == max(combo_powers)]

        if len(winners) == 1:
            winner, = winners
            winner.bank += self.tbl.banks[0]
        else:
            for plr in winners:
                plr.bank += self.tbl.banks[0] // len(winners)

        self.tbl.banks[0] = 0
        return winners

    def change_state(self, state, states, start_sb, start_bb, d_blinds, d_int):

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
                sb_player.bit = sb
                sb_player.bank -= sb
                act = 'SB'
            else:
                self.tbl.banks[0] += sb_player.bank
                sb_player.bit = sb_player.bank
                sb_player.bank = 0
                act = 'All-in'

            sb_player.act = act
            self.acts_log.append({'plr': sb_player.name, 'act': act, 'bits_round': self.bits_round, 'bit': sb_player.bit})

            bb_player = self.next_player()
            if bb_player.bank > bb:
                self.tbl.banks[0] += bb
                bb_player.bit = bb
                bb_player.bank -= bb
                act = 'BB'
            else:
                self.tbl.banks[0] += bb_player.bank
                bb_player.bit = bb_player.bank
                bb_player.bank = 0
                act = 'All-in'

            bb_player.act = act
            self.bb = bb
            self.min_bit = bb
            self.acts_log.append({'plr': bb_player.name, 'act': act, 'bits_round': self.bits_round, 'bit': bb_player.bit})

        def check_combos():
            for plr in self.active_players():
                plr.combo = Combo(plr.cards + self.tbl.cards, state)
            return None

        def actions():
            start_min_bit = self.min_bit

            for x in range(len(self.active_players('no_fold', 'no_all_in'))):
                plr = self.next_player('for_bit')

                if plr.act == 'Raise' and plr.bit == self.min_bit:
                    print('raise stop')
                    return None

                if len(self.active_players('no_fold')) < 2:
                    return None

                act = plr.action(self.active_players('no_fold'), self.acts_log, self.bits_round, self.min_bit, self.bb)

                self.tbl.banks[0] += plr.bit

                if plr.act != 'Fold' and plr.bit > self.min_bit:
                    self.min_bit = plr.bit

                self.acts_log.append({'plr': plr.name, 'act': act, 'bits_round': self.bits_round, 'bit': plr.bit})

            self.bits_round += 1

            self.finish_min_bit = self.min_bit

            if self.min_bit > start_min_bit:
                actions()

            if len(self.active_players('no_fold', 'no_all_in')) < 2:
                return None

            self.bits_round = 0
            return None

        self.clear_log()
        self.clear_plrs_acts('no_all_in')
        self.clear_plrs_bits()

        if state == states[0]:
            take_blinds()
            self.tbl.cards = []
        elif state == states[1]:
            self.tbl.cards = self.tbl.deck[:3]
        elif state == states[2]:
            self.tbl.cards = self.tbl.deck[:4]
        elif state == states[3]:
            self.tbl.cards = self.tbl.deck

        check_combos()
        actions()
        self.min_bit = 0
