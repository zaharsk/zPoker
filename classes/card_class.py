from .config_class import CardConfig as cfg


class Card(cfg):
    """Класс одной карты"""
    def __init__(self, sui, val):
        super(Card, self).__init__()
        self.sui = sui
        self.val = val
        self.name = cfg.suits[self.sui] + cfg.vals[self.val]
