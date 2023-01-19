import copy
from util import find_all_legal_moves
from constants import STARTING_POSITION
def get_san_square(x,y):
    return chr(y + 97) + str(x+1)

class MoveTree():
    legal_moves = {}
    board = []
    wtm = True #White to move
    checkmate = False

    def __init__(self, depth=0, board=STARTING_POSITION, wtm=True):
        self.legal_moves = {}
        self.board = board
        self.wtm = wtm
        self.populate(depth)

    def __str__(self):
        out = ""
        for rank in self.board:
            for file in rank:
                out += file
        return out
        
    
    def get(self, x,y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return '0'
        else:
            return self.board[x][y]

    def populate(self, depth=0):
        if depth > 0:
            find_all_legal_moves(self)
            for leaf in self.legal_moves.values():
                leaf.populate(depth-1)
            self.checkmate_prune()
                
    def checkmate_prune(self):
        checkmate_sans = []
        for san in self.legal_moves.keys():
            if self.legal_moves[san].checkmate == True:
                checkmate_sans.append(san)
        
        for san in checkmate_sans:
            self.legal_moves.pop(san)
        
        if len(self.legal_moves) == 0:
            self.checkmate = True
    
    def generate_legal_move(self, from_x, from_y, to_x, to_y, piece):
        from_piece = piece
        to_piece = self.get(to_x,to_y)
        #Check for check
        if to_piece.lower() == 'k':
            self.checkmate = True
            return
        #Get SAN
        san_capture = '' if to_piece == '-' else 'x'
        san_piece = '' if piece.lower() == 'p' else piece.upper()
        san_square = get_san_square(to_x,to_y)
        san = san_piece + san_capture + san_square
        #Get Board State
        new_board = copy.deepcopy(self.board)
        new_board[to_x][to_y] = self.board[from_x][from_y]
        new_board[from_x][from_y] = '-'
        self.legal_moves[san] = MoveTree(0, new_board, not self.wtm)
    
    def get_san_move_list(self):
        return self.legal_moves.keys()


class Game():
    move_tree = MoveTree(2)

    def __str__(self):
        out = "  -----------------\n"
        for rank in range(7,-1,-1):
            out += (str(rank + 1) + " | ")
            for file in range(0,8):
                out += str(self.move_tree.board[rank][file]) + " "
            out +=  "\n"
        out += "  -----------------\n"
        out += "    a b c d e f g h\n"
        return out

    def move(self, san):
        if san in self.move_tree.get_san_move_list():
            new_tree = self.move_tree.legal_moves[san]
            new_tree.populate(2)
            self.move_tree = new_tree
            return True
        else:
            return False

    def game_over(self):
        return move_tree.checkmate

    

