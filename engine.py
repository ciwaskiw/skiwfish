from constants import TABLE_MAP, MATERIAL_VALUES

def minimax(tree, depth = 1):
    children, wtm = tree.children, tree.wtm
    if depth < 2:
        scores = list(map(lambda x: (1 if wtm else -1) * eval(children[x]), children.keys()))
        #print(list(children.keys()))
        #print(scores)
        max_score = max(scores)
        return list(children.keys())[scores.index(max_score)]

    pass

def eval(tree):
    wtm, board, = tree.wtm, tree.board
    score = 0
    flattened_board = [item for sublist in board for item in sublist] #Thanks for the one liner https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
    for i in range(0,len(flattened_board)):
        square = flattened_board[i]
        if square != '-': #Check each square, skip if empty
            if square.isupper(): #If this is a white piece
                score += MATERIAL_VALUES[square] #Add the material value of this piece
                score += TABLE_MAP[square][i] #Add the piece-square-value for this piece on this square
            else: #If this is a black piece
                score -= MATERIAL_VALUES[square.upper()] #Subtract the material value
                score -= list(reversed(TABLE_MAP[square.upper()]))[i] #Subtract the piece-square-value for this piece on this square
    mobility = len(tree.children) * 100 #Get mobility score
    score += (1 if wtm else -1) * mobility #Add if evaluating white, subtract if evaluating black
    if tree.checkmate:
        score += 200000
    return score





