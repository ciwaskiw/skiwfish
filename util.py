def scan(tree, x, y, dir_x, dir_y, distance=7):
    #dir_x and dir_y are from -1 to 1 and represent the direction we are scanning
    #i.e. (dir_x,dir_y) is a normal vector in the correct direction
    piece = tree.get(x,y)
    wtm = tree.wtm
    is_capturable = lambda str : str.islower() if wtm else str.isupper()
    for i in range(1,distance+1):
        scanned_square = tree.get(x + i*dir_x, y + i*dir_y)
        if scanned_square == '-':
            tree.generate_legal_move(x, y, x + i*dir_x, y + i*dir_y, piece)
        else:
            if scanned_square == '0':
                return
            if is_capturable(scanned_square):
                tree.generate_legal_move(x, y, x + i*dir_x, y + i*dir_y, piece)
            return

def find_all_legal_moves(tree):
        legal_moves = {}
        for x in range(0,8):
            for y in range(0,8):
                #If we found that our king is threatened by a legal move, stop processing
                if tree.checkmate:
                    return
                piece = tree.get(x,y)
                if tree.wtm:
                    if piece == 'P':
                        white_pawn_moves(tree,x,y,piece)
                    elif piece == 'R':
                        horizontal_moves(tree,x,y,piece)
                    elif piece == 'B':
                        diagonal_moves(tree,x,y,piece)
                    elif piece == 'Q':
                        horizontal_moves(tree,x,y,piece)
                        diagonal_moves(tree,x,y,piece)
                    elif piece == 'N':
                        knight_moves(tree,x,y,piece)
                    elif piece == 'K':
                        king_moves(tree,x,y,piece)
                else:
                    if piece == 'p':
                        black_pawn_moves(tree,x,y,piece)
                    elif piece == 'r':
                        horizontal_moves(tree,x,y,piece)
                    elif piece == 'b':
                        diagonal_moves(tree,x,y,piece)
                    elif piece == 'q':
                        horizontal_moves(tree,x,y,piece)
                        diagonal_moves(tree,x,y,piece)
                    elif piece == 'n':
                        knight_moves(tree,x,y,piece)
                    elif piece == 'k':
                        king_moves(tree,x,y,piece)

def king_moves(tree,x,y,piece):
    scan(tree,x,y,1,0,1)
    scan(tree,x,y,0,1,1)
    scan(tree,x,y,-1,0,1)
    scan(tree,x,y,0,-1,1)
    scan(tree,x,y,1,1,1)
    scan(tree,x,y,-1,1,1)
    scan(tree,x,y,1,-1,1)
    scan(tree,x,y,-1,-1,1)

def knight_moves(tree,x,y,piece):
    get, wtm, generate_legal_move = tree.get, tree.wtm, tree.generate_legal_move
    is_capturable = lambda str : str.islower() if wtm else str.isupper()
    for position in [[x+2,y+1],[x+2,y-1],[x-2,y+1],[x-2,y-1],[x+1,y+2],[x+1,y-2],[x-1,y+2],[x-1,y-2]]:
        if is_capturable(get(position[0],position[1])) or get(position[0],position[1]) == '-':
            generate_legal_move(x,y,position[0],position[1],piece)

def horizontal_moves(tree,x,y,piece):
    scan(tree,x,y,1,0)
    scan(tree,x,y,0,1)
    scan(tree,x,y,-1,0)
    scan(tree,x,y,0,-1)

def diagonal_moves(tree,x,y,piece):
    scan(tree,x,y,1,1)
    scan(tree,x,y,-1,1)
    scan(tree,x,y,1,-1)
    scan(tree,x,y,-1,-1)

def white_pawn_moves(tree,x,y,piece):
    get, generate_legal_move = tree.get, tree.generate_legal_move
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

def black_pawn_moves(tree,x,y,piece):
    get, generate_legal_move = tree.get, tree.generate_legal_move
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
