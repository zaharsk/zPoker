from config import *
from table import *
from game import *
from render import *

cfg = Config()
render = Render()
tbl = Table(cfg.n_of_players, cfg.start_bank, cfg.player_names)
game = Game(tbl)

game.start()

render.desk(tbl)