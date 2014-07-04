class Card(object):
    """
    Класс игральной карты.
    При инициализации стола создаётся массив объектов этого класса, после чего
    распрделяется между игроками и в пул стола.
    """
    def __init__(self, sui, val, name):
        self.sui = sui
        self.val = val
        self.name = name
