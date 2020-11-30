"""
Board file including general functions and the Board class
"""
# Importing needed modules
from typing import Tuple
import numpy as np
from copy import deepcopy

# STATICS (START)
ROWS: int = 8
COLUMNS: int = 8
col_enumerator: Tuple[str, str, str, str, str, str, str, str] = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
row_enumerator: Tuple[str, str, str, str, str, str, str, str] = ('1', '2', '3', '4', '5', '6', '7', '8')
# STATICS (END)


def col_enum(index: int):
    """
    Converts number to column letter using the col_enumerator variable
    :param index: The index number of a move (list index value)
    :type index: int
    :return: The column name as in col_enumerator
    :rtype: int
    """
    if index < len(col_enumerator):
        return col_enumerator[index]
    return False


def row_enum(index: int):
    """
    Converts number to row number using the row_enumerator variable
    :param index: The index number of a move (list index value)
    :type index: int
    :return: The row number as in row_enumerator
    :rtype: int
    """
    if index < len(row_enumerator):
        return row_enumerator[index]
    return False


class Board:
    """
    Class board including the following variables and functions:
    -----VARIABLES-----
    :var self.board: The list presenting the board
    :type self.board: list
    :var self.last_move: The latest move played
    :type self.last_move: tuple
    """
    def __init__(self, board: list = '', last_move: tuple = ''):
        """
        __init__ function
        :param board: a board list. If none give, then the board is created from initial game state
        :type board: list
        :param last_move: The latest move played. If none given then it is initialized to blank ('')
        :type last_move: tuple
        :return: Nothing
        :rtype: N/A
        """
        # Creating board
        if board == '':
            self.board: list = self.create_board()
        else:
            self.board: list = board
        self.last_move: tuple = last_move  # Assigning parameter to self variable

    @staticmethod
    def create_board():
        """
        Creating board
        :return: a list indicating a board
        :rtype: list
        """
        return [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', 'L', 'D', ' ', ' ', ' '],
                [' ', ' ', ' ', 'D', 'L', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

    def set_board(self, move: tuple, value: str, valid_moves: list, game_history: list, actor_color: str):
        """
        Setting board value according to input from user/AI
        :param move: A move that we would like to display
        :type move: tuple
        :param value: The value of the player
        :type value: str
        :param valid_moves: A list with all the valid moves
        :type valid_moves: list
        :param game_history: a list including all the game history
        :type game_history: list
        :param actor_color: the value of the current player
        :type actor_color: str
        :return: The move and the game history
        :rtype: tuple
        """
        def move_exists():
            """
            Helper function which checks if a move is a valid move passed as an argument
            :return: True if a move is in the list valid moves otherwise false
            :rtype: bool
            """
            # Checking if a move is present in the valid moves
            for valid_move in valid_moves:
                if (move[0], move[1]) == valid_move:
                    return True
            return False

        # Checking if we are out of bounds
        if move[0] > ROWS or move[1] > COLUMNS:
            print("Your piece can't be placed in outside of the board. Invalid move.")

        # Handling move
        if move_exists():  # Checks if move is in the valid moves via helper function
            self.board[move[0]][move[1]] = value  # Adding the move on the board with the passed valie
            if value == 'D' or value == 'L':
                game_history.append((move[0], move[1], value))  # Adding the move in game history
                self.last_move: tuple = (move[0], move[1])  # Change the latest move to current move
                self.flip_opponent_pieces(move, actor_color)  # Calling the function to flip opponent pieces
            return move, game_history
        else:
            print("Your piece can't be placed in {}{}. It is not a valid move.".format(col_enum(move[1]),
                                                                                       row_enum(move[0])))
            return False

    def print_board(self):
        """
        Print the current board state
        :return: Nothing
        :rtype: N/A
        """
        def print_header():
            """
            Helper function to print the headers
            :return: Nothing
            :rtype: N/A
            """
            print("     ", end='')

            # Printing letters
            for letter in range(ord('A'), ord('I')):
                print(chr(letter), end='')
                print("     ", end='')

        print_header()  # Printing the header vial the helper function

        # Looping through the board in order to add the values. Printing also the rows and seperators
        for i in range(0, ROWS):
            print("")
            print("  -------------------------------------------------")
            print(str(i + 1) + " ", end='')

            for j in range(0, COLUMNS):
                print("| ", self.board[i][j], " ", end='')

            print("| ", end='')
            print(str(i + 1) + " ", end='')
        print("")
        print("  -------------------------------------------------")
        print_header()  # Printing the footer
        print()
        print()

    def flip_opponent_pieces(self, piece: tuple, actor_color: str):
        """
        Flipping the opponent pieces after placing a new checker
        :param piece:
        :type piece:
        :param actor_color:
        :type actor_color:
        :return:
        :rtype:
        """
        # Checking who is who
        if actor_color == 'L':
            opponent_color: str = 'D'
        else:
            opponent_color: str = 'L'

        # Finding darks and lights and adding the coordinates in set
        matrix: np.ndarray = np.array(self.board)
        player_pieces_: np.ndarray = np.where(matrix == actor_color)
        player_pieces: set = set()
        for i in range(0, len(player_pieces_[0])):
            player_pieces.add((player_pieces_[0][i], player_pieces_[1][i]))
        opponent_pieces_: np.ndarray = np.where(matrix == opponent_color)
        opponent_pieces: set = set()
        for i in range(0, len(opponent_pieces_[0])):
            opponent_pieces.add((opponent_pieces_[0][i], opponent_pieces_[1][i]))
        pieces_to_flip: list = []  # Storing the values of the pieces to flip color

        # Looping through the rows and columns
        for x in range(piece[1] - 1, -1, -1):  # Going upwards
            if (piece[0], x) in opponent_pieces:  # If next piece is opponent's add it to the list
                pieces_to_flip.append((piece[0], x))
            elif self.board[piece[0]][x] == actor_color:
                for single_piece in pieces_to_flip:  # If next piece is actor's flip it
                    self.board[single_piece[0]][single_piece[1]]: list = actor_color
                break
            elif self.board[piece[0]][x] == ' ':  # If next piece is blank
                break
        pieces_to_flip.clear()  # Clearing list
        for y in range(piece[0] - 1, -1, -1):  # Going left
            if (y, piece[1]) in opponent_pieces:  # If next piece is opponent's add it to the list
                pieces_to_flip.append((y, piece[1]))
            elif self.board[y][piece[1]] == actor_color:
                for single_piece in pieces_to_flip:  # If next piece is actor's flip it
                    self.board[single_piece[0]][single_piece[1]]: list = actor_color
                break
            elif self.board[y][piece[1]] == ' ':  # If next piece is blank
                break
        pieces_to_flip.clear()  # Clearing list
        for x in range(piece[1] + 1, 8):  # Going downwards
            if (piece[0], x) in opponent_pieces:  # If next piece is opponent's add it to the list
                pieces_to_flip.append((piece[0], x))
            elif self.board[piece[0]][x] == actor_color:
                for single_piece in pieces_to_flip:  # If next piece is actor's flip it
                    self.board[single_piece[0]][single_piece[1]]: list = actor_color
                break
            elif self.board[piece[0]][x] == ' ':  # If next piece is blank
                break
        pieces_to_flip.clear()  # Clearing list
        for y in range(piece[0] + 1, 8):  # Going right
            if (y, piece[1]) in opponent_pieces:  # If next piece is opponent's add it to the list
                pieces_to_flip.append((y, piece[1]))
            elif self.board[y][piece[1]] == actor_color:
                for single_piece in pieces_to_flip:  # If next piece is actor's flip it
                    self.board[single_piece[0]][single_piece[1]]: list = actor_color
                break
            elif self.board[y][piece[1]] == ' ':  # If next piece is blank
                break
        pieces_to_flip.clear()  # Clearing list

        # Finding diagonal
        for y, x in zip(range(piece[0] + 1, 8), range(piece[1] + 1, 8)):  # Going down right
            if (y, x) in opponent_pieces:  # If next piece is opponent's add it to the list
                pieces_to_flip.append((y, x))
            elif self.board[y][x] == actor_color:
                for single_piece in pieces_to_flip:
                    self.board[single_piece[0]][single_piece[1]]: list = actor_color  # If next piece is actor's flip it
                break
            elif self.board[y][x] == ' ':  # If next piece is blank
                break
        pieces_to_flip.clear()  # Clearing list
        for y, x in zip(range(piece[0] - 1, -1, -1), range(piece[1] - 1, -1, -1)):  # Going up left
            if (y, x) in opponent_pieces:  # If next piece is opponent's add it to the list
                pieces_to_flip.append((y, x))
            elif self.board[y][x] == actor_color:
                for single_piece in pieces_to_flip:
                    self.board[single_piece[0]][single_piece[1]]: list = actor_color  # If next piece is actor's flip it
                break
            elif self.board[y][x] == ' ':  # If next piece is blank
                break
        pieces_to_flip.clear()  # Clearing list

        for y, x in zip(range(piece[0] - 1, -1, -1), range(piece[1] + 1, 8)):  # Going upright
            if (y, x) in opponent_pieces:  # If next piece is opponent's add it to the list
                pieces_to_flip.append((y, x))
            elif self.board[y][x] == actor_color:
                for single_piece in pieces_to_flip:
                    self.board[single_piece[0]][single_piece[1]]: list = actor_color  # If next piece is actor's flip it
                break
            elif self.board[y][x] == ' ':  # If next piece is blank
                break
        pieces_to_flip.clear()  # Clearing list

        for y, x in zip(range(piece[0] + 1, 8), range(piece[1] - 1, -1, -1)):  # Going down left
            if (y, x) in opponent_pieces:  # If next piece is opponent's add it ot the list
                pieces_to_flip.append((y, x))
            elif self.board[y][x] == actor_color:
                for single_piece in pieces_to_flip:
                    self.board[single_piece[0]][single_piece[1]]: list = actor_color  # If next piece is actor's flip it
                break
            elif self.board[y][x] == ' ':  # If next piece is blank
                break
        pieces_to_flip.clear()  # Clearing list
        return self.board

    def find_moves(self, player_color: str):
        """
        Finding all possible moves for current round (neighbours of checkers)
        :param player_color: The color of the player
        :type player_color: str
        :return: all valid moves found
        :rtype: list
        """
        # Who is who
        if player_color == 'L':
            opponent_color: str = 'D'
        else:
            opponent_color: str = 'L'

        # Finding darks and lights and adding the coordinates in tuple
        matrix: np.ndarray = np.array(self.board)
        player_pieces_: np.ndarray = np.where(matrix == player_color)
        player_pieces: set = set()
        for i in range(0, len(player_pieces_[0])):
            player_pieces.add((player_pieces_[0][i], player_pieces_[1][i]))
        opponent_pieces_: np.ndarray = np.where(matrix == opponent_color)
        opponent_pieces: set = set()
        for i in range(0, len(opponent_pieces_[0])):
            opponent_pieces.add((opponent_pieces_[0][i], opponent_pieces_[1][i]))
        valid_moves: list = []
        diagonal: set = set()

        # Finding valid moves (valid=being around opposite color). Checking also border condition
        for piece in opponent_pieces:
            if (piece[0], piece[1] + 1) not in opponent_pieces and (piece[0], piece[1] + 1) not in player_pieces and \
                    piece[1] != 7:
                for x in range(piece[1] - 1, -1, -1):
                    if (piece[0], x) in player_pieces:
                        valid_moves.append((piece[0], piece[1] + 1))
                    elif self.board[piece[0]][x] == ' ':
                        break
            if (piece[0] + 1, piece[1]) not in opponent_pieces and (piece[0] + 1, piece[1]) not in player_pieces and \
                    piece[0] != 7:
                for y in range(piece[0] - 1, -1, -1):
                    if (y, piece[1]) in player_pieces:
                        valid_moves.append((piece[0] + 1, piece[1]))
                    elif self.board[y][piece[1]] == ' ':
                        break
            if (piece[0], piece[1] - 1) not in opponent_pieces and (piece[0], piece[1] - 1) not in player_pieces and \
                    piece[1] != 0:
                for x in range(piece[1] + 1, 8):
                    if (piece[0], x) in player_pieces:
                        valid_moves.append((piece[0], piece[1] - 1))
                    elif self.board[piece[0]][x] == ' ':
                        break
            if (piece[0] - 1, piece[1]) not in opponent_pieces and (piece[0] - 1, piece[1]) not in player_pieces and \
                    piece[0] != 0:
                for y in range(piece[0] + 1, 8):
                    if (y, piece[1]) in player_pieces:
                        valid_moves.append((piece[0] - 1, piece[1]))
                    elif self.board[y][piece[1]] == ' ':
                        break

            # Finding diagonal
            if (piece[0] - 1, piece[1] - 1) not in opponent_pieces and (
                    piece[0] - 1, piece[1] - 1) not in player_pieces and piece[0] != 0 and piece[1] != 0:
                for y, x in zip(range(piece[0] + 1, 8), range(piece[1] + 1, 8)):
                    if (y, x) in player_pieces:
                        valid_moves.append((piece[0] - 1, piece[1] - 1))
                        diagonal.add((piece[0] - 1, piece[1] - 1))
                    elif self.board[y][x] == ' ':
                        break
            if (piece[0] + 1, piece[1] + 1) not in opponent_pieces and (
                    piece[0] + 1, piece[1] + 1) not in player_pieces and piece[0] != 7 and piece[1] != 7:
                for y, x in zip(range(piece[0] - 1, -1, -1), range(piece[1] - 1, -1, -1)):
                    if (y, x) in player_pieces:
                        valid_moves.append((piece[0] + 1, piece[1] + 1))
                        diagonal.add((piece[0] + 1, piece[1] + 1))
                    elif self.board[y][x] == ' ':
                        break
            if (piece[0] + 1, piece[1] - 1) not in opponent_pieces and (
                    piece[0] + 1, piece[1] - 1) not in player_pieces and piece[0] != 7 and piece[1] != 0:
                for y, x in zip(range(piece[0] - 1, -1, -1), range(piece[1] + 1, 8)):
                    if (y, x) in player_pieces:
                        valid_moves.append((piece[0] + 1, piece[1] - 1))
                        diagonal.add((piece[0] + 1, piece[1] - 1))
                    elif self.board[y][x] == ' ':
                        break
            if (piece[0] - 1, piece[1] + 1) not in opponent_pieces and (
                    piece[0] - 1, piece[1] + 1) not in player_pieces and piece[0] != 0 and piece[1] != 7:
                for y, x in zip(range(piece[0] + 1, 8), range(piece[1] - 1, -1, -1)):
                    if (y, x) in player_pieces:
                        valid_moves.append((piece[0] - 1, piece[1] + 1))
                        diagonal.add((piece[0] - 1, piece[1] + 1))
                    elif self.board[y][x] == ' ':
                        break

        # Finding actual valid moves (not being used)
        for (row_v, col_v) in valid_moves.copy():
            exists_in_player: bool = False
            for (row, col) in player_pieces:
                if col == col_v or row == row_v or (row_v, col_v) in diagonal:
                    exists_in_player: bool = True
            if not exists_in_player:
                valid_moves.remove((row_v, col_v))
        return valid_moves

    def get_children(self, player_color: str):
        """
        Finding children (possible board states after possible moves) of board
        :param player_color: The color of the player
        :type player_color: str
        :return: A list including children (board instances)
        :rtype: list
        """
        children: list = []
        hr: list = []
        valid_moves: list = self.find_moves(player_color)
        for move in valid_moves:
            child: Board = deepcopy(self)
            child.set_board(move, player_color, valid_moves, hr, player_color)
            children.append(child)
        return children

    def check_win_conditions(self, player_color: str, computer_color: str, print_on: bool):
        """
        Check win conditions and returns win value
        :param player_color: The color of the player
        :type player_color: str
        :param computer_color: The color of the computer
        :type computer_color: str
        :param print_on: Value to print or not
        :type print_on: bool
        :return: The value of the win condition (who won)
        :rtype: str
        """
        player_score: int = 0
        computer_score: int = 0
        for i in range(0, COLUMNS):
            for j in range(0, ROWS):
                if self.board[i][j] == player_color:
                    player_score += 1
                elif self.board[i][j] == computer_color:
                    computer_score += 1
        if print_on:
            if player_score > computer_score:
                print("Victory! Player wins with score {} over Computer's score {} !".format(player_score,
                                                                                             computer_score))
                return 'p'
            elif player_score < computer_score:
                print(
                    "Defeat! Computer wins with score {} over Player's score {} !".format(computer_score,
                                                                                          player_score))
                return 'c'
            elif player_score == computer_score:
                print("Draw! Player and Computer have equal score {} - {} !".format(player_score,
                                                                                    computer_score))
                return '-'
            elif player_score == 0:
                print("Defeat! Computer wins with score {} over Player's score {} !".format(64,
                                                                                            player_score))
                return 'c'
            elif computer_score == 0:
                print("Victory! Player wins with score {} over Computer's score {} !".format(64,
                                                                                             computer_score))
                return 'p'
        else:
            return 0

    def evaluate(self, computer_color: str):
        """
        Evaluates the current board
        :param computer_color: The color of the computer
        :type computer_color:
        :return: The value of the evaluate function
        :rtype: int
        """
        board_value: int = 0
        computer_value: int = 1
        player_value: int = -1

        # Who is who
        if computer_color == 'L':
            player_color: str = 'D'
        else:
            player_color: str = 'L'

        # Iterate through board
        for row in range(0, ROWS):
            for column in range(0, COLUMNS):
                if self.board[row][column] == computer_color:
                    board_value: int = board_value + computer_value
                elif self.board[row][column] == player_color:
                    board_value: int = board_value + player_value

        # In case of game win add 100 to the winner value
        if self.check_win_conditions(player_color, computer_color, False) == 'p':
            board_value = board_value + (player_value * 100)
        elif self.check_win_conditions(player_color, computer_color, False) == 'c':
            board_value = board_value + (computer_value * 100)

        return board_value
