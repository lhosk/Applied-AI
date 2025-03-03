# UNC Charlotte 
# ITCS 5153 - Applied AI - Spring 2025 
# Lab 3 
# Adversarial Search / Game Playing 
# This module implements the minimax andd ab pruning methods
# Student ID: 801


import time


ai_player = 'AI'
human = 'player'
empty = None
max_depth = 5


# Picks a move (sends to main)
def pick_move(agent, board):
    start_time = time.time()

    # Checks easy block or easy win
    forced_col = quick_win_or_block(board)
    if forced_col is not None:
        best_col = forced_col
        nodes = 1
    else: # Use normal search if no forced moves
        if agent == 'ab_pruning':
            best_col, _, nodes = ab_pruning_algorithm(board, max_depth, float('-inf'), float('inf'), True)
        else:
            best_col, _, nodes = minimax_algorithm(board, max_depth, True)

        if best_col is None:
            valid = get_valid_moves(board)
            if valid:
                best_col = valid[0]
            else:
                best_col = None

    end_time = time.time()
    mins, secs = divmod(end_time - start_time, 60)

    # Sends column, minutes, seconds, and number of nodes for log output
    return best_col, int(mins), round(secs, 2), nodes


# Runs the MiniMax algorithm by minimizing and maximizing scores
def minimax_algorithm(board, depth, maximizing_player):
    valid_cols = get_valid_moves(board)
    nodes_explored = 1

    # Reached max depth
    if depth == 0 or is_terminal_node(board):
        if is_terminal_node(board):
            if check_win(board, ai_player):
                return (None, 1000000000, nodes_explored)
            elif check_win(board, human):
                return (None, -1000000000, nodes_explored)
            else:
                return (None, 0, nodes_explored)
        else:
            return (None, evaluate_board(board, ai_player), nodes_explored)

    # Maximize score
    if maximizing_player:
        best_score = float('-inf')
        best_col = valid_cols[0] if valid_cols else None
        for col in valid_cols:
            new_board = make_move(board, col, ai_player)
            _, score, subnodes = minimax_algorithm(new_board, depth - 1, False)
            nodes_explored += subnodes
            if score > best_score:
                best_score = score
                best_col = col
            if best_score >= 1000000000:
                break
        return (best_col, best_score, nodes_explored)
    else: # Minimize score
        best_score = float('inf')
        best_col = valid_cols[0] if valid_cols else None
        for col in valid_cols:
            new_board = make_move(board, col, human)
            _, score, subnodes = minimax_algorithm(new_board, depth - 1, True)
            nodes_explored += subnodes
            if score < best_score:
                best_score = score
                best_col = col
            if best_score <= -1000000000:
                break
        return (best_col, best_score, nodes_explored)


# Runs the Alpha-Beta Pruning Algorithm by cutting off nodes
def ab_pruning_algorithm(board, depth, alpha, beta, maximizing_player):
    valid_cols = get_valid_moves(board)
    nodes_explored = 1

    # Reached max depth
    if depth == 0 or is_terminal_node(board):
        if is_terminal_node(board):
            if check_win(board, ai_player):
                return (None, 1000000000, nodes_explored)
            elif check_win(board, human):
                return (None, -1000000000, nodes_explored)
            else:
                return (None, 0, nodes_explored)
        else:
            return (None, evaluate_board(board, ai_player), nodes_explored)

    # Maximizing score
    if maximizing_player:
        best_score = float('-inf')
        best_col = valid_cols[0] if valid_cols else None
        for col in valid_cols:
            new_board = make_move(board, col, ai_player)
            _, score, subnodes = ab_pruning_algorithm(new_board, depth - 1, alpha, beta, False)
            nodes_explored += subnodes
            if score > best_score:
                best_score = score
                best_col = col
            alpha = max(alpha, best_score)
            if alpha >= beta or best_score >= 1000000000:
                break
        return (best_col, best_score, nodes_explored)
    else: # Minimizing score
        best_score = float('inf')
        best_col = valid_cols[0] if valid_cols else None
        for col in valid_cols:
            new_board = make_move(board, col, human)
            _, score, subnodes = ab_pruning_algorithm(new_board, depth - 1, alpha, beta, True)
            nodes_explored += subnodes
            if score < best_score:
                best_score = score
                best_col = col
            beta = min(beta, best_score)
            if alpha >= beta or best_score <= -1000000000:
                break
        return (best_col, best_score, nodes_explored)


# Find winning move (if possible)
# Find a block (if possible)
# Find a win in two-moves (if possible)
def quick_win_or_block(board):
    valid_cols = get_valid_moves(board)
    
    for col in valid_cols:
        sim_board = make_move(board, col, ai_player)
        if check_win(sim_board, ai_player):
            return col
            
    for col in valid_cols:
        sim_board = make_move(board, col, human)
        if check_win(sim_board, human):
            return col
            
    for col in valid_cols:
        sim_board = make_move(board, col, ai_player)
        winning_moves = 0
        for next_col in get_valid_moves(sim_board):
            next_board = make_move(sim_board, next_col, ai_player)
            if check_win(next_board, ai_player):
                winning_moves += 1
        if winning_moves >= 2:
            return col
            
    return None


# Checks if player has won on the board
def check_win(board, player):
    rows = len(board)
    cols = len(board[0])

    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == player and
                board[r][c+1] == player and
                board[r][c+2] == player and
                board[r][c+3] == player):
                return True

    for r in range(rows - 3):
        for c in range(cols):
            if (board[r][c] == player and
                board[r+1][c] == player and
                board[r+2][c] == player and
                board[r+3][c] == player):
                return True

    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == player and
                board[r+1][c+1] == player and
                board[r+2][c+2] == player and
                board[r+3][c+3] == player):
                return True

    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == player and
                board[r-1][c+1] == player and
                board[r-2][c+2] == player and
                board[r-3][c+3] == player):
                return True

    return False


# Makes sure move is valid
def is_valid_move(board, col):
    return board[0][col] is None


# Provides valid moves based on board
def get_valid_moves(board):
    valid = []
    cols = len(board[0])
    for c in range(cols):
        if is_valid_move(board, c):
            valid.append(c)
    center = cols // 2
    valid.sort(key=lambda x: abs(x - center))
    return valid


# Makes new board to test future moves
def make_move(board, col, player):
    new_board = [row[:] for row in board]
    for r in range(len(new_board)-1, -1, -1):
        if new_board[r][col] is None:
            new_board[r][col] = player
            return new_board
    return new_board


# Assigns scores to section of board
# Good moves = higher score, Bad moves = lower score
def evaluate_window(window, player):
    opponent = human if player == ai_player else ai_player
    score = 0

    if window.count(player) == 4:
        score += 1000000
    elif window.count(player) == 3 and window.count(None) == 1:
        score += 1000
    elif window.count(player) == 2 and window.count(None) == 2:
        score += 10

    if window.count(opponent) == 3 and window.count(None) == 1:
        score -= 800
    elif window.count(opponent) == 2 and window.count(None) == 2:
        score -= 8

    return score


# Iterates through windows to provide overall score
def evaluate_board(board, player):
    rows = len(board)
    cols = len(board[0])
    score = 0

    # Gives bonus if middle is controlled
    center = cols // 2
    center_array = [board[r][center] for r in range(rows)]
    score += center_array.count(player) * 30

    for r in range(rows):
        for c in range(cols - 3):
            window = [board[r][c + i] for i in range(4)]
            score += evaluate_window(window, player)

    for r in range(rows - 3):
        for c in range(cols):
            window = [board[r + i][c] for i in range(4)]
            score += evaluate_window(window, player)

    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, player)

    for r in range(3, rows):
        for c in range(cols - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, player)

    return score


# Checks if game is over
def is_terminal_node(board):
    return check_win(board, ai_player) or check_win(board, human) or len(get_valid_moves(board)) == 0