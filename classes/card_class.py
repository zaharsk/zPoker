from .config_class import CardConfig as cfg


class Card(cfg):
    """Класс одной карты"""
    def __init__(self, sui, val):
        super(Card, self).__init__()
        self.sui = sui
        self.val = val + 2
        self.name = cfg.suits[self.sui] + cfg.vals[self.val - 2]

if __name__ == '__main__':
    main()
