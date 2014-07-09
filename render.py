from sys import platform
from os import system


def clear():
    if platform == 'win32':
        system('cls')
    elif platform == 'linux':
        system('clear')
    return None


def desk(tbl, hand_number, min_bit):
    clear()
    dealer, = [plr.name for plr in tbl.players if plr.dealer]
    print('-' * 80)

    print(
        'Раздача', hand_number, '\t',
        'Дилер', dealer
        )

    print('-' * 80)

    print(
        'Банк', tbl.banks[0], '\t',
        'Ставка', min_bit, '\t',
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
            plr.act,
            plr.combo.text
            )

    print('-' * 80)

    return None


def state_result(state, full_log):
    for log in full_log:
        print(log['bits_round'], log['plr'], log['act'], log['bit'])
    message = 'Ставки для ' + str(state) + ' приняты.'
    message += 'Нажмите ENTER, чтобы продолжить.'
    input(message)
    return None


def hand_result(winners):
    if len(winners) == 1:
        print('В раздаче победил', winners[0].name, 'с комбинацией', winners[0].combo.text)
    else:
        print('Банк разделили ' + ', '.join([plr.name for plr in winners]) + ' с комбинацией ', winners[0].combo.text)
    message = 'Нажмите ENTER, чтобы продолжить.'
    input(message)
    return None


def game_result():
    print('Результат игры')
    message = 'Нажмите ENTER, чтобы продолжить.'
    input(message)
    return None
