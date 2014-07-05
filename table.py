from random import *
from player import *
from card import *
from render import desk as render_desk

class Table(object):
    """
    Класс игрового стола.
    Объединяет все игровые объекты: игроков, карты, блайнды, банк и т.д. Все 
    манипуляции с объектами осуществляются в классе Game.
    """
    def __init__(
            self,
            n_of_players,
            start_bank,
            player_names,
            deck_suits,
            deck_values,
            start_small_blind,
            start_big_blind,
            doubles_blinds,
            doubles_hands
            ):
        self.banks = [0]  # Сумма ставок на столе в текущей раздаче
        self.cards_pool = None  # Карты, выбранные для раздчи
        self.cards = None  # Открыте карты
        self.players = []  # Массив игроков
        self.bit = None  # Минимальная ставка
        self.hand_number = 0  # Номер раздачи
        self.sb = 0  # Малый блайнд
        self.bb = 0  # Большой блайнд
        self.acts_log = []
        self.raise_log = False

        self.n_of_players = n_of_players
        self.start_bank = start_bank
        self.player_names = player_names
        self.deck_suits = deck_suits
        self.deck_values = deck_values
        self.start_sb = start_small_blind
        self.start_bb = start_big_blind
        self.doubles_blinds = doubles_blinds
        self.doubles_hands = doubles_hands

    def create_players(self):
        """
        Проверяем настройки и создаём игроков.
        """
        if self.n_of_players < 2: self.n_of_players = 2
        if self.n_of_players > 6: self.n_of_players = 6

        plrs_bank = self.start_bank // self.n_of_players


        for x in range(self.n_of_players):  # Создаём игроков
            name_index = randint(0, len(self.player_names) - 1)
            plr_name = self.player_names[name_index]
            self.player_names.remove(plr_name)

            self.players.append(Player(plr_name, plrs_bank))

        human_index = randint(0, len(self.players) - 1)
        self.players[human_index].human = True

        user_name = input('Введите Ваше имя [Игрок]:')

        if user_name:
            self.players[human_index].name = user_name
        else:
            self.players[human_index].name = 'Игрок'

        return None

    def select_dealer(self):
        """
        Случайным образом выбираем дилера в начале игры.
        """
        dealer_index = randint(0, self.n_of_players - 1)
        self.players[dealer_index].dealer = True
        self.act_player = dealer_index
        return None

    def index_of_dealer(self):
        """
        Определяем, какой игрок является дилером.
        """
        for plr in self.players:
            if plr.dealer:
                return self.players.index(plr)


    def in_game_players(self, no_fold=False):
        if no_fold:
            plrs_list = [plr for plr in self.players if plr.in_game and plr.act != 'Fold' and plr.act != 'All-in']
        else:
            plrs_list = [plr for plr in self.players if plr.in_game]

        if len(plrs_list) < 2:
            return None

        return plrs_list

    def next_act_player(self, bit=False):
        """
        Выбираем следующего игрока для действия.
        """
        self.act_player += 1

        if self.act_player == len(self.players):
                self.act_player = 0

        if bit:
            in_game_list = self.in_game_players('no_fold')
        else:
            in_game_list = self.in_game_players()

        while self.players[self.act_player] not in in_game_list:
            self.act_player += 1

            if self.act_player == len(self.players):
                self.act_player = 0

        return self.players[self.act_player]

    def clear_log(self):
        """
        Очищаем лог раздачи.
        """
        self.acts_log = []
        return None

    def clear_acts(self, full=False):
        """
        Очищаем действия игроков. Полностью или только текущие без истории.
        """
        for plr in self.players:
            if full:
                plr.act = ''
            else:
                if plr.act != 'Fold' and plr.act != 'All-in':
                    plr.act = ''
        return None

    def take_cards(self):
        """
        Раздаём карты.
        """

        def create_deck():
            """
            Создаём колоду.
            """

            def random_card():
                """
                Выбираем случайную карту.
                """
                sui = randint(0, len(self.deck_suits) - 1)
                val = randint(0, len(self.deck_values) - 1)
                name = self.deck_suits[sui] + self.deck_values[val]

                rnd_card = Card(sui, val, name)
                return rnd_card

            n_of_cards = 5 + 2 * len(self.players)

            self.cards_pool = []
            self.cards = []

            new_card = random_card()

            for i in range(n_of_cards):
                # Test with name cause may be 2 diff obj with same attrs
                while new_card.name in [card.name for card in self.cards_pool]:
                    new_card = random_card()
                self.cards_pool.append(new_card)
            return None

        create_deck()

        for plr in self.players:
            plr.cards = self.cards_pool[:2]
            self.cards_pool = self.cards_pool[2:]
        return None

    def give_blinds(self):
        if self.doubles_blinds:  # Вычисление блайндов если умножаются
            double_index = (self.hand_number - 1) // self.doubles_hands  # Делим без остатка номер раздачи (от 0) на промежуток

            self.sb = self.start_sb * (2 ** double_index)  # Умножаем стартовый блайнд на 2 в степени double_index
            self.bb = self.start_bb * (2 ** double_index)

        sb_player = self.next_act_player()

        if sb_player.bank > self.sb:
            plr_sb = self.sb
            sb_player.bank -= self.sb
        else:
            plr_sb = sb_player.bank
            sb_player.bank = 0

        sb_player.act = 'SB ' + str(plr_sb)
        self.acts_log.append([sb_player.name, sb_player.act])

        bb_player = self.next_act_player()

        if bb_player.bank > self.bb:
            plr_bb = self.bb
            bb_player.bank -= self.bb
        else:
            plr_bb = bb_player.bank
            bb_player.bank = 0

        bb_player.act = 'BB ' + str(plr_bb)
        self.acts_log.append([bb_player.name, bb_player.act])

        self.banks[0] = plr_sb + plr_bb

        self.bit = self.bb

    def human_bit(self, plr):

        def take_act():
            human_act = input(
                'Check: e\n' + 
                'Fold: f\n' + 
                'Call: c\n' + 
                'Rise: новая ставка (число)\n' + 
                'Ваша ставка[c]:'
                )
            return human_act

        render_desk(self)

        act = take_act()

        if act == '':
            act_res = plr.do_call(self.banks[0], self.bit)

        return act_res


    def give_bits(self, state, states):
        self.acts_log.append(['--- ---', '---'])
        acts = []
        if state != states[0] and not self.raise_log:
            self.clear_log()
            self.clear_acts()

        for player in self.in_game_players():

            if self.in_game_players('no_fold') == None:
                break

            plr = self.next_act_player('bit')

            if plr.human:
                act = self.human_bit(plr)
            else:

                # [Start] Принятие решение о действии компьютерным игроком
                if plr.bank >= self.bit + self.bb:
                    plr_act = randint(1, 3)
                else:
                    plr_act = randint(1, 2)

                if plr_act == 0:
                    act = plr.do_check(self.banks[0], self.bit)
                elif plr_act == 1:
                    act = plr.do_fold(self.banks[0], self.bit)
                elif plr_act == 2:
                    act = plr.do_call(self.banks[0], self.bit)
                elif plr_act == 3:
                    act = plr.do_raise(self.banks[0], self.bit + self.bb)
                    self.bit = act['bit']
                # [End] Принятие решение о действии компьютерным игроком



            self.banks[0] += act['bit']
            self.acts_log.append([plr.name, plr.act])
            acts.append(plr.act)

            #self.clear_acts()
            

        acts = [log[:5] for log in acts]
        print(act)

        if 'Raise' in acts:
            self.raise_log = True
            self.give_bits(state, states)
            self.raise_log = False

        self.bit = self.bb  # Возвращаем минимальную ставку на большой блайнд
        self.act_player = self.index_of_dealer()  # Ставим активного игрока на дилера

        return None
            