from .config_class import GameConfig as cfg
from .card_class import Card
from .player_class import Player


class Game(cfg):
    """Класс игры"""
    def __init__(self, arg):
        super(Game, self).__init__()
        self.arg = arg

    deck = None
    players = None

    def create_players(self):
        players = []
        for x in range(cfg.n_of_players):
            player = Player(x)
            players.append(player)

    def create_deck(self):
        self.deck = []
        for sui in range(len(Card.suits)):
            for val in range(len(Card.vals)):
                c = Card(sui, val)
                self.deck.append(c)
