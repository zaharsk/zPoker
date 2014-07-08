import copy


class Combo(object):
    """
    Класс комбинации игрока.
    При проверке комбинаций выбирается старшая и записывается в атрибут объекта
    класса Player.
    """
    def __init__(self, all_cards, state):
        self.index = None
        self.cards = []
        self.text = None
        self.power = None  # "Сила" комбинации для сравнения одинаковых
        self.rel_power = None

        self.all_cards = all_cards
        self.state = state

        def test_cards(all_cards):
            plr_pool = sorted(all_cards, key=lambda card: card.val)
            # Создаём полную копию пула дял работы с тузами
            ace_plr_pool = copy.deepcopy(plr_pool)
            for card in ace_plr_pool:
                if card.val == 12:
                    card.val = -1

            ace_plr_pool = sorted(ace_plr_pool, key=lambda card: card.val)

            vals = [card.val for card in plr_pool]

            def calc_power(cards, combo):
                if combo == 'high_card':
                    i = 0
                    p_max = 264561

                elif combo == 'one_pair':
                    i = 1
                    p_max = 271008

                elif combo == 'two_pairs':
                    i = 2
                    p_max = 271030

                elif combo == 'three':
                    i = 3
                    p_max = 271427

                elif combo == 'straight':
                    i = 4
                    p_max = 264562

                elif combo == 'flush':
                    i = 5
                    p_max = 264561

                elif combo == 'full_house':
                    i = 6
                    p_max = 271428

                elif combo == 'four':
                    i = 7
                    p_max = 271451

                elif combo == 'straight_flush':
                    i = 8
                    p_max = 264562

                pos = 0
                res = 0
                for val in [c.val for c in cards]:
                    pos += 1
                    res += val ** pos

                return {
                    'index': i,
                    'val': res,
                    'rel_val': i + res / (p_max + 1)
                    }

            def high_card():
                self.cards = plr_pool[-5:]
                self.text = 'Старшая карта ' + ' '.join([c.name for c in self.cards])
                power = calc_power(self.cards, 'high_card')
                self.index = power['index']
                self.power = power['val']
                self.rel_power = power['rel_val']
                return None

            def pairs():
                temp_pool = copy.deepcopy(plr_pool)  # Создаём временный пул для формирования комбинации

                res = [card for card in plr_pool if vals.count(card.val) == 2]  # Проверяем все карты, которые встречаются дважды

                if len(res) == 2:  # Если получили две карты, то у нас одна пара

                    for card in temp_pool:
                        if card.name == res[0].name:
                            temp_pool.remove(card)  # Удаляем карты из пула, чтобы получить старшие без пар
                    for card in temp_pool:
                        if card.name == res[1].name:
                            temp_pool.remove(card)  # Удаляем карты из пула, чтобы получить старшие без пар

                    temp_pool = temp_pool[-3:]

                    for card in plr_pool:
                        if card.name in [c.name for c in temp_pool]:
                            res.append(card)

                    self.cards = sorted(res, key=lambda card: card.val)
                    self.text = 'Пара ' + ' '.join([c.name for c in self.cards])
                    power = calc_power(self.cards, 'one_pair')
                    self.index = power['index']
                    self.power = power['val']
                    self.rel_power = power['rel_val']

                if len(res) == 4 or len(res) == 6:
                    for card in temp_pool:
                        if card.name == res[-3].name:
                            temp_pool.remove(card)
                    for card in temp_pool:
                        if card.name == res[-4].name:
                            temp_pool.remove(card)
                    for card in temp_pool:
                        if card.name == res[-1].name:
                            temp_pool.remove(card)
                    for card in temp_pool:
                        if card.name == res[-2].name:
                            temp_pool.remove(card)

                    temp_pool = temp_pool[-1:]

                    for card in plr_pool:
                        if card.name in [c.name for c in temp_pool]:
                            res.append(card)

                    self.cards = sorted(res, key=lambda card: card.val)
                    self.text = 'Две пары ' + ' '.join([c.name for c in self.cards])
                    power = calc_power(self.cards, 'two_pairs')
                    self.index = power['index']
                    self.power = power['val']
                    self.rel_power = power['rel_val']
                del temp_pool

            def three():
                if self.state == 'pre_flop':  # Невозможно на pre_flop
                    return None

                temp_pool = copy.deepcopy(plr_pool)  # Создаём временный пул для формирования комбинации

                res = [card for card in plr_pool if vals.count(card.val) == 3]  # Проверяем все карты, которые встречаются трижды

                if res:  # Если что-то получили в результате

                    for card in temp_pool:
                        if card.name == res[0].name:
                            temp_pool.remove(card)
                    for card in temp_pool:
                        if card.name == res[1].name:
                            temp_pool.remove(card)
                    for card in temp_pool:
                        if card.name == res[2].name:
                            temp_pool.remove(card)
                    temp_pool = temp_pool[-2:]

                    for card in plr_pool:
                        if card.name in [c.name for c in temp_pool]:
                            res.append(card)

                    self.cards = sorted(res, key=lambda card: card.val)
                    self.text = 'Тройка ' + ' '.join([c.name for c in self.cards])
                    power = calc_power(self.cards, 'three')
                    self.index = power['index']
                    self.power = power['val']
                    self.rel_power = power['rel_val']

                del temp_pool

                return None

            def straight_flush():

                def test_sf(cards):
                    straight = True
                    flush = True

                    i = 0
                    while i < 4:
                        straight = straight and cards[i].val + 1 == cards[i + 1].val
                        flush = flush and cards[i].sui == cards[i + 1].sui
                        i += 1
                    return {'straight': straight, 'flush': flush, 'cards': cards}

                if self.state == 'pre_flop':  # Невозможно на pre_flop
                    return None

                res = []

                res.append(test_sf(plr_pool[:5]))
                if self.state == 'turn':
                    res.append(test_sf(plr_pool[1:6]))
                elif self.state == 'river':
                    res.append(test_sf(plr_pool[1:6]))
                    res.append(test_sf(plr_pool[2:7]))

                if 12 in vals:

                    res.append(test_sf(ace_plr_pool))
                    if self.state == 'turn':
                        res.append(test_sf(ace_plr_pool[:5]))
                        res.append(test_sf(ace_plr_pool[1:6]))
                    elif self.state == 'river':
                        res.append(test_sf(ace_plr_pool[:5]))
                        res.append(test_sf(ace_plr_pool[1:6]))
                        res.append(test_sf(ace_plr_pool[2:7]))

                for result in res:
                    if result['straight'] or result['flush']:
                        if result['straight'] and result['flush']:
                            self.cards = sorted(result['cards'], key=lambda card: card.val)
                            self.text = 'Стрит - флеш ' + ' '.join([c.name for c in self.cards])
                            power = calc_power(self.cards, 'straight_flush')

                        if result['straight']:
                            self.cards = sorted(result['cards'], key=lambda card: card.val)
                            self.text = 'Стрит' + ' '.join([c.name for c in self.cards])
                            power = calc_power(self.cards, 'straight')

                        if result['flush']:
                            self.cards = sorted(result['cards'], key=lambda card: card.val)
                            self.text = 'Флеш ' + ' '.join([c.name for c in self.cards])
                            power = calc_power(self.cards, 'flush')

                        self.index = power['index']
                        self.power = power['val']
                        self.rel_power = power['rel_val']
                return None

            def full_house():
                if self.state == 'pre_flop':  # Невозможно на pre_flop
                    return None

                if self.index != 8:  # Проверяем, нет ли стрит-флеша, чтобы не перезаписать
                    return None
                temp_pool = copy.deepcopy(plr_pool)

                three_res = [card for card in temp_pool if vals.count(card.val) == 3]  # Выбираем все карты, которые встречаются трижды

                if three_res:  # Если что-то получили в результате
                    for card in temp_pool:
                        if card.name in [c.name for c in three_res[-3:]]:
                            temp_pool.remove(card)

                        two_res = [card for card in temp_pool if vals.count(card.val) == 2]  # Выбираем все карты, которые встречаются дважды

                        if two_res:  # Если что-то получили в результате
                            self.cards = plr_pool
                            self.text = 'Фул-хаус ' + ' '.join([c.name for c in self.cards])
                            power = calc_power(self.cards, 'full_house')
                            self.index = power['index']
                            self.power = power['val']
                            self.rel_power = power['rel_val']

                return None

            def four():
                if self.state == 'pre_flop':  # Невозможно на pre_flop
                    return None

                if self.index != 8:  # Проверяем, нет ли стрит-флеша, чтобы не перезаписать
                    return None

                res = [card for card in plr_pool if vals.count(card.val) == 4]  # Выбираем все карты, которые встречаются четыре раза

                if res:
                    temp_pool = copy.deepcopy(plr_pool)
                    for card in temp_pool:
                        if card.name == res[0].name:
                            temp_pool.remove(card)
                    for card in temp_pool:
                        if card.name == res[1].name:
                            temp_pool.remove(card)
                    for card in temp_pool:
                        if card.name == res[2].name:
                            temp_pool.remove(card)
                    for card in temp_pool:
                        if card.name == res[3].name:
                            temp_pool.remove(card)
                    temp_pool = temp_pool[-1:]

                    for card in plr_pool:
                        if card.name in [c.name for c in temp_pool]:
                            res.append(card)

                    self.cards = sorted(res, key=lambda card: card.val)
                    self.text = 'Сет ' + ' '.join([c.name for c in self.cards])
                    power = calc_power(self.cards, 'four')
                    self.index = power['index']
                    self.power = power['val']
                    self.rel_power = power['rel_val']

            high_card()
            pairs()
            three()
            straight_flush()
            full_house()
            four()

            return None

        test_cards(all_cards)
