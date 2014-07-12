from classes import Combo
from classes import Card

c1 = Card(0, 0)
c2 = Card(0, 6)
c3 = Card(0, 5)
c4 = Card(0, 3)
c5 = Card(1, 2)
c6 = Card(1, 1)
c7 = Card(1, 0)

cards = [c1, c2, c3, c4, c5, c6, c7]
cards = sorted(cards, key=lambda card: card.val, reverse=True)

combo = Combo(cards)

print([c.name for c in cards])
print(combo.text)
