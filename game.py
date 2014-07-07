from random import *

class Game(object):
    """
    Класс игры.
    """
    def __init__(self, table, states):
        self.state = None
        self.tbl = table
        self.states = states
        
    def start(self):
        """
        Инициализация новой игры.
        """
        self.tbl.create_players()
        self.tbl.select_dealer()
        return None

    def open_hand(self):
        """
        Открытие раздачи.
        """
        self.tbl.hand_number += 1
        self.tbl.take_cards()
        self.tbl.give_blinds()  # На pre_flop собираем блайнды
        
        return None

    def change_state(self, state):


        def open_cards():
            if state == self.states[0]:
                pass
            elif state == self.states[1]:
                self.tbl.cards = self.tbl.cards_pool[:3]  # Открываем первые три карты из пула
            elif state == self.states[2]:
                self.tbl.cards = self.tbl.cards_pool[:4]  # Открываем первые четыре карты из пула
            elif state == self.states[3]:
                self.tbl.cards = self.tbl.cards_pool  # Открываем весь пул
            return None

        self.state = state
        open_cards()

        self.tbl.check_combos(self.state)

        self.tbl.give_bits(state, self.states)

        self.tbl.bit = self.tbl.bb  # Возвращаем минимальную ставку на большой блайнд
        self.tbl.act_player = self.tbl.index_of_dealer()  # Ставим активного игрока на дилера
        self.tbl.clear_bits()  # Обнуляем историю ставок в конце раздачи
        self.tbl.clear_log()  # Очищаем лог в конце раздачи
        #self.tbl.clear_acts()  # Очищаем действия игроков в конце раздачи

        
        return None

    def close_hand(self):
        """
        Закрытие раздачи.
        Подсчёт результатов, удаление проигравших.
        """
        def select_winner():
            if self.tbl.in_game_players('no_fold') == None:
                for plr in self.tbl.players:
                    if plr.act != 'Fold':
                        return [plr]

            combo_indexes = [plr.combo.index for plr in self.tbl.in_game_players('no_fold')]

            winners = [plr for plr in self.tbl.in_game_players('no_fold') if plr.combo.index == max(combo_indexes)]

            if len(winners) == 1:
                return winners[0]
            else:
                powers = [plr.combo.power for plr in winners]

                winners = [plr for plr in winners if plr.combo.power == max(powers)]

                return winners

            return self.tbl.players[winner_index]  # Возвращаем игрока - победителя

        def remove_loosers():
            for plr in self.tbl.players:
                if plr.bank == 0:
                    plr.in_game = False
            return None

        winners = select_winner()
        

        if len(winners) == 1:
            winners[0].bank += self.tbl.banks[0]
        else:
            for plr in winners:
                plr.bank += self.tbl.banks[0] // len(winners)

        self.tbl.banks[0] = 0

        remove_loosers()
        
        self.tbl.clear_log()
        self.tbl.clear_acts('full')
        self.tbl.clear_bits()

        return winners

    def move_dealer(self):
        self.tbl.move_dealer()

        return None