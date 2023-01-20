import copy, random
from util import find_all_legal_moves
from engine import minimax
from constants import STARTING_POSITION, UNICODE_PIECE_MAP
def get_san_square(x,y):
    return chr(y + 97) + str(x+1)

class MoveTree():
    last_move = ""
    legal_moves = {}
    board = []
    wtm = True #White to move
    castleable = [True,True,True,True] #White kingside then queenside, black kingside then queenside
    checkmate = False
    illegal = False

    def __init__(self, depth=0, board=STARTING_POSITION, wtm=True, castleable=[True,True,True,True], last_move = ''):
        self.legal_moves = {}
        self.board = board
        self.wtm = wtm
        self.populate(depth)
        self.castleable = castleable
        self.last_move = last_move

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
            #print(depth)
            #print(self.last_move)
            #print('---')
            if len(self.legal_moves) == 0:
                
                #print(len(self.legal_moves))
                find_all_legal_moves(self)
                #print(len(self.legal_moves))
                #print('-----')
            for leaf in self.legal_moves.values():
                leaf.populate(depth-1)
            self.illegal_prune()
                
    def castle_check(self):
        get, wtm, castleable = self.get, self.wtm, self.castleable
        if wtm:
            if castleable[0] and get(0,6) == '-' and get(0,5) == '-': #Kingside
                new_board = copy.deepcopy(self.board)
                new_board[0][4] = '-'
                new_board[0][5] = 'R'
                new_board[0][6] = 'K'
                new_board[0][7] = '-'
                new_castleable = copy.deepcopy(self.castleable)
                new_castleable[0] = False
                new_castleable[1] = False
                self.legal_moves['0-0'] = MoveTree(0, new_board, not self.wtm, new_castleable, '0-0')
            if castleable[1] and get(0,1) == '-' and get(0,2) == '-' and get(0,3) == '-': #Queenside
                new_board = copy.deepcopy(self.board)
                new_board[0][0] = '-'
                new_board[0][1] = '-'
                new_board[0][2] = 'K'
                new_board[0][3] = 'R'
                new_board[0][4] = '-'
                new_castleable = copy.deepcopy(self.castleable)
                new_castleable[0] = False
                new_castleable[1] = False
                self.legal_moves['0-0-0'] = MoveTree(0, new_board, not self.wtm, new_castleable, '0-0-0')
        else:
            if castleable[2] and get(7,6) == '-' and get(7,5) == '-': #Kingside
                new_board = copy.deepcopy(self.board)
                new_board[7][4] = '-'
                new_board[7][5] = 'r'
                new_board[7][6] = 'k'
                new_board[7][7] = '-'
                new_castleable = copy.deepcopy(self.castleable)
                new_castleable[2] = False
                new_castleable[3] = False
                self.legal_moves['0-0'] = MoveTree(0, new_board, not self.wtm, new_castleable, '0-0')
            if castleable[3] and get(7,1) == '-' and get(7,2) == '-' and get(7,3) == '-': #Queenside
                new_board = copy.deepcopy(self.board)
                new_board[7][0] = '-'
                new_board[7][1] = '-'
                new_board[7][2] = 'k'
                new_board[7][3] = 'r'
                new_board[7][4] = '-'
                new_castleable = copy.deepcopy(self.castleable)
                new_castleable[2] = False
                new_castleable[3] = False
                self.legal_moves['0-0-0'] = MoveTree(0, new_board, not self.wtm, new_castleable, '0-0-0')


    def illegal_prune(self):
        illegal_sans = []
        for san in self.legal_moves.keys():
            if self.legal_moves[san].illegal == True:
                illegal_sans.append(san)
        
        for san in illegal_sans:
            self.legal_moves.pop(san)
            #print(len(self.legal_moves))
        if len(self.legal_moves) == 0:
            self.checkmate = True

    def add_legal_move_to_tree(self, from_x, from_y, to_x, to_y, san, from_piece, new_piece):
        wtm = self.wtm
        #TODO: ADD ABILITY TO CHECK CONFLICTS BETWEEN MOVES
        
        new_board = copy.deepcopy(self.board)
        new_board[to_x][to_y] = new_piece
        new_board[from_x][from_y] = '-'

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

        if san in self.legal_moves:
            insert_index = 0 if san[0].islower() else 1
            new_san = san[:insert_index] + get_san_square(from_x,from_y) + san[insert_index:]
            self.legal_moves[new_san] = MoveTree(0, new_board, not self.wtm, new_castleable, san)
        else:
            self.legal_moves[san] = MoveTree(0, new_board, not self.wtm, new_castleable, san)
    
    def generate_promotion(self, from_x, from_y, to_x, to_y):
        to_piece = self.get(to_x,to_y)
        san_capture = '' if to_piece == '-' else 'x'
        san_square = get_san_square(to_x,to_y)
        #Generate 4 moves for each type of promotion
        for promotion in ['N','B','R','Q'] if self.wtm else ['n','b','r','q']:
            san = san_capture + san_square + promotion
            self.add_legal_move_to_tree(from_x,from_y,to_x,to_y,san,'',promotion)
           

    def generate_legal_move(self, from_x, from_y, to_x, to_y):
        from_piece = self.get(from_x,from_y)
        to_piece = self.get(to_x,to_y)
        #Check for check
        if to_piece.lower() == 'k':
            self.illegal = True
            return
        #Get SAN
        san_capture = '' if to_piece == '-' else 'x'
        san_piece = '' if from_piece.lower() == 'p' else from_piece.upper()
        san_square = get_san_square(to_x,to_y)
        san = san_piece + san_capture + san_square
        #Get Board State
        self.add_legal_move_to_tree(from_x,from_y,to_x,to_y,san,from_piece,from_piece)
    
    def get_san_move_list(self):
        return list(self.legal_moves.keys())


class Game():
    move_tree = MoveTree(3)

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
            new_tree = self.move_tree.legal_moves[san]
            new_tree.populate(3)
            self.move_tree = new_tree
            return True
        else:
            return False

    def game_over(self):
        #TODO ADD STALEMATE
        return self.move_tree.checkmate

    

