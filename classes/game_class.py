from .config_class import GameConfig as cfg
from .card_class import Card
from .player_class import Player
import random


class Game(cfg):
    """Класс игры"""
    def __log(self, *args):
        message = ' '.join([str(arg) for arg in args])
        self.log.append(message)

    def __create_players(self):
        self.players = []
        bank = cfg.all_players_bank // cfg.n_of_players
        for x in range(cfg.n_of_players):
            player = Player(bank)
            self.players.append(player)
            self.log.append('Новый игрок: ' + player.name + ' ' + str(player.bank))

    def __select_dealer(self):
        player = random.choice(self.players)
        player.dealer = True
        self.current_player_id = self.players.index(player)
        self.__log('Дилер:', player.name)

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

    def __init__(self):
        super(Game, self).__init__()
        self.log = []
        self.river = []
        self.bank = 0
        self.min_bit = 0
        self.sb = 0
        self.bb = 0
        self.hand_number = 1

        self.states = cfg.states

        self.__create_players()
        self.__select_dealer()
        self.__give_cards()

    def __next_player(self):
        self.current_player_id += 1
        if self.current_player_id == len(self.players):
                self.current_player_id = 0

        skip_list = ['Fold', 'All-in']

        while self.players[self.current_player_id].last_act in skip_list:
            self.current_player_id += 1
            if self.current_player_id == len(self.players):
                self.current_player_id = 0

        next_player = self.players[self.current_player_id]

        return next_player

    def __take_blinds(self):
        if cfg.double_blinds:  # Вычисление блайндов если умножаются
            double_index = (self.hand_number - 1) // cfg.double_blinds_interval  # Делим без остатка номер раздачи (от 0) на промежуток

            self.sb = cfg.start_sb * (2 ** double_index)  # Умножаем стартовый блайнд на 2 в степени double_index
            self.bb = cfg.start_bb * (2 ** double_index)
        else:
            self.sb = cfg.start_sb
            self.bb = cfg.start_bb

        sb_player = self.__next_player()
        act = sb_player.small_blind(self.sb)
        self.bank += act['bit']
        self.__log(sb_player.name, act['name'], act['bit'])

        bb_player = self.__next_player()
        act = bb_player.big_blind(self.bb)
        self.bank += act['bit']
        self.min_bit = self.bb
        self.__log(bb_player.name, act['name'], act['bit'])

    def active_players(self):
        skip_list = ['Fold', 'All-in']

        players = [player for player in self.players if player.last_act not in skip_list]

        return players

    def clear_acts(self, full=False):
        if full:
            for player in self.players:
                player.last_act = 'None'
        else:
            for player in self.players:
                if player.last_act != 'Fold' and player.last_act != 'All-in':
                    player.last_act = 'None'

    def process_the_state(self, state):
        self.__log('-' * 80)
        self.log.append('Начинаем принимать ставки на ' + state)
        self.__log('-' * 80)
        if state == self.states[0]:
            self.__take_blinds()
        elif state == self.states[1]:
            self.river += self.deck.pop()
            self.river += self.deck.pop()
            self.river += self.deck.pop()
            self.__log('На столе', [card.name for card in self.river])
        elif state == self.states[2]:
            self.river += self.deck.pop()
            self.__log('На столе', [card.name for card in self.river])
        elif state == self.states[3]:
            self.river += self.deck.pop()
            self.__log('На столе', [card.name for card in self.river])

        def take_bits():

            while True:

                player = self.__next_player()

                # Если игрок повышал и после него не повышали, выходим
                if player.last_act == 'Raise' and player.last_bit == self.min_bit:
                    self.__log('Ставки приняты. После', player.name, 'никто не повышал.')
                    break

                # Если игрок делал BB, прищуриваемся
                if player.last_act == 'BB':
                    bb_player = True
                else:
                    bb_player = False

                act = player.action(self.players, self.river, self.min_bit, self.bb)
                self.bank += act['bit']

                self.__log(player.name, act['name'], act['bit'])
                self.__log('Банк:', self.bank)

                # Если игрок повысил, повышаем минимальную ставку
                if act['bit'] > self.min_bit:
                    self.min_bit = act['bit']

                # Если игрок после BB не повысил, выходим
                if bb_player and player.last_bit == 0 and self.min_bit == self.bb:
                    self.__log('Ставки приняты. После BB', player.name, 'никто не повышал.')
                    break

                # Проверяем, остались ли игроки для ставок
                if len(self.active_players()) == 1:
                    last_player, = self.active_players()

                    act = last_player.action(self.players, self.river, self.min_bit, self.bb)
                    self.bank += act['bit']

                    self.__log(last_player.name, act['name'], act['bit'])
                    self.__log('Банк:', self.bank)

                    self.__log('Ставки приняты.', last_player.name, 'последний.')
                    break

        take_bits()
        # Записываем в лог результат обработки state
        self.__log('-' * 80)
        self.__log('Результат', state)
        self.__log('-' * 80)
        for player in self.players:
            self.__log(player.name, player.last_act, player.last_bit)

        self.clear_acts()
