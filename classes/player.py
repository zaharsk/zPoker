from .config_class import PlayerConfig as cfg


class Player(cfg):
    """docstring for PLayer"""
    def __init__(self, id_num, bank):
        super(Player, self).__init__()
        self.id_num = id_num
        self.bank = bank
