import sys
import os

class Render(object):
    """
    Класс отрисовки.
    В будущем должен быть заменён с консольного на графический.
    """
    def __init__(self):
        pass
    
    def clear(self):
        if sys.platform == 'win32':
            os.system('cls')
        elif sys.platform == 'linux':
            os.system('clear')
        return None

    def desk(self, tbl):
        self.clear()

        if tbl.cards:
            tbl_cards = ' '.join([card.name for card in tbl.cards])
        else:
            tbl_cards = ''

        print('-' * 80)
        print(
            'Раздача:', tbl.hand_number, 
            'Дилер:', tbl.players[tbl.index_of_dealer()].name
            )
        print('-' * 80)

        print(
            'На столе:', tbl_cards, '\t',
            'Банк:', tbl.banks[0], '\t',
            'Минимальная ставка:', tbl.bit
            )

        print('-' * 80)
        x = 0
        for plr in tbl.players:
            if plr.dealer:
                d = 'D'
            else:
                d = ' '
            print(
                x,
                '[' + str(plr.bank) + ']',
                plr.name,
                plr.cards[0].name, plr.cards[1].name,
                d,
                plr.act
                )
            x += 1
        print('-' * 80)
        for act in tbl.acts_log:
            print(act[0], act[1])
