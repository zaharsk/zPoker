class Game(object):
    """
    Класс игры.
    """
    def __init__(self, table):
        self.tbl = table
        
    def start(self):
        self.tbl.create_players()