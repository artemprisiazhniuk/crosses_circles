from gameClass import Game
import argparse
import random

parser = argparse.ArgumentParser(description='Management assistant')
parser.add_argument('n', type=str, help='Field size')
parser.add_argument('k', type=str, help='Win condition (number of figures in a row)')
parser.add_argument('mode', type=str, help='Game mode. '
                                           '0 - Player vs Player, '
                                           '1 - Player vs Computer, '
                                           '2 - Computer vs Computer(Simulation)')

args = parser.parse_args()

game = Game(int(args.n), int(args.k), int(args.mode))

if game.mode == 0:
    while not game.win_check(game.field, game.player):
        game.swap_player()
        print('Player {} turn. Put in the coordinates please'.format(game.player))
        x, y = list(map(int, input().split()))
        while not game.make_turn(x, y):
            x, y = list(map(int, input().split()))
        game.display()
    if game.counter == game.n * game.n:
        print('Draw!')
    else:
        print('Player {} wins!'.format(game.player))
elif game.mode == 1:
    player = random.choice([1, 2])
    game.initialize_players(player, 3 - player)
    print('You are player {}'.format(player))
    while not (game.win_check(game.field, game.player) == 1):
        if game.counter >= game.n * game.n:
            break
        game.swap_player()
        if player == game.player:
            print('Your turn. Put in the coordinates please'.format(game.player))
            x, y = list(map(int, input().split()))
            while not game.make_turn(x, y):
                x, y = list(map(int, input().split()))
        else:
            print('Computer\'s turn')
            x, y = game.compute(game.field, game.player)[0]
            game.make_turn(x, y)
        game.display()
        game.counter += 1
    if game.counter == game.n * game.n:
        print('Draw!')
    else:
        print('You {}!'.format('win' * (player == game.player) + 'lose' * (player != game.player)))
else:
    while not game.win_check(game.field, game.player):
        game.swap_player()
        game.swap_roles()
        x, y = game.compute(game.field, game.player)[0]
        game.make_turn(x, y)
        game.display()
    if game.counter == game.n * game.n:
        print('Draw!')
    else:
        print('Player {} wins!'.format(game.player))
