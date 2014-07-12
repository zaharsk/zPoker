def calc(combo):
    cards = combo['cards']
    pre_power = ''.join([str(hex(card))[2:] for card in cards])
    if len(pre_power) == 3:
        pre_power += '000'
    power = int(pre_power, 16)

    print(combo['name'], power, power/100000, combo['cards'])

combos = [
    {'name': 'min_hq', 'cards': [0, 3, 2]},
    {'name': 'max_hq', 'cards': [0, 14, 13, 12, 11, 9]},
    {'name': '', 'cards': [0]},

    {'name': 'min_op', 'cards': [1, 2, 2]},
    {'name': 'max_op', 'cards': [1, 14, 14, 13, 12, 11]},
    {'name': '', 'cards': [0]},

    {'name': 'min_tp', 'cards': [2, 4, 3, 3, 2, 2]},
    {'name': 'max_tp', 'cards': [2, 14, 14, 13, 13, 11]},
    {'name': '', 'cards': [0]},

    {'name': 'min_th', 'cards': [3, 4, 3, 2, 2, 2]},
    {'name': 'max_th', 'cards': [3, 14, 14, 14, 13, 12]},
    {'name': '', 'cards': [0]},

    {'name': 'min_st', 'cards': [4, 5, 4, 3, 2, 1]},
    {'name': 'max_st', 'cards': [4, 14, 13, 12, 11, 10]},
    {'name': '', 'cards': [0]},

    {'name': 'mim_fl', 'cards': [5, 7, 6, 5, 4, 2]},
    {'name': 'max_fl', 'cards': [5, 14, 13, 12, 11, 9]},
    {'name': '', 'cards': [0]},

    {'name': 'min_fh', 'cards': [6, 3, 3, 2, 2, 2]},
    {'name': 'max_fh', 'cards': [6, 14, 14, 14, 13, 13]},
    {'name': '', 'cards': [0]},

    {'name': 'min_fo', 'cards': [7, 3, 2, 2, 2, 2]},
    {'name': 'max_fo', 'cards': [7, 14, 14, 14, 14, 13]},
    {'name': '', 'cards': [0]},

    {'name': 'min_sf', 'cards': [8, 5, 4, 3, 2, 1]},
    {'name': 'min_sf', 'cards': [8, 14, 13, 13, 11, 10]},
]

for combo in combos:
    calc(combo)
