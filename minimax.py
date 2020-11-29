# def minimax_move(board, difficulty):
#     return move

import board as board_class
from copy import deepcopy

# STATICS
ROWS = 8
COLUMNS = 8


# STATICS (END)

def minimax_move(board, max_depth, player_color, computer_color):
    return maximize(deepcopy(board), 0, max_depth, player_color, computer_color)


# noinspection PyUnboundLocalVariable
def maximize(board, depth, max_depth, player_color, computer_color):
    play = board.check_win_conditions(player_color, computer_color)
    if play == 'c' or play == '-' or depth == max_depth:
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
        move = minimize(child, depth + 1, max_depth, player_color, computer_color)
        if move.evaluate(computer_color) >= max_value.evaluate(computer_color):
            max_value = child
    return n_board


def minimize(board, depth, max_depth, player_color, computer_color):
    play = board.check_win_conditions(player_color, computer_color)
    if play == 'd' or play == '-' or depth == max_depth:
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
        move = maximize(child, depth + 1, max_depth, player_color, computer_color)
        if move.evaluate(computer_color) <= min_value.evaluate(computer_color):
            min_value = child
    return n_board
