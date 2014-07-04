class Combo(object):
    """
    Класс комбинации игрока.
    При проверке комбинаций выбирается старшая и записывается в атрибут объекта
    класса Player.
    """
    def __init__(self, index, name, cards, text):
        self.index = index
        self.name = name
        self.cards = cards
        self.text = text
        self.power = 0  # "Сила" комбинации для сравнения одинаковых (index * [cards.val])