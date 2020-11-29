# def minimax_move(board, difficulty):
#     return move

import board as board_class
from copy import deepcopy
import time
# STATICS
ROWS = 8
COLUMNS = 8


# STATICS (END)

def minimax_move(board, max_depth, player_color, computer_color):
    toc = time.perf_counter()
    move = maximize(deepcopy(board), 0, max_depth, player_color, computer_color, -65, 65).last_move
    tic = time.perf_counter()
    print(tic-toc)
    return move


# noinspection PyUnboundLocalVariable
def maximize(board, depth, max_depth, player_color, computer_color, alpha, beta):
    play = board.check_win_conditions(player_color, computer_color, False)
    if play == 'c' or play == '-' or depth == max_depth:
        print("Checking maximezer1 ", board.evaluate(computer_color), " ", board.last_move, " ", depth)
        return board
    children = board.get_children(computer_color)
    n_board_list = []
    n_board_sublist = []
    for row in range(0, ROWS):
        for column in range(0, COLUMNS):
            n_board_sublist.append(player_color)
        n_board_list.append(n_board_sublist)
    n_board = board_class.Board(n_board_list)
    max_value = n_board
    for child in children:
        move = minimize(child, depth + 1, max_depth, player_color, computer_color, alpha, beta)
        print("Checking maximzer2", max_value.evaluate(computer_color), " ", max_value.last_move, " ", move.evaluate(computer_color), " ", move.last_move, " ", depth)
        if move.evaluate(computer_color) >= max_value.evaluate(computer_color):
            max_value = child
        if max_value.evaluate(computer_color) >= beta:
            return max_value

        if max_value.evaluate(computer_color) > alpha:
            alpha = max_value.evaluate(computer_color)
    return max_value

def minimize(board, depth, max_depth, player_color, computer_color, alpha, beta):
    play = board.check_win_conditions(player_color, computer_color, False)
    if play == 'd' or play == '-' or depth == max_depth:
        print("Checking minimizer1 ", board.evaluate(computer_color), " ", board.last_move, " ",depth)
        return board
    children = board.get_children(player_color)
    n_board_list = []
    n_board_sublist = []
    for row in range(0, ROWS):
        for column in range(0, COLUMNS):
            n_board_sublist.append(computer_color)
        n_board_list.append(n_board_sublist)
    n_board = board_class.Board(n_board_list)
    min_value = n_board
    for child in children:
        move = maximize(child, depth + 1, max_depth, player_color, computer_color, alpha, beta)
        print("Checking minimizer2", min_value.evaluate(computer_color), " ", min_value.last_move, " ", move.evaluate(computer_color), " ", move.last_move, " ", depth)
        if move.evaluate(computer_color) <= min_value.evaluate(computer_color):
            min_value = child

        if min_value.evaluate(computer_color) <= alpha:
            return min_value

        if min_value.evaluate(computer_color) < beta:
            beta = min_value.evaluate(computer_color)
    return min_value
