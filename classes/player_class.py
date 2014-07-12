from .config_class import PlayerConfig as cfg
from .combo_class import Combo
import random


class Player(cfg):
    """docstring for PLayer"""
    def __init__(self, bank):
        super(Player, self).__init__()
        self.dealer = False
        self.last_act = 'None'
        self.last_bit = 0
        self.combo = None

        self.bank = bank

        random.shuffle(cfg.names)
        self.name = cfg.names.pop()

    def __check_combo(self, river):
        check_cards = self.cards + river
        self.combo = Combo(check_cards)

    def action(self, players, river, min_bit, bb):
        self.__check_combo(river)
        actions = ['Fold', 'Check', 'Call', 'Raise', 'All-in']
        max_bank = max([player.bank for player in players])

        if min_bit > 0 and self.last_bit < min_bit:
            actions.remove('Check')

        if min_bit == 0 or min_bit == self.last_bit:
            actions.remove('Fold')

        if self.bank <= min_bit or min_bit == 0:
            actions.remove('Call')

        if self.bank < min_bit + bb:
            actions.remove('Raise')

        if self.bank > max_bank:
            actions.remove('All-in')

        min_power = 761856

        act_power = self.combo.power // min_power

        if act_power < 1:
            act = actions[0]
        else:
            act = actions[1]
        print(self.name, min_bit, actions, act_power, act)
        print('')
        if act == 'Check':
            self.last_act = 'Check'
            self.last_bit = 0
        elif act == 'Fold':
            self.last_act = 'Fold'
            self.last_bit = 0
        elif act == 'Call':
            self.last_act = 'Call'
            self.last_bit = min_bit
            self.bank -= self.last_bit
        elif act == 'Raise':
            self.last_act = 'Raise'
            self.last_bit = min_bit + bb
            self.bank -= self.last_bit
        elif act == 'All-in':
            self.last_act = 'All-in'
            self.last_bit = self.bank
            self.bank = 0

        return {'name': self.last_act, 'bit': self.last_bit}

    def small_blind(self, sb):
        if self.bank > sb:
            self.last_act = 'SB'
            self.last_bit = sb
            self.bank -= sb
        else:
            self.last_act = 'All-in'
            self.last_bit = self.bank
            self.bank = 0

        return {'name': self.last_act, 'bit': self.last_bit}

    def big_blind(self, bb):
        if self.bank > bb:
            self.last_act = 'BB'
            self.last_bit = bb
            self.bank -= bb
        else:
            self.last_act = 'All-in'
            self.last_bit = self.bank
            self.bank = 0

        return {'name': self.last_act, 'bit': self.last_bit}
