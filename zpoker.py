from config import *
from table import *
from game import *
import render as draw

### ### ### Начало создания объектов ### ### ###
cfg = Config()
#render = Render()
tbl = Table(
    cfg.n_of_players,
    cfg.start_bank,
    cfg.player_names,
    cfg.deck_suits,
    cfg.deck_values,
    cfg.start_small_blind,
    cfg.start_big_blind,
    cfg.doubles_blinds,
    cfg.doubles_hands
    )
game = Game(tbl, cfg.game_states)
### ### ### Конец создания объектов ### ### ###

def you_loose():
    human = [plr for plr in tbl.players if plr.human][0]  # Если у игрока не осталось денег, заканчиваем игру
    if human.bank == 0:
        return True
    else:
        return False

game.start()
while True:

    plrs_list = [plr for plr in tbl.players if plr.in_game]
    if len(plrs_list) == 1:   # Если в игре остался один, заканчиваем игру
        break

    game.open_hand()

    for state in cfg.game_states:

        if tbl.in_game_players('no_fold') == None or len(tbl.in_game_players('no_fold')) < 2:
            break

        game.change_state(state)
        draw.desk(tbl)
        input('Ставки для '+ state + ' приняты. Нажмите ENTER для продолжения.')

        
    winners = game.close_hand()

    draw.desk(tbl)
    draw.hand(winners)
    input('Нажмите ENTER для продолжения.')

    if you_loose():
        break

    game.move_dealer()
    
if you_loose():
    print('Вы проиграли')
else:
    print('Вы выиграли')