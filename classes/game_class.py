from .config_class import GameConfig as cfg
from .card_class import Card
from .player_class import Player
import random


class Game(cfg):
    """Класс игры"""
    def __log(self, *args):
        message = ' '.join([str(arg) for arg in args])
        #print(message)
        self.log.append(message)

    def __create_plrs(self):
        self.plrs = []
        bank = cfg.all_players_bank // cfg.n_of_players
        names = cfg.players_names[:]
        random.shuffle(names)

        for plr in range(cfg.n_of_players):
            name = names.pop()
            plr = Player(bank, name)
            self.plrs.append(plr)

    def __select_dealer(self):
        plr = random.choice(self.plrs)
        plr.dealer = True
        self.current_plr_id = self.plrs.index(plr)

    def __init__(self):
        super(Game, self).__init__()
        self.log = []
        self.river = []
        self.bank = 0
        self.min_bit = 0
        self.sb = 0
        self.bb = 0
        self.hand_number = 1
        self.deck = []

        self.__create_plrs()
        self.__select_dealer()

    def __create_deck(self):
        deck = []
        for sui in range(len(Card.suits)):
            for val in range(len(Card.vals)):
                c = Card(sui, val)
                deck.append(c)
        return deck

    def __give_cards(self):
        random.shuffle(self.deck)
        for plr in self.plrs:
            plr.cards = []
            plr_card_1 = [self.deck.pop()]
            plr_card_2 = [self.deck.pop()]
            plr.cards += plr_card_1 + plr_card_2

    def hand_init(self):
        self.deck = self.__create_deck()
        random.shuffle(self.deck)
        self.__give_cards()

    def __next_act_plr(self):
        self.current_plr_id += 1
        if self.current_plr_id > len(self.plrs) - 1:
                self.current_plr_id = 0

        skip_list = ['Fold', 'All-in']
        while self.plrs[self.current_plr_id].last_act in skip_list:
            self.current_plr_id += 1
            if self.current_plr_id > len(self.plrs) - 1:
                self.current_plr_id = 0

        next_plr = self.plrs[self.current_plr_id]

        return next_plr

    def __daler_id(self):
        dealer, = [plr for plr in self.plrs if plr.dealer]

        ind = self.plrs.index(dealer)

        return ind

    def __clear_acts(self, full=False):
        if full:
            for plr in self.plrs:
                plr.last_act = 'None'
        else:
            for plr in self.plrs:
                if plr.last_act != 'Fold' and plr.last_act != 'All-in':
                    plr.last_act = 'None'

    def __clear_bits(self):
        for plr in self.plrs:
            plr.last_bit = 0

    def hand_result(self):

        def select_winner():
            self.__log('=' * 80)
            if len(self.active_plrs(no_fold=True)) == 1:
                winner, = self.active_plrs(no_fold=True)
                winner.bank += self.bank
                self.__log(winner.name, 'не открывая карты')
            else:
                win_combo_power = max(plr.combo.power for plr in self.plrs)
                winners = [plr for plr in self.plrs if plr.combo.power == win_combo_power]
                if len(winners) == 1:
                    winner, = winners
                    winner.bank += self.bank
                    self.__log(winner.name, winner.combo.text)
                else:
                    for plr in winners:
                        plr.bank += self.bank // len(winners)
                        self.__log(', '.join([plr.name for plr in winners]), winners[0].combo.text)
            self.bank = 0
            self.__log('=' * 80)

        def remove_loosers():
            loosers = []
            for plr in self.plrs:
                if plr.bank == 0:
                    loosers.append(plr)

            for looser in loosers:
                self.plrs.remove(looser)

        def move_dealer():
            old_dealer_id = self.__daler_id()
            old_dealer = self.plrs[old_dealer_id]
            old_dealer.dealer = False

            new_dealer_id = old_dealer_id + 1
            if new_dealer_id == len(self.plrs):
                new_dealer_id = 0

            while self.plrs[new_dealer_id] not in self.with_bank_plrs():
                new_dealer_id += 1
                if new_dealer_id == len(self.plrs):
                    new_dealer_id = 0

            new_dealer = self.plrs[new_dealer_id]
            new_dealer.dealer = True

            self.current_plr_id = self.plrs.index(new_dealer)

        select_winner()
        move_dealer()
        remove_loosers()

        self.river = []
        self.__clear_acts('full')

    def with_bank_plrs(self):
        plrs_list = [plr for plr in self.plrs if plr.bank > 0]
        return plrs_list

    def active_plrs(self, no_fold=False, no_allin=False):
        if no_fold and no_allin:
            skip_list = ['Fold', 'All-in']
        elif no_fold:
            skip_list = ['Fold']
        elif no_allin:
            skip_list = ['All-in']

        plrs = [plr for plr in self.plrs if plr.last_act not in skip_list]
        return plrs

    def __process_the_state(self, state):

        def take_blinds():
            if cfg.double_blinds:  # Вычисление блайндов если умножаются
                double_index = (self.hand_number - 1) // cfg.double_blinds_interval  # Делим без остатка номер раздачи (от 0) на промежуток

                self.sb = cfg.start_sb * (2 ** double_index)  # Умножаем стартовый блайнд на 2 в степени double_index
                self.bb = cfg.start_bb * (2 ** double_index)
            else:
                self.sb = cfg.start_sb
                self.bb = cfg.start_bb

            sb_plr = self.__next_act_plr()
            act = sb_plr.small_blind(self.sb)
            self.bank += act['bit']
            self.__log(self.plrs.index(sb_plr), sb_plr.name, sb_plr.last_act, sb_plr.last_bit)

            bb_plr = self.__next_act_plr()
            act = bb_plr.big_blind(self.bb)
            self.bank += act['bit']
            self.__log(self.plrs.index(bb_plr), bb_plr.name, bb_plr.last_act, bb_plr.last_bit)

            self.min_bit = self.bb

        def take_bits():
            while True:

                bb_flag = False
                if len(self.active_plrs(no_fold=True, no_allin=True)) > 1:
                    plr = self.__next_act_plr()

                    if plr.last_bit == self.bb and plr.last_act == 'BB':
                        bb_flag = True
                    elif plr.last_bit == self.min_bit and plr.last_act == 'Raise':
                        break
                else:
                    plr, = self.active_plrs(no_fold=True, no_allin=True)
                    break

                plr.action(self.plrs, self.river, self.min_bit, self.bb)
                self.bank += plr.last_bit

                self.__log(self.plrs.index(plr), plr.name, plr.last_act, plr.last_bit, plr.combo.text)

                if bb_flag and plr.last_bit == 0 and self.min_bit > 0:
                    break

                if plr.last_bit > self.min_bit:
                    self.min_bit = plr.last_bit

        if state == self.states[0]:
            take_blinds()
        elif state == self.states[1]:
            self.river += [self.deck.pop()]
            self.river += [self.deck.pop()]
            self.river += [self.deck.pop()]
        elif state == self.states[2]:
            self.river += [self.deck.pop()]
        elif state == self.states[3]:
            self.river += [self.deck.pop()]

        self.__log(self.hand_number, state, self.__daler_id(), ' '.join([c.name for c in self.river]), '-' * 30)

        take_bits()

        # Очищаем записи о действиях игроков
        self.__clear_acts()
        self.__clear_bits()
        self.min_bit = 0
        self.current_plr_id = self.__daler_id()

    def process_hand(self):
        for state in cfg.states:

            if len(self.active_plrs(no_fold=True, no_allin=True)) < 2:
                break
            self.__process_the_state(state)


if __name__ == '__main__':
    main()
