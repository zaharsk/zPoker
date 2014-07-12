from .config_class import ComboConfig as cfg
import copy


class Combo(cfg):
    """docstring for Combo"""
    def test_cards(self, pool):
        normal_pool = sorted(pool, key=lambda card: card.val, reverse=True)
        flash_pool = sorted(pool, key=lambda card: card.sui, reverse=True)

        pool_vals = [card.val for card in normal_pool]

        if 14 in pool_vals:
            ace_pool = copy.deepcopy(pool)
            for card in ace_pool:
                if card.val == 14:
                    card.val = 1
            ace_pool = sorted(ace_pool, key=lambda card: card.val, reverse=True)

        result = {}

        def put_result():
            self.cards = result['cards']

            cards_names = ' '.join([card.name for card in result['cards']])
            self.text = result['text'] + cards_names

            pre_power = ''.join([str(hex(card.val))[2:] for card in self.cards])

            if len(pre_power) == 2:
                pre_power += '000'

            power_0x = str(result['combo_index']) + pre_power

            self.power = int(power_0x, 16)

        def high_card():
            if self.power > 0:
                return None
            result['cards'] = normal_pool[:5]
            result['text'] = 'Старшая карта '
            result['combo_index'] = 0

            put_result()

        def one_pair():
            if self.power > 1:
                return None
            res = [card for card in normal_pool if pool_vals.count(card.val) == 2]
            print('op', [c.name for c in res], len(res))
            if len(res) == 2:
                cards = normal_pool[:5]
                x = 0
                while res[0] not in cards and res[1] not in cards:
                    cards = normal_pool[x:5+x]
                    x += 1

                result['cards'] = cards
                result['text'] = 'Одна пара '
                result['combo_index'] = 1

                put_result()

        def two_pairs():
            if self.power > 2:
                return None
            res = [card for card in normal_pool if pool_vals.count(card.val) == 2][:4]
            print('tp', [c.name for c in res], len(res))
            if len(res) == 4:
                cards = normal_pool[:5]
                x = 0
                while res[0] not in cards and res[1] not in cards and res[2] not in cards and res[3] not in cards:
                    cards = normal_pool[x:5+x]
                    x += 1

                result['cards'] = cards
                result['text'] = 'Две пары '
                result['combo_index'] = 2

                put_result()

        two_pairs()
        one_pair()
        high_card()

    def __init__(self, pool):
        super(Combo, self).__init__()
        self.pool = pool
        self.power = 0
        self.text = ''
        self.cards = []
        self.test_cards(pool)
