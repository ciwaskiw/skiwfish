from constants import TABLE_MAP, MATERIAL_VALUES, INF
import random

def minimax(tree, depth, alpha, beta):
        
    if depth == 0:
        return None, eval(tree)
    
    if tree.get_san_move_list():
        best_move = random.choice(tree.get_san_move_list())
    else:
        best_move = None

    if tree.wtm:
        max_eval = -INF
        for child in tree.children.values():
            current_eval = minimax(child, depth - 1, alpha, beta)[1]
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = child.last_move
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        return best_move, max_eval

    else:
        min_eval = INF
        for child in tree.children.values():
            current_eval = minimax(child, depth - 1, alpha, beta)[1]
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = child.last_move
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        return best_move, min_eval
        

def max_from_tuple(tupleA, tupleB):
    return max(tupleA[1],tupleB[1])

def min_from_tuple(tupleA, tupleB):
    return min(tupleA[1],tupleB[1])

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
        if tree.wtm:
            score += INF
        else:
            score -= INF
    return score





