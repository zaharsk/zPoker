from classes import Game


game = Game()

for state in game.states:
    game.process_the_state(state)

    if len(game.active_players()) < 2:
        break

for line in game.log:
    print(line)
