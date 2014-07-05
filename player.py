class Player(object):
    """
    Класс игрока.
    При инициализации стола создаётся массив объектов этого класса в количестве,
    указанном в классе Config.
    """
    def __init__(self, name, bank):
        self.cards = []  # Карты игрока
        self.combo = None  # Сильнейшая комбинация игрока
        self.act = ''  # Текущее действие/ставка игрока
        self.human = False  # Человек или компьютер.
        self.in_game = True  # Есть ли деньги для продолжения игры
        self.dealer = False  # Является ли игрок дилером

        self.name = name  # Имя игрока
        self.bank = bank  # Текущий банк игрока

    def do_check(self, table_bank, bit):
        """
        Действие Check.
        Записывает Check в аттрибут act текущего экземпляра класса Player.
        Возвращает нулевую ставку и Check.
        """
        self.act = 'Check'
        res = {
            'bit': 0,
            'act': self.act
        }
        return res

    def do_fold(self, table_bank, bit):
        """
        Действие Fold.
        Записывает Fold в аттрибут act текущего экземпляра класса Player.
        Возвращает нулевую ставку и Fold.
        """
        self.act = 'Fold'
        res = {
            'bit': 0,
            'act': self.act
        }
        return res

    def do_call(self, table_bank, bit):
        """
        Действие Call.
        Записывает Call в аттрибут act текущего экземпляра класса Player,
        проверяет хватает ли у игрока денег на принятие текущей ставки и
        уменьшает её в случае необходимости.
        Возвращает ставку и Call.
        """
        self.act = 'Call'
        res = {'act': self.act}

        if self.bank >= bit:
            res['bit'] = bit
            self.bank -= bit
        else:
            res['bit'] = self.bank
            self.bank = 0
            res['act'] = 'All-in'

        return res

    def do_raise(self, table_bank, new_bit):
        """
        Действие Raise.
        Записывает Raise в аттрибут act текущего экземпляра класса Player,
        проверяет хватает ли у игрока денег на поднятие текущей ставки и
        уменьшает её в случае необходимости.
        Возвращает ставку и Raise.
        """
        self.act = 'Raise: ' + str(new_bit)
        res = {'act': self.act}

        if self.bank >= new_bit:
            res['bit'] = new_bit
            self.bank -= new_bit
        else:
            res['bit'] = self.bank
            self.bank = 0
            res['act'] = 'All-in'

        return res
