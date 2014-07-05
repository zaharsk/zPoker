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
        self.tbl.give_blinds()
        return None

    def change_state(self, state):

        def open_cards():
            if state == self.states[0]:
                pass  # Ничего не меняем, по-умолчанию на столе ''
            elif state == self.states[1]:
                self.tbl.cards = self.tbl.cards_pool[:3]  # Открываем первые три карты из пула
            elif state == self.states[2]:
                self.tbl.cards = self.tbl.cards_pool[:4]  # Открываем первые четыре карты из пула
            elif state == self.states[3]:
                self.tbl.cards = self.tbl.cards_pool  # Открываем весь пул
            return None

        self.state = state
        open_cards()
        self.tbl.give_bits()

        return None

    def close_hand(self):
        """
        Закрытие раздачи.
        Подсчёт результатов, удаление проигравших.
        """
