import copy
from util import scan

def get_san_square(x,y):
    return chr(y + 97) + str(x+1)

class Game():
    board = [
        ['R','N','B','Q','K','B','N','R'],
        ['-','P','P','P','P','P','P','P'],
        ['-','-','-','-','-','-','-','-'],
        ['-','-','-','-','-','-','-','-'],
        ['-','-','-','-','-','-','-','-'],
        ['-','-','-','-','-','-','-','-'],
        ['p','p','p','p','p','p','p','p'],
        ['r','n','b','q','k','b','n','r']
    ]
    legal_moves = {}
    white_to_move = True

    def __init__(self):
        self.find_all_legal_moves()

    def __str__(self):
        out = ""
        for rank in range(7,-1,-1):
            out += (str(rank + 1) + " | ")
            for file in range(0,8):
                out += str(self.board[rank][file]) + " "
            out +=  "\n"
        out += "  -----------------\n"
        out += "    a b c d e f g h\n"
        return out + "\n" + str(self.legal_moves.keys())

    def move(self, san):
        legal_moves, wtm = self.legal_moves, self.white_to_move
        if san in legal_moves:
            self.board = legal_moves[san]
            self.white_to_move = not wtm
            self.find_all_legal_moves()
            return True
        else:
            return False

    def get(self, x,y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return '0'
        else:
            return self.board[x][y]

    def generate_legal_move(self, from_x, from_y, to_x, to_y, piece):
        pass
        from_piece = piece
        san_capture = 'x' if self.get(to_x,to_y) != '-' else ''
        san_piece = '' if piece.lower() == 'p' else piece
        san_square = get_san_square(to_x,to_y)
        san = san_piece + san_capture + san_square
        new_board = copy.deepcopy(self.board)
        new_board[to_x][to_y] = self.board[from_x][from_y]
        new_board[from_x][from_y] = '-'
        self.legal_moves[san] = new_board

    def find_all_legal_moves(self):
        self.legal_moves = {}
        for x in range(0,8):
            for y in range(0,8):
                piece = self.board[x][y]
                if self.white_to_move:
                    if piece == 'P':
                        white_pawn_moves(self,x,y,piece)
                    elif piece == 'R':
                        horizontal_moves(self,x,y,piece)
                    elif piece == 'B':
                        diagonal_moves(self,x,y,piece)
                    elif piece == 'Q':
                        horizontal_moves(self,x,y,piece)
                        diagonal_moves(self,x,y,piece)
                    elif piece == 'N':
                        knight_moves(self,x,y,piece)
                    elif piece == 'K':
                        king_moves(self,x,y,piece)
                else:
                    if piece == 'p':
                        black_pawn_moves(self,x,y,piece)
                    elif piece == 'r':
                        horizontal_moves(self,x,y,piece)
                    elif piece == 'b':
                        diagonal_moves(self,x,y,piece)
                    elif piece == 'q':
                        horizontal_moves(self,x,y,piece)
                        diagonal_moves(self,x,y,piece)
                    elif piece == 'n':
                        knight_moves(self,x,y,piece)
                    elif piece == 'k':
                        king_moves(self,x,y,piece)

def king_moves(game,x,y,piece):
    scan(game,x,y,1,0,1)
    scan(game,x,y,0,1,1)
    scan(game,x,y,-1,0,1)
    scan(game,x,y,0,-1,1)
    scan(game,x,y,1,1,1)
    scan(game,x,y,-1,1,1)
    scan(game,x,y,1,-1,1)
    scan(game,x,y,-1,-1,1)

def knight_moves(game,x,y,piece):
    get, wtm, generate_legal_move = game.get, game.white_to_move, game.generate_legal_move
    is_capturable = lambda str : str.islower() if wtm else str.isupper()
    for position in [[x+2,y+1],[x+2,y-1],[x-2,y+1],[x-2,y-1],[x+1,y+2],[x+1,y-2],[x-1,y+2],[x-1,y-2]]:
        if is_capturable(get(position[0],position[1])):
            generate_legal_move(x,y,position[0],position[1],piece)

def horizontal_moves(game,x,y,piece):
    scan(game,x,y,1,0)
    scan(game,x,y,0,1)
    scan(game,x,y,-1,0)
    scan(game,x,y,0,-1)

def diagonal_moves(game,x,y,piece):
    scan(game,x,y,1,1)
    scan(game,x,y,-1,1)
    scan(game,x,y,1,-1)
    scan(game,x,y,-1,-1)

def white_pawn_moves(game,x,y,piece):
    get, generate_legal_move = game.get, game.generate_legal_move
    #Advance 1 square
    if get(x+1,y) == '-':
        generate_legal_move(x,y,x+1,y,piece)
        #Advance 2 squares
        if get(x+2,y) == '-' and x == 1:
            generate_legal_move(x,y,x+2,y,piece)
    #Capture
    if get(x+1,y+1).islower():
        generate_legal_move(x,y,x+1,y+1,piece)
    if get(x+1,y-1).islower():
        generate_legal_move(x,y,x+1,y-1,piece)

def black_pawn_moves(game,x,y,piece):
    get, generate_legal_move = game.get, game.generate_legal_move
    #Advance 1 square
    if get(x-1,y) == '-':
        generate_legal_move(x,y,x-1,y,piece)
        #Advance 2 squares
        if get(x-2,y) == '-' and x == 6:
            generate_legal_move(x,y,x-2,y,piece)
    #Capture
    if get(x-1,y+1).isupper():
        generate_legal_move(x,y,x-1,y+1,piece)
    if get(x-1,y-1).isupper():
        generate_legal_move(x,y,x-1,y-1,piece)