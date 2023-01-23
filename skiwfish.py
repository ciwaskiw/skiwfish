from game import Game

new_game = Game()

print(new_game)
while not new_game.move_tree.checkmate:
    white_move = False
    black_move = False
    while not white_move:
        print("\nLegal Moves For White: " + str(new_game.move_tree.get_san_move_list()))
        print("\n" + "White move?")
        white_move = new_game.move('engine')#input())
        if white_move:
            print(new_game)
            pass
        else:
            print('ILLEGAL MOVE TRY AGAIN!')
    while not black_move and not new_game.move_tree.checkmate:
        print("\nLegal Moves For Black: " + str(new_game.move_tree.get_san_move_list()))
        print("\n" + "Black move?")
        black_move = new_game.move('random')#input())
        if black_move:
            print(new_game)
            pass
        else:
            print('ILLEGAL MOVE TRY AGAIN!')
print("CHECK MATE!!!!!")
print(new_game)
if new_game.move_tree.wtm:
    print("BLACK WINS!!!!")
else:
    print("WHITE WINS!!!!")


