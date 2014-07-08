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

    def do_check(self, table_bank, bit):
        self.act = 'Check'
        self.bit = 0
        res = {
            'bit': 0,
            'act': self.act
        }
        return res

    def do_fold(self, table_bank, bit):
        self.act = 'Fold'
        self.bit = 0
        res = {
            'bit': 0,
            'act': self.act
        }
        return res

    def do_call(self, table_bank, bit):
        self.act = 'Call ' + str(bit)
        self.bit = bit
        res = {'act': self.act}

        if self.bank > bit:
            res['bit'] = bit
            self.bank -= bit
        else:
            res['bit'] = self.bank
            res['act'] = 'Call ' + str(self.bank) + ' All-in'
            self.act = 'Call ' + str(self.bank) + ' All-in'
            self.bank = 0

        return res

    def do_raise(self, table_bank, new_bit):
        self.act = 'Raise ' + str(new_bit)
        self.bit = new_bit
        res = {'act': self.act}

        if self.bank > new_bit:
            res['bit'] = new_bit
            self.bank -= new_bit
        else:
            res['bit'] = self.bank
            res['act'] = 'Raise ' + str(self.bank) + ' All-in'
            self.act = 'Raise ' + str(self.bank) + ' All-in'
            self.bank = 0

        return res
