import sys
import os

def clear():
    if sys.platform == 'win32':
        os.system('cls')
    elif sys.platform == 'linux':
        os.system('clear')
    return None

def desk(tbl):
    clear()

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
        if plr.in_game:
        ###
            if plr.dealer:
                d = 'D'
            else:
                d = ' '
            print(
                x,
                '[' + str(plr.bank) + ']',
                plr.name,
                ' '.join([c.name for c in plr.cards]),
                d,
                plr.act,
                plr.combo.text
                )
        ###
        x += 1
    print('-' * 80)
    for plr in tbl.players:
        if plr.human:
            print(
                'Ваши карты ' + ' '.join([c.name for c in plr.cards]),
                '\t',
                plr.combo.text
                )
    print('-' * 80)
    for act in tbl.acts_log:
        print(act[0], act[1])
    print('-' * 80)

def hand(winners):
    #clear()
    if len(winners) == 1:
        print('В раздаче победил', winners[0].name)
    else:
        print('Банк разделили ' + ' '.join([plr.name for plr in winners]))
