from classes import Combo
from classes import Card


def combo_resolver():
    combo_power = 831488  # Сюда вписывается combo.power
    combo_power = int(combo_power)
    hex_combo = str(hex(combo_power))[2:]
    cards = [int(card, 16) for card in hex_combo if card != '0']
    if len(hex_combo) < 6:
        combo_id = 0
    else:
        combo_id = cards[0]
        cards = cards[1:]

    return combo_id, cards


def calc():
    cards = [0, 12, 10]  # Сюда вписывается набор значений карт
    pre_power = ''.join([str(hex(card))[2:] for card in cards])
    if len(pre_power) == 3:
        pre_power += '000'
    power = int(pre_power, 16)

    return power


def combo_test():
    c1 = Card(1, 0)
    c2 = Card(0, 1)
    c3 = Card(0, 2)
    c4 = Card(1, 3)
    c5 = Card(0, 4)
    c6 = Card(0, 5)
    c7 = Card(1, 6)

    cards = [c1, c2, c3, c4, c5, c6, c7]
    cards = sorted(cards, key=lambda card: card.val, reverse=True)

    combo = Combo(cards)

    return ' '.join([c.name for c in cards]), combo.text

print(combo_resolver())
print(calc())
print(combo_test())
