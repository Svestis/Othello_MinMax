"""
minimax file implementing minimax algorithm
"""
# Importing needed modules
import board as board_class
from copy import deepcopy

# STATICS
ROWS: int = 8
COLUMNS: int = 8
# STATICS (END)


def minimax_move(board: board_class.Board, max_depth: int, player_color: str, computer_color: str):
    """
    Starting the minimax algorith
    :param board: The current board instance
    :type board: board_class.Board
    :param max_depth: The max depth that the minimax algorith will reach
    :type max_depth: int
    :param player_color: the color of the player
    :type player_color: str
    :param computer_color: the color of the computer
    :type computer_color: str
    :return: The best move
    :rtype: tuple
    """
    move: tuple = maximize(deepcopy(board), 0, max_depth, player_color, computer_color, -65, 65).last_move
    return move


# noinspection PyUnboundLocalVariable
def maximize(board: board_class.Board, depth: int, max_depth: int, player_color: str, computer_color: str,
             alpha: int, beta: int):
    """
    The maximize value (for the computer)
    :param board: a board instance
    :type board: board_class.Board
    :param depth: the current depth passed
    :type depth: int
    :param max_depth: the max depth that the algorith will reach
    :type max_depth: int
    :param player_color: the color of the player
    :type player_color: str
    :param computer_color: the color of the computer
    :type computer_color: str
    :param alpha: the alpha parameter for the alpha-beta pruning
    :type alpha: int
    :param beta: the beta function for the alpha-beta pruning
    :type beta: int
    :return: the board with the best move
    :rtype: board_class.Board
    """
    # Checks win condition
    play: str = board.check_win_conditions(player_color, computer_color, False)
    if play == 'c' or play == '-' or depth == max_depth:
        return board

    children: list = board.get_children(computer_color)  # Getting children
    n_board_list: list = []
    n_board_sublist: list = []

    # Creating a board with the opposite values
    for row in range(0, ROWS):
        for column in range(0, COLUMNS):
            n_board_sublist.append(player_color)
        n_board_list.append(n_board_sublist)
    n_board: board_class.Board = board_class.Board(n_board_list)
    max_value: board_class.Board = n_board

    # Running for all children
    for child in children:
        move: board_class.Board = minimize(child, depth + 1, max_depth, player_color, computer_color, alpha, beta)
        if move.evaluate(computer_color) >= max_value.evaluate(computer_color):
            max_value: board_class.Board = child

        # Implementing a-b pruning
        if max_value.evaluate(computer_color) >= beta:
            return max_value

        if max_value.evaluate(computer_color) > alpha:
            alpha: int = max_value.evaluate(computer_color)
    return max_value


def minimize(board: board_class.Board, depth: int, max_depth: int, player_color: str, computer_color: str,
             alpha: int, beta: int):
    """
    The minimize value (for the player)
    :param board: a board instance
    :type board: board_class.Board
    :param depth: the current depth passed
    :type depth: int
    :param max_depth: the max depth that the algorithm will reach
    :type max_depth: int
    :param player_color: the color of the player
    :type player_color: str
    :param computer_color: the color of the computer
    :type computer_color: str
    :param alpha: the alpha parameter for the alpha-beta pruning
    :type alpha: int
    :param beta: the beta function for the alpha-beta pruning
    :type beta: int
    :return: the board with the best move
    :rtype: board_class.Board
    """
    # Checks win condition
    play: str = board.check_win_conditions(player_color, computer_color, False)
    if play == 'd' or play == '-' or depth == max_depth:
        return board

    children = board.get_children(player_color)  # Getting children
    n_board_list = []
    n_board_sublist = []

    # Creating a board with the opponent value
    for row in range(0, ROWS):
        for column in range(0, COLUMNS):
            n_board_sublist.append(computer_color)
        n_board_list.append(n_board_sublist)
    n_board: board_class.Board = board_class.Board(n_board_list)
    min_value: board_class.Board = n_board

    # Running for all children
    for child in children:
        move: board_class.Board = maximize(child, depth + 1, max_depth, player_color, computer_color, alpha, beta)
        if move.evaluate(computer_color) <= min_value.evaluate(computer_color):
            min_value: board_class.Board = child

        # Implementing a-b pruning
        if min_value.evaluate(computer_color) <= alpha:
            return min_value

        if min_value.evaluate(computer_color) < beta:
            beta: int = min_value.evaluate(computer_color)
    return min_value
