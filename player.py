class Player(object):
    """docstring for Player"""
    def __init__(self, name, bank):
        self.cards = []  # Player hand
        self.combo = None  # Player combo
        self.act = ''  # Current action
        self.last_act = ''  # Last action
        self.iq = 'comp'  # Computer, human or draw. Deafault: comp
        self.in_game = True
        self.dealer = False  # Current dealer

        self.name = name  # Player name
        self.bank = bank  # Player bank

    def do_check(self, table_bank, bit):
        self.act = 'Check'
        res = {
            'bit': 0,
            'act': self.act
        }
        return res

    def do_fold(self, table_bank, bit):
        self.act = 'Fold'
        res = {
            'bit': 0,
            'act': self.act
        }
        return res

    def do_call(self, table_bank, bit):
        self.act = 'Call'

        if self.bank >= bit:
            res = {'bit': bit}
            self.bank -= bit
        else:
            res = {'bit': self.bank}
            self.bank = 0

        res['act'] = self.act
        return res

    def do_raise(self, table_bank, new_bit):
        self.act = 'Raise: ' + str(new_bit)

        if self.bank >= new_bit:
            res = {'bit': new_bit}
            self.bank -= new_bit
        else:
            res = {'bit': self.bank}
            self.bank = 0

        res['act'] = 'Raise'
        return res
