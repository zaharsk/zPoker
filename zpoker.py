from classes import game_class
game = game_class.Game()


def show_log():
    for x, line in enumerate(game.log):
        print(x, line)
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
