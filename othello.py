"""
othello file including gameplay handling
"""
# Import needed modules
from typing import Tuple
import minimax
import board

# STATICS
ROWS: int = 8
COLUMNS: int = 8
col_enumerator: Tuple[str, str, str, str, str, str, str, str] = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
row_enumerator: Tuple[str, str, str, str, str, str, str, str] = ('1', '2', '3', '4', '5', '6', '7', '8')
# STATICS (END)


def col_enum(index):
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


def row_enum(index):
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


# Get column index from element
def col_index(element: str):
    """
    Returning the column index by using the col_enumerator function
    :param element: A string with the element
    :type element: str
    :return: The index in the list of the element
    :rtype: int
    """
    index: int = col_enumerator.index(element)
    return index


# Get row index from element
def row_index(element):
    """
    Return the row index by using the row_enumerator function
    :param element: A string with the element
    :type element: str
    :return: The inxed in the list of the element
    :rtype: int
    """
    index = row_enumerator.index(element)
    return index


class Game:
    """
    Glass game handling te game play
    :var self.player_color: The color of the player
    :type self.player_color: str
    :var self.computer_color: The color of the computer
    :type self.computer_color: str
    :var self.actor_color: The color of the current color
    :type self.actor_color: str
    :var self.game_history: All the boards in the game_history
    :type self.game_history: list
    :var self.boardC: The board of the gameplay
    :type self.boardC: board.Board
    :var self.valid_moves: The valid moves of the current state of the game
    :type self.valid_moves: list
    :var self.show_possible_moves: A flag to show or not the possible moves
    :type self.show_possible_moves: bool
    :var self.difficulty: The selected difficulty
    :type self.diffulty: int
    """
    def __init__(self, player_first: bool, show_possible_moves: bool, difficulty: int):
        """
        __init__ function
        :param player_first: A value showing who is playing first
        :type player_first: bool
        :param show_possible_moves: Indicating if the possible moves will be displayed or not
        :type show_possible_moves: bool
        :param difficulty: The difficulty level
        :type difficulty: int
        """
        self.player_color = None
        self.computer_color = None
        self.actor_color = None
        self.set_colors(player_first)
        self.game_history: list = []  # game history is saved as a list of
        self.boardC: board.Board = board.Board()
        self.valid_moves: list = []
        self.show_possible_moves: bool = show_possible_moves
        self.difficulty: int = difficulty

    # Set colors based on who is playing first
    def set_colors(self, player_first: bool):
        """
        Setting player color according to who is playing first
        :param player_first: A value indicating if the player is playing first
        :type player_first: bool
        :return: Nothing
        :rtype: N/A
        """
        if player_first:
            self.player_color: str = 'D'
            self.computer_color: str = 'L'
            self.actor_color: str = self.player_color
        else:
            self.player_color: str = 'L'
            self.computer_color: str = 'D'
            self.actor_color: str = self.computer_color

    # Print all moves made till now
    def print_history(self):
        """
        Printing the move history
        :return: Nothing
        :rtype: N/A
        """
        i: int = 0
        print("\nGame History:")
        if not self.game_history:
            print("No moves were made yet!\n")
            return 0
        for turn in self.game_history:
            i += 1
            if turn[2] == 'D':
                print("Turn {}: Dark player placed a piece in {}".format(i, col_enum(turn[1])) + row_enum(turn[0]))
            elif turn[2] == 'L':
                print("Turn {}: Light player placed a piece in {}".format(i, col_enum(turn[1])) + row_enum(turn[0]))
        print("\n")

    # Select who is playing
    def turn(self, player_skipped: bool, computer_skipped: bool):
        """
        Chaning players during game play
        :param player_skipped: Checking if the player skipped due to no available moves
        :type player_skipped: bool
        :param computer_skipped: Checking if the computer skipped due to no available moves
        :return: True if the both player and computer skipped meaning that gameplay ends, False if gameplay continues
        :rtype: bool
        """
        # Changing players
        if self.actor_color == self.player_color:
            player_skipped: bool = self.player_move()
            self.actor_color: str = self.computer_color
        else:
            computer_skipped: bool = self.computer_move()
            self.actor_color: str = self.player_color

        # Checking if both player and computer skipped in order to end game
        if player_skipped:
            computer_skipped: bool = self.computer_move()
            self.actor_color: str = self.player_color
            if computer_skipped:
                self.boardC.print_board()
                return True
        elif computer_skipped:
            player_skipped: bool = self.player_move()
            self.actor_color: str = self.computer_color
            if player_skipped:
                self.boardC.print_board()
                return True
        return False

    # Select what happens when the player is playing
    def player_move(self):
        """
        Handles the player_move behavior
        :return: If there any moves left (True if not, False if yes)
        :rtype bool
        """
        self.valid_moves: list = self.boardC.find_moves(self.player_color)
        if not self.valid_moves:  # Checks if list is empty
            print("No valid move player turn skipped!")
            return True
        if self.show_possible_moves:
            self.set_possible()

        print("Turn {}: Your move!".format(len(self.game_history) + 1))
        self.boardC.print_board()
        self.handle_player_input(input("Choose and action (move XY or history): "))
        return False

    def handle_player_input(self, player_input: str):
        """
        Handles player input (move or history display )
        :param player_input: What the player wants to do
        :type player_input: str
        :return: Nothing
        :rtype: N/A
        """
        self.reset_all_marks()
        input_split: list = player_input.split(" ")
        if len(input_split) > 0 and input_split[0] == "move":
            if len(input_split) > 1:
                try:
                    move = (row_index(input_split[1].__getitem__(1)), col_index(input_split[1].__getitem__(0).upper()))
                    (new_piece, self.game_history) = self.boardC.set_board(move, self.actor_color, self.valid_moves,
                                                                           self.game_history,
                                                                           self.actor_color)
                    if not new_piece:
                        self.handle_player_input(input("Choose and action (move XY or history): "))
                except:
                    self.handle_player_input(input("Choose and action (move XY or history): "))
            else:
                self.handle_player_input(input("Choose and action (move XY or history): "))
        elif input_split[0] == "history":
            self.print_history()
            self.handle_player_input(input("Choose and action (move XY or history): "))
        else:
            self.handle_player_input(input("Choose and action (move XY or history): "))

    # Select what happens when the computer is playing
    def computer_move(self):
        """
        Hanles the computer behavior (calling AI)
        :return: If there any moves left (True if not, False if yes)
        :rtype: bool
        """
        self.valid_moves = self.boardC.find_moves(self.computer_color)
        if not self.valid_moves:  # Checks if list is empty
            print("No valid move computer turn skipped!")
            return True
        print("Turn {}: Computer is playing...".format(len(self.game_history) + 1))
        self.boardC.print_board()

        self.boardC.set_board(
            minimax.minimax_move(self.boardC, self.difficulty, self.player_color, self.computer_color),
            self.computer_color, self.valid_moves, self.game_history, self.actor_color)
        return False

    # Reset all X marks
    def reset_all_marks(self):
        """
        Resetting possible moves markes to blank
        :return: Nothing
        :rtype: N/A
        """
        for i in range(0, COLUMNS):
            for j in range(0, ROWS):
                if self.boardC.board[i][j] == 'X':
                    self.boardC.board[i][j] = ' '
        return

    def set_possible(self):
        """
        Displaying possible moves as x on the board
        :return: Nothing
        :rtype: N/A
        """
        for move in self.valid_moves:
            self.boardC.set_board(move, 'X', self.valid_moves, self.game_history, self.actor_color)

    # Starts the actual game
    def play(self):
        """
        Starts the game and keep on playing till finish
        :return: Nothing
        :rtype: N/A
        """
        while True:
            result = self.turn(False, False)
            if result:
                self.boardC.check_win_conditions(self.player_color, self.computer_color, True)
                self.print_history()
                break
        return 0


# Creates a Game item
def start_game(player_first: bool, show_possible_moves: bool, difficulty: int):
    """
    Creates a game item to start the game
    :param player_first: Input on if the player wants to play first
    :type player_first: bool
    :param show_possible_moves: Input on if the possible moves shall be shown
    :type show_possible_moves: bool
    :param difficulty: The difficulty is the actual depth of minimax (max 10)
    :type difficulty: int
    :return: An instance of the game
    :rtype: Game
    """
    if player_first is None:
        condition = True
        while condition:
            player_first = input("Do you want to play first? (Y/N): ")
            if player_first == 'Y':
                player_first = True
                condition = False
            elif player_first == 'N':
                player_first = False
                condition = False

    game: Game = Game(player_first, show_possible_moves, difficulty)
    return game
