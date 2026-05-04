def heuristic(board):
    score = 0
    for line in range(board._BOARDSIZE):
        for case in range(board._BOARDSIZE):
            if board.board[line][case] == board._BLACK:
                score += 1
            elif board.board[line][case] == board._WHITE:
                score -= 1
    return score

def deroulementAlphaBeta(board, depth, alpha, beta, player):
    '''Déroulement d'une partie de GO avec l'algorithme alpha-beta.'''
    if depth == 0:
        return heuristic(board)
    elif board.is_game_over():
        if player == board._BLACK and board.winner() == board._BLACK:
            return float('inf')
        elif player == board._WHITE and board.winner() == board._WHITE:
            return float('inf')
        return float('-inf') 
    
    else:
        if player == board._BLACK: # minimiser
            value = float('inf')
            for move in board.legal_moves:
                board.push(move)
                value = min(value, deroulementAlphaBeta(board, depth - 1, alpha, beta, board._WHITE))
                board.pop()
                if alpha >= value:
                    return value
                beta = min(beta, value)

        else: # maximiser
            value = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                value = max(value, deroulementAlphaBeta(board, depth - 1, alpha, beta, board._BLACK))
                board.pop()
                if value >= beta:
                    return value
                alpha = max(alpha, value)
        
    return value