def combo_resolver(combo):
    combo = int(combo * 100000)
    combo = str(hex(combo))[2:]
    if len(combo) == 5:
        combo_id = 0
        cards = [int(card, 16) for card in combo]
    else:
        combo_id = [int(card, 16) for card in combo][0]
        cards = [int(card, 16) for card in combo][1:]

    return combo_id, cards

combo_code = 75.45379  # Сюда вписывается combo.power
print(combo_resolver(combo_code))
