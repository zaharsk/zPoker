from config import Cards_config as cfg


class Card(cfg):
    """docstring for Card"""
    def __init__(self, sui, val):
        super(Card, self).__init__()
        self.sui = sui
        self.val = val
        self.name = cfg.suits[self.sui] + cfg.vals[self.val]
