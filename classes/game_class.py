from .config_class import GameConfig as cfg
from .card_class import Card
from .player_class import Player
import random


class Game(cfg):
    """Класс игры"""
    def __create_players(self):
        self.players = []
        bank = cfg.all_players_bank // cfg.n_of_players
        for x in range(cfg.n_of_players):
            player = Player(x, bank)
            self.players.append(player)
            self.log.append('Новый игрок: ' + player.name)

    def __select_dealer(self):
        player = random.choice(self.players)
        player.dealer = True
        self.current_player_pid = player.pid
        self.log.append('Дилер: ' + player.name)

    def __create_deck(self):
        self.deck = []
        for sui in range(len(Card.suits)):
            for val in range(len(Card.vals)):
                c = Card(sui, val)
                self.deck.append(c)

    def __give_cards(self):
        self.__create_deck()
        random.shuffle(self.deck)
        for player in self.players:
            player.cards = []
            player_card_1 = [self.deck.pop()]
            player_card_2 = [self.deck.pop()]
            player.cards += player_card_1 + player_card_2

    def __next_player(self):
        current_player, = [plr for plr in self.players if plr.pid == self.current_player_pid]
        current_player_id = self.players.index(current_player)

        next_player_id = current_player_id + 1
        if next_player_id == len(self.players):
            next_player_id = 0

        next_player = self.players[next_player_id]
        self.current_player_pid = next_player.pid
        return next_player

    def __init__(self):
        super(Game, self).__init__()
        self.log = []
        self.river = []
        self.bank = 0
        self.min_bit = 0
        self.hand_number = 1

        self.states = cfg.states

        self.__create_players()
        self.__select_dealer()
        self.__give_cards()

    def __take_blinds(self):
        if cfg.double_blinds:  # Вычисление блайндов если умножаются
            double_index = (self.hand_number - 1) // cfg.double_blinds_interval  # Делим без остатка номер раздачи (от 0) на промежуток

            sb = cfg.start_sb * (2 ** double_index)  # Умножаем стартовый блайнд на 2 в степени double_index
            bb = cfg.start_bb * (2 ** double_index)
        else:
            sb = cfg.start_sb
            bb = cfg.start_bb

        sb_player = self.__next_player()
        act = sb_player.action(self.river, 'sb', sb, bb)
        self.bank += act['bit']
        self.log.append(' '.join([sb_player.name, act['name'], str(act['bit'])]))

        bb_player = self.__next_player()
        act = bb_player.action(self.river, 'bb', sb, bb)
        self.bank += act['bit']
        self.log.append(' '.join([bb_player.name, act['name'], str(act['bit'])]))

    def process_the_state(self, state):
        self.log.append('Начинаем принимать ставки на ' + state)
        if state == self.states[0]:
            self.__take_blinds()

        for x in range(len(self.players)):
            player = self.__next_player()
            act = player.action(self.river)
            self.log.append(' '.join([player.name, act['name'], str(act['bit'])]))
