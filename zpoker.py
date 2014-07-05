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

game.start()
game.open_hand()

for state in cfg.game_states:   
    game.change_state(state)
    draw.desk(tbl)
    input('Ставки для '+ state + ' приняты. Нажмите ENTER для продолжения.')

    if tbl.in_game_players('no_fold') == None or len(tbl.in_game_players('no_fold')) < 2:
        break

print('Результат раздачи')