import time

def heuristic(board):
    score = 0
    for line in range(board._BOARDSIZE):
        for case in range(board._BOARDSIZE):
            p = board[board.flatten((case, board._BOARDSIZE - line - 1))]
            if p == board._BLACK:
                score += 1
            elif p == board._WHITE:
                score -= 1
    return score

def deroulementAlphaBeta(board, depth, alpha, beta, is_player_max, start_time, time_limit):
    '''Déroulement d'une partie de GO avec l'algorithme alpha-beta.'''
    if time.time() - start_time > time_limit:
        raise TimeOutException()
    
    if depth == 0:
        return heuristic(board)
    
    elif board.is_game_over():
        winner = board.winner()
        if winner == board._BLACK:
            return float('inf')
        elif winner == board._WHITE:
            return float('-inf') 
        return 0; # egalite
    
    elif is_player_max: # maximiser (is_player_max == True)
        value = float('-inf')
        for move in board.legal_moves():
            board.push(move)
            value = max(value, deroulementAlphaBeta(board, depth - 1, alpha, beta, False, start_time, time_limit))
            board.pop()
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    else: # minimiser
        value = float('inf')
        for move in board.legal_moves():
            board.push(move)
            value = min(value, deroulementAlphaBeta(board, depth - 1, alpha, beta, True, start_time, time_limit))
            board.pop()
            if alpha >= value:
                return value
            beta = min(beta, value)            
        return value 
class TimeOutException(Exception):
    pass

def find_best_move(board, depth, start_time, time_limit):
    '''Trouve le meilleur coup pour le joueur courant en utilisant l'algorithme alpha-beta.'''
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    # Noir cherche toujours a maximiser
    # Blanc cherche toujours a minimiser
    is_player_max = (board._nextPlayer == board._BLACK)
    
    # Pire score possible
    if is_player_max:
        # Si la fonction joue pour Noir, elle cherche un score superieur
        best_eval = float('-inf')
    else:
        # Si la fonction joue pour Blanc, elle cherche un score inferieur
        best_eval = float('inf')

    try :
        for move in board.legal_moves():
            if time.time() - start_time > time_limit:
                    raise TimeOutException()
            board.push(move)
            # not is_player_max = adversaire
            eval = deroulementAlphaBeta(board, depth - 1, alpha, beta, not is_player_max, start_time, time_limit)
            board.pop()
            
            if is_player_max: # Si on est Noir (max)
                if eval > best_eval:
                    best_eval = eval
                    best_move = move
                alpha = max(alpha, best_eval)
            else: # Si on est Blanc (min)
                if eval < best_eval:
                    best_eval = eval
                    best_move = move
                beta = min(beta, best_eval)
                
        return best_move
    except TimeOutException:
        return None