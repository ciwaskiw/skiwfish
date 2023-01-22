import copy, random
from util import find_all_children
from engine import minimax
from constants import STARTING_POSITION, UNICODE_PIECE_MAP
def get_san_square(x,y):
    return chr(y + 97) + str(x+1)

class MoveTree():
    depth = 0 #Depth of tree; i.e. the number of levels below here.
    parent = None #Parent tree object ref
    children = {} #Map of s.a.n strings to child object refs
    board = [] #Board state
    wtm = True #True if white's move, false if black's
    castleable = [True,True,True,True] #White kingside then queenside, black kingside then queenside
    checkmate = False #(should be) True if children is empty

    def __init__(self, depth=0, parent = None, board=STARTING_POSITION, wtm=True, castleable=[True,True,True,True]):
        self.depth = depth
        self.parent = parent
        self.board = board
        self.wtm = wtm
        self.castleable = castleable
        self.children = {}
        if depth > 0:
            find_all_children(self)
    
    def increment_depth(self):
        self.depth += 1
        for child in self.children.values():
            child.increment_depth()
        if self.depth == 1:
            find_all_children()

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

    def illegal_prune(self):
        illegal_sans = []
        for san in self.children.keys():
            if self.children[san].illegal == True:
                illegal_sans.append(san)
        
        for san in illegal_sans:
            self.children.pop(san)
            #print(len(self.children))
        

    def add_legal_move_to_tree(self, from_x, from_y, to_x, to_y, san, from_piece, new_piece):
        wtm = self.wtm
        
        # Move the piece
        new_board = copy.deepcopy(self.board)
        new_board[to_x][to_y] = new_piece
        new_board[from_x][from_y] = '-'

        # Check if we removed the ability to castle
        new_castleable = copy.deepcopy(self.castleable)
        if from_piece.lower() == 'k':
            if wtm:
                new_castleable[0] = False
                new_castleable[1] = False
            else:
                new_castleable[2] = False
                new_castleable[3] = False
        elif from_piece.lower == 'r':
            if wtm:
                if from_y == 7:
                    new_castleable[0] = False
                elif from_y == 0:
                    new_castleable[1] = False
            else:
                if from_y == 7:
                    new_castleable[2] = False
                elif from_y == 0:
                    new_castleable[3] = False

        #Check if this move already exists, and specify the square of the moving piece if so.
        if san in self.children:
            insert_index = 0 if san[0].islower() else 1
            new_san = san[:insert_index] + get_san_square(from_x,from_y) + san[insert_index:]
            self.children[new_san] = MoveTree(self.depth - 1, self, new_board, not self.wtm, new_castleable)
        else:
            #If no conflicts, just add it.
            self.children[san] = MoveTree(self.depth - 1, self, new_board, not self.wtm, new_castleable)
    

    def generate_promotion(self, from_x, from_y, to_x, to_y):
        """Special version of generate_legal_move that's for pawn promotions"""
        to_piece = self.get(to_x,to_y)
        san_capture = '' if to_piece == '-' else 'x'
        san_square = get_san_square(to_x,to_y)
        #Generate 4 moves for each type of promotion
        for promotion in ['N','B','R','Q'] if self.wtm else ['n','b','r','q']:
            san = san_capture + san_square + promotion
            self.add_legal_move_to_tree(from_x,from_y,to_x,to_y,san,'',promotion)
           

    def generate_legal_move(self, from_x, from_y, to_x, to_y):
        """Given the 'from' square and the 'to' square, adds a move to the tree"""
        from_piece = self.get(from_x,from_y)
        to_piece = self.get(to_x,to_y)
        #If this move captures a king, its parent should be marked a checkmate.
        if to_piece.upper() == 'K':
            self.parent.checkmate = True
            return
        #Get SAN
        san_capture = '' if to_piece == '-' else 'x'
        san_piece = '' if from_piece.lower() == 'p' else from_piece.upper()
        san_square = get_san_square(to_x,to_y)
        san = san_piece + san_capture + san_square
        #Get Board State
        self.add_legal_move_to_tree(from_x,from_y,to_x,to_y,san,from_piece,from_piece)
    
    def get_san_move_list(self):
        return list(self.children.keys())


class Game():
    move_tree = MoveTree(2)

    def __str__(self):
        out = "  -----------------\n"
        for rank in range(7,-1,-1):
            out += (str(rank + 1) + " | ")
            for file in range(0,8):
                out += str(UNICODE_PIECE_MAP[self.move_tree.board[rank][file]]) + " "
            out +=  "\n"
        out += "  -----------------\n"
        out += "    a b c d e f g h\n"
        return out

    def move(self, san):
        if san == "engine":
            san = minimax(self.move_tree)
        elif san == "random":
            san = random.choice(self.move_tree.get_san_move_list())
        if san in self.move_tree.get_san_move_list():
            new_tree = self.move_tree.children[san]
            self.move_tree = new_tree
            return True
        else:
            return False

    def game_over(self):
        #TODO ADD STALEMATE
        return self.move_tree.checkmate

    

