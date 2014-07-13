from classes import game_class
game = game_class.Game()


def show_log():
    x = 0
    for line in game.log:
        print(x, line)
        x += 1
    game.log = []

while True:
    game.hand_init()

    game.process_hand()

    game.hand_result()

    if len(game.with_bank_plrs()) == 1:
        break

    game.hand_number += 1

show_log()  # Debug

winner, = game.plrs

print(winner.name, winner.bank)
