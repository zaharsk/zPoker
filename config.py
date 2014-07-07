import sys

class Config(object):
    """
    Класс настроек. Общий для всех остальных.
    ВАЖНО: Должен быть загружен первым.
    """
    def __init__(self):
        self.game_states = ['pre_flop', 'flop', 'turn', 'river']
        self.n_of_players = 6

        if sys.stdout.encoding == 'cp866':  # Консоль windows
            self.deck_suits = [chr(3), chr(4), chr(5), chr(6)]
        elif sys.stdout.encoding == 'UTF-8':  # unix
            self.deck_suits = [chr(0x2665), chr(0x2666), chr(0x2663), chr(0x2660)]
        elif sys.stdout.encoding == 'cp1251':  # GUI windows
            self.deck_suits = ['H', 'D', 'C', 'S']
        
        self.deck_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.start_bank = 6000  # Общий банк игроков за столом. В начале игры делится поровну
        self.start_small_blind = 50  # Базовая ставка малого блайнда
        self.start_big_blind = 100  # Базовая ставка большого блайнда
        self.player_names = [  # Имена игроков для создания стола
            'Васил',
            'Анна_',
            'Серге',
            'Анаст',
            'Антон',
            'Светл',
            'Пётр_',
            'Дмитр',
            'Вадим',
            'Ольга',
            'Мария',
            'Андре',
            'Алекс']
        self.doubles_blinds = True  # Удваиваивать блайнды
        self.doubles_hands = 10  # Промежуток раздач для удвоения.
