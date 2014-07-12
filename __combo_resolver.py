def combo_resolver(combo_power):
    combo_power = int(combo_power)
    hex_combo = str(hex(combo_power))[2:]
    cards = [int(card, 16) for card in hex_combo if card != '0']
    if len(hex_combo) < 6:
        combo_id = 0
    else:
        combo_id = cards[0]
        cards = cards[1:]

    return {'combo_id': combo_id, 'cards': cards}


def calc(cards):
    pre_power = ''.join([str(hex(card))[2:] for card in cards])
    if len(pre_power) == 3:
        pre_power += '000'
    power = int(pre_power, 16)

    return power

combo_code = 831488  # Сюда вписывается combo.power
cards = [0, 11, 10]  # Сюда вписывается набор значений карт

print(calc(cards))
print(combo_resolver(combo_code))



"""
min_hq 204800 [0, 3, 2]
max_hq 974009 [0, 14, 13, 12, 11, 9]
 0 [0]
min_op 1187840 [1, 2, 2]
max_op 2026955 [1, 14, 14, 13, 12, 11]
 0 [0]
min_tp 2372386 [2, 4, 3, 3, 2, 2]
max_tp 3075547 [2, 14, 14, 13, 13, 11]
 0 [0]
min_th 3420706 [3, 4, 3, 2, 2, 2]
max_th 4124380 [3, 14, 14, 14, 13, 12]
 0 [0]
min_st 4539169 [4, 5, 4, 3, 2, 1]
max_st 5168314 [4, 14, 13, 12, 11, 10]
 0 [0]
mim_fl 5727554 [5, 7, 6, 5, 4, 2]
max_fl 6216889 [5, 14, 13, 12, 11, 9]
 0 [0]
min_fh 6500898 [6, 3, 3, 2, 2, 2]
max_fh 7270109 [6, 14, 14, 14, 13, 13]
 0 [0]
min_fo 7545378 [7, 3, 2, 2, 2, 2]
max_fo 8318701 [7, 14, 14, 14, 14, 13]
 0 [0]
min_sf 8733473 [8, 5, 4, 3, 2, 1]
min_sf 9362874 [8, 14, 13, 13, 11, 10]
"""
