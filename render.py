from sys import platform
from os import system


def clear():
    if platform == 'win32':
        system('cls')
    elif platform == 'linux':
        system('clear')
    return None


def desk(tbl, hand_number):
    clear()
    print('-' * 80)

    print(
        'Раздача', hand_number,
        ' '.join([card.name for card in tbl.cards])
        )

    print('-' * 80)

    for plr in tbl.players:
        if plr.dealer:
            d = 'D'
        else:
            d = ' '

        print(
            plr.index,
            plr.bank,
            plr.name,
            d,
            ' '.join([card.name for card in plr.cards]),
            plr.act
            )

    print('-' * 80)

    return None


def state_result(state, acts_log):
    for act in acts_log:
        print(act['plr'], act['act'])
    message = 'Ставки для ' + str(state) + ' приняты.'
    message += 'Нажмите ENTER, чтобы продолжить.'
    input(message)
    return None


def hand_result():
    print('Результат раздачи')
    message = 'Нажмите ENTER, чтобы продолжить.'
    input(message)
    return None


def game_result():
    print('Результат игры')
    message = 'Нажмите ENTER, чтобы продолжить.'
    input(message)
    return None


def hand(winners):
    #clear()
    if len(winners) == 1:
        print('В раздаче победил', winners[0].name)
    else:
        print('Банк разделили ' + ' '.join([plr.name for plr in winners]))
