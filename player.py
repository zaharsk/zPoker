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

    def action(self):

        return None
