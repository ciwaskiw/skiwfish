from constants import TABLE_MAP, MATERIAL_VALUES

def minimax(tree, depth = 1):
    legal_moves = tree.legal_moves
    if depth < 2:
        scores = list(map(lambda x: eval(legal_moves[x]), legal_moves.keys()))
        #print(list(legal_moves.keys()))
        #print(scores)
        max_score = max(scores)
        return list(legal_moves.keys())[scores.index(max_score)]

    pass

def eval(tree):
    wtm, board, = tree.wtm, tree.board
    score = 0
    flattened_board = [item for sublist in board for item in sublist] #Thanks for the one liner https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
    for i in range(0,len(flattened_board)):
        square = flattened_board[i]
        if square != '-':
            if not wtm:
                if square.isupper():
                    score += MATERIAL_VALUES[square]
                    score += TABLE_MAP[square][i]
                else:
                    score -= MATERIAL_VALUES[square.upper()]
            elif wtm and square.islower():
                if square.islower():
                    score += MATERIAL_VALUES[square.upper()]
                    score += list(reversed(TABLE_MAP[square.upper()]))[i]
                else:
                    score -= MATERIAL_VALUES[square]
    score += len(tree.legal_moves) * 100
    if tree.checkmate:
        score += 200000
    return score





