class Combo(object):
    """docstring for Combo"""
    def __init__(self, index, name, cards, text):
        self.index = index
        self.name = name
        self.cards = cards
        self.text = text
        self.power = 0  # "Сила" комбинации для сравнения одинаковых (index * [cards.val])