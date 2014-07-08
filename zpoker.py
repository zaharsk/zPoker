from config import *
from game import *
import render as draw

### ### ### Начало создания объектов ### ### ###
cfg = Config()  # Загужаем настройки
gm = Game()  # Создаём новую игру
### ### ### Конец создания объектов ### ### ###

gm.create_table()  # Создаём пустой стол
gm.create_players(cfg.n_of_players, cfg.player_names, cfg.start_bank)
gm.select_dealer()

gm.hand_number = 0

while len(gm.active_players()) > 1:
    gm.hand_number += 1

    gm.give_cards(cfg.deck_suits, cfg.deck_values)

    for state in cfg.game_states:
        gm.change_state(
            state,
            cfg.game_states,
            cfg.start_small_blind,
            cfg.start_big_blind,
            cfg.doubles_blinds,
            cfg.doubles_interval
            )

        draw.desk(gm.tbl, gm.hand_number)
        draw.state_result(state, gm.acts_log)

    draw.hand_result()
    gm.move_dealer()

draw.game_result()
