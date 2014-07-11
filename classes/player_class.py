from .config_class import PlayerConfig as cfg
import random


class Player(cfg):
    """docstring for PLayer"""
    def __init__(self, pid, bank):
        super(Player, self).__init__()
        self.dealer = False
        self.last_act = 'None'
        self.last_bit = 0

        self.pid = pid
        self.bank = bank

        random.shuffle(cfg.names)
        self.name = cfg.names.pop()

    def __check_combo(self):
        pass

    def action(self, river, blind=False, sb=0, bb=0):
        if blind == 'sb':
            if self.bank > sb:
                self.last_act = 'SB'
                self.last_bit = sb
                self.bank -= sb
            else:
                self.last_act = 'All-in'
                self.last_bit = self.bank
                self.bank = 0
        elif blind == 'bb':
            if self.bank > bb:
                self.last_act = 'BB'
                self.last_bit = bb
                self.bank -= bb
            else:
                self.last_act = 'All-in'
                self.last_bit = self.bank
                self.bank = 0

        self.__check_combo()
        actions = ['Check', 'Fold', 'Call', 'Raise', 'All-in']

        act = {'name': self.last_act, 'bit': self.last_bit}
        return act
