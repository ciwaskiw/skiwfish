from game import Game

new_game = Game()

print(new_game)
while True:
    white_move = False
    black_move = False
    while not white_move:
        print("\n" + "White move?")
        white_move = new_game.move(input())
        if white_move:
            print(new_game)
        else:
            print('ILLEGAL MOVE TRY AGAIN!')
    while not black_move:
        print("\n" + "Black move?")
        black_move = new_game.move(input())
        if black_move:
            print(new_game)
        else:
            print('ILLEGAL MOVE TRY AGAIN!')


