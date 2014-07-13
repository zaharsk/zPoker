from classes import Game


game = Game()

while True:
    game.hand_init()

    for state in game.states:
        game.process_the_state(state)

        if len(game.active_players()) < 2:
            break

    game.hand_result()

    if len(game.players) == 1:
        break

    game.hand_number += 1

    for line in game.log:
        print(line)

    if game.hand_number > 3:
        break
