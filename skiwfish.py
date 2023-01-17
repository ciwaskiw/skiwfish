def get_san_square(x,y):
    return chr(x + 97) + str(y+1)

def generate_legal_move(from_x, from_y, to_x, to_y, piece):
    from_piece = piece
    print(piece + ' to ' + get_san_square(to_x,to_y))
    pass

class Game():
    board = [
        ['R','N','B','Q','K','B','N','R'],
        ['P','P','P','P','P','P','P','P'],
        ['-','-','-','-','-','-','-','-'],
        ['-','-','-','-','-','-','-','-'],
        ['-','-','-','-','-','-','-','-'],
        ['-','-','-','-','-','-','-','-'],
        ['p','p','p','p','p','p','p','p'],
        ['r','n','b','q','k','b','n','r']
    ]
    white_to_move = True

    def get(self, x,y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return '0'
        else:
            return self.board[y][x]

    def find_all_legal_moves(self):
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if self.white_to_move:
                    #White pawns
                    if piece == 'P':
                        white_pawn_moves(self,x,y,piece)
                    if piece == 'R':
                        rook_moves(self,x,y,piece)
                else:
                    #Black pawns
                    if piece == 'p':
                        black_pawn_moves(self,x,y,piece)
                    if piece == 'r':
                        rook_moves(self,x,y,piece)

def is_available(square, white_to_move):
    if white_to_move:
        return square == '-' or square.islower()
    else:
        return square == '-' or square.isupper()

def rook_moves(game,x,y,piece):
    get, wtm = game.get, game.white_to_move
    #check direction right
    for x_scan in range(x+1,8):
        print(get_san_square(x_scan,y))
        if is_available(get(x_scan,y),wtm):
            generate_legal_move(x,y,x_scan,y,piece)
        else:
            break
    #check direction left
    for x_scan in range(7,x-1,-1):
        print(get_san_square(x_scan,y))
        if is_available(get(x_scan,y),wtm):
            generate_legal_move(x,y,x_scan,y,piece)
        else:
            break
    #check direction up
    for y_scan in range(y+1,8):
        if is_available(get(x_scan,y),wtm):
            generate_legal_move(x,y,x,y_scan,piece)
        else:
            break
    #check direction down
    for y_scan in range(7,y-1,-1):
        if is_available(get(x,y_scan),wtm):
            generate_legal_move(x,y,x,y_scan,piece)
        else:
            break


def white_pawn_moves(game,x,y,piece):
    get = game.get
    #Advance 1 square
    if get(x,y+1) == '-':
        generate_legal_move(x,y,x,y+1,piece)
        #Advance 2 squares
        if get(x,y+2) == '-' and y == 1:
            generate_legal_move(x,y,x,y+2,piece)
    #Capture
    if get(x+1,y+1).islower():
        generate_legal_move(x,y,x+1,y+1,piece)
    if get(x-1,y+1).islower():
        generate_legal_move(x,y,x-1,y+1,piece)

def black_pawn_moves(game,x,y,piece):
    get = game.get
    #Advance 1 square
    if get(x,y-1) == '-':
        generate_legal_move(x,y,x,y-1,piece)
        #Advance 2 squares
        if get(x,y-2) == '-' and y == 6:
            generate_legal_move(x,y,x,y-2,piece)
    #Capture
    if get(x+1,y-1).isupper():
        generate_legal_move(x,y,x+1,y-1,piece)
    if get(x-1,y-1).isupper():
        generate_legal_move(x,y,x-1,y-1,piece)

new_game = Game()

new_game.find_all_legal_moves()

