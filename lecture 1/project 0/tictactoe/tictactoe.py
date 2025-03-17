"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # assuming x plays first
    count_x = 0
    count_o = 0
    for row in board:
        count_x += row.count(X)
        count_o += row.count(O)
    
    # if count_x==count_o: return X

    if count_x>count_o: return O
    return X# in case greater than or equal


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    
    copy_board = deepcopy(board)
    copy_board[i][j] = player(board)
    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # column wise
    for j in range(3):
        if board[0][j]==board[1][j]==board[2][j]: return board[2][j]
    
    # row wise
    for i in range(3):
        if board[i][0]==board[i][1]==board[i][2]: return board[i][2]
    
    # diogonal
    if board[0][0]==board[1][1]==board[2][2]: return board[0][0]
    if board[0][2]==board[1][1]==board[2][0]: return board[0][2]
    
    return


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board): return True

    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY: return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    won = winner(board)
    if won==None: return 0

    if won==X: return 1
    return -1


inf = float("inf")
def max_value(board):
    if terminal(board):
        return utility(board), tuple()
    
    v = -inf
    pos = tuple()
    for i, j in actions(board):
        next_val = min_value(result(board, (i, j)))[0]
        # v = max(v, next_val)
        if next_val>v:
            v = next_val
            pos = (i, j)
    
    return v, pos

def min_value(board):
    if terminal(board):
        return utility(board), tuple()
    
    v = inf
    pos = tuple()
    for i, j in actions(board):
        next_val = max_value(result(board, (i, j)))[0]
        # v = min(v, next_val)
        if next_val<v:
            v = next_val
            pos = (i, j)

    return v, pos

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board): return

    if player(board)==X:# max function
        return max_value(board)[1]
    else:# min function
        return min_value(board)[1]

if __name__=="__main__":
    board = initial_state()
    board[0][0] = X
    # print(min_value(board))
    print(minimax(board))
    # print(actions(board))