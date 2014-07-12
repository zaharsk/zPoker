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

        def high_card():
            result['cards'] = normal_pool[:5]
            result['text'] = 'Старшая карта '
            result['combo_index'] = 0

        high_card()

        self.cards = result['cards']

        cards_names = ' '.join([card.name for card in result['cards']])
        self.text = result['text'] + cards_names

        pre_power = ''.join([str(hex(card.val))[2:] for card in self.cards])

        if len(pre_power) == 2:
            pre_power += '000'

        power_0x = str(result['combo_index']) + pre_power

        self.power = int(power_0x, 16)/100000

    def __init__(self, pool):
        super(Combo, self).__init__()
        self.pool = pool
        self.power = 0
        self.text = ''
        self.cards = []
        self.test_cards(pool)
