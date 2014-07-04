import sys
import os

class Render(object):
    """
    Класс отрисовки.
    В будущем должен быть заменён с консольного на графический.
    """
    def __init__(self):
        pass
    
    def clear(self):
        if sys.platform == 'win32':
            os.system('cls')
        elif sys.platform == 'linux':
            os.system('clear')
        return None

    def desk(self, tbl):
        self.clear()
        print('-' * 80)
        for plr in tbl.players:
            print(
                '[' + str(plr.bank) + ']',
                plr.name
                )
        print('-' * 80)
