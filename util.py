def scan(tree, x, y, dir_x, dir_y, distance=7):
    #dir_x and dir_y are from -1 to 1 and represent the direction we are scanning
    #i.e. (dir_x,dir_y) is a normal vector in the correct direction
    piece = tree.get(x,y)
    wtm = tree.wtm
    is_capturable = lambda str : str.islower() if wtm else str.isupper()
    for i in range(1,distance+1):
        scanned_square = tree.get(x + i*dir_x, y + i*dir_y)
        if scanned_square == '-':
            tree.generate_legal_move(x, y, x + i*dir_x, y + i*dir_y)
        else:
            if scanned_square == '0':
                return
            if is_capturable(scanned_square):
                tree.generate_legal_move(x, y, x + i*dir_x, y + i*dir_y)
            return

def find_all_children(tree):
    children = {}
    for x in range(0,8):
        for y in range(0,8):
            #If we found that our king is threatened by a legal move, stop processing
            if tree.checkmate:
                return
            piece = tree.get(x,y)
            if tree.wtm:
                if piece == 'P':
                    pawn_moves(tree,x,y)
                elif piece == 'R':
                    horizontal_moves(tree,x,y)
                elif piece == 'B':
                    diagonal_moves(tree,x,y)
                elif piece == 'Q':
                    horizontal_moves(tree,x,y)
                    diagonal_moves(tree,x,y)
                elif piece == 'N':
                    knight_moves(tree,x,y)
                elif piece == 'K':
                    king_moves(tree,x,y)
            else:
                if piece == 'p':
                    pawn_moves(tree,x,y)
                elif piece == 'r':
                    horizontal_moves(tree,x,y)
                elif piece == 'b':
                    diagonal_moves(tree,x,y)
                elif piece == 'q':
                    horizontal_moves(tree,x,y)
                    diagonal_moves(tree,x,y)
                elif piece == 'n':
                    knight_moves(tree,x,y)
                elif piece == 'k':
                    king_moves(tree,x,y)
    castle_check(tree)
    if len(tree.children) == 0:
        tree.checkmate = True
    

def king_moves(tree,x,y):
    scan(tree,x,y,1,0,1)
    scan(tree,x,y,0,1,1)
    scan(tree,x,y,-1,0,1)
    scan(tree,x,y,0,-1,1)
    scan(tree,x,y,1,1,1)
    scan(tree,x,y,-1,1,1)
    scan(tree,x,y,1,-1,1)
    scan(tree,x,y,-1,-1,1)

def knight_moves(tree,x,y):
    get, wtm, generate_legal_move = tree.get, tree.wtm, tree.generate_legal_move
    is_capturable = lambda str : str.islower() if wtm else str.isupper()
    for position in [[x+2,y+1],[x+2,y-1],[x-2,y+1],[x-2,y-1],[x+1,y+2],[x+1,y-2],[x-1,y+2],[x-1,y-2]]:
        if is_capturable(get(position[0],position[1])) or get(position[0],position[1]) == '-':
            generate_legal_move(x,y,position[0],position[1])

def horizontal_moves(tree,x,y):
    scan(tree,x,y,1,0)
    scan(tree,x,y,0,1)
    scan(tree,x,y,-1,0)
    scan(tree,x,y,0,-1)

def diagonal_moves(tree,x,y):
    scan(tree,x,y,1,1)
    scan(tree,x,y,-1,1)
    scan(tree,x,y,1,-1)
    scan(tree,x,y,-1,-1)

def pawn_moves(tree,x,y):
    get, wtm = tree.get, tree.wtm
    #Advance 1 square
    inc = 1 if wtm else -1
    generate_legal_move = tree.generate_promotion if (x+inc) % 7 == 0 else tree.generate_legal_move
    if get(x+inc,y) == '-':
        generate_legal_move(x,y,x+inc,y)
        #Advance 2 squares
        if get(x+2*inc,y) == '-' and x-inc % 7 == 0:
            generate_legal_move(x,y,x+2*inc,y)
    #Capture
    if get(x+inc,y+1).islower():
        generate_legal_move(x,y,x+inc,y+1)
    if get(x+inc,y-1).islower():
        generate_legal_move(x,y,x+inc,y-1)

def castle_check(tree):
        get, wtm, castleable = tree.get, tree.wtm, tree.castleable
        if wtm:
            if castleable[0] and get(0,6) == '-' and get(0,5) == '-': #Kingside
                new_board = copy.deepcopy(tree.board)
                new_board[0][4] = '-'
                new_board[0][5] = 'R'
                new_board[0][6] = 'K'
                new_board[0][7] = '-'
                new_castleable = copy.deepcopy(tree.castleable)
                new_castleable[0] = False
                new_castleable[1] = False
                tree.children['0-0'] = MoveTree(0, new_board, not tree.wtm, new_castleable, '0-0')
            if castleable[1] and get(0,1) == '-' and get(0,2) == '-' and get(0,3) == '-': #Queenside
                new_board = copy.deepcopy(tree.board)
                new_board[0][0] = '-'
                new_board[0][1] = '-'
                new_board[0][2] = 'K'
                new_board[0][3] = 'R'
                new_board[0][4] = '-'
                new_castleable = copy.deepcopy(tree.castleable)
                new_castleable[0] = False
                new_castleable[1] = False
                tree.children['0-0-0'] = MoveTree(0, new_board, not tree.wtm, new_castleable, '0-0-0')
        else:
            if castleable[2] and get(7,6) == '-' and get(7,5) == '-': #Kingside
                new_board = copy.deepcopy(tree.board)
                new_board[7][4] = '-'
                new_board[7][5] = 'r'
                new_board[7][6] = 'k'
                new_board[7][7] = '-'
                new_castleable = copy.deepcopy(tree.castleable)
                new_castleable[2] = False
                new_castleable[3] = False
                tree.children['0-0'] = MoveTree(0, new_board, not tree.wtm, new_castleable, '0-0')
            if castleable[3] and get(7,1) == '-' and get(7,2) == '-' and get(7,3) == '-': #Queenside
                new_board = copy.deepcopy(tree.board)
                new_board[7][0] = '-'
                new_board[7][1] = '-'
                new_board[7][2] = 'k'
                new_board[7][3] = 'r'
                new_board[7][4] = '-'
                new_castleable = copy.deepcopy(tree.castleable)
                new_castleable[2] = False
                new_castleable[3] = False
                tree.children['0-0-0'] = MoveTree(0, new_board, not tree.wtm, new_castleable, '0-0-0')
