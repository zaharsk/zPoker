from classes import Game


game = Game()

for state in game.states:
    game.process_the_state(state)

for line in game.log:
    print(line)
