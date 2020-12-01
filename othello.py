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
        self.set_color(player_first)
        self.game_history: list = []  # game history is saved as a list of
        self.boardC: board.Board = board.Board()
        self.valid_moves: list = []
        self.show_possible_moves: bool = show_possible_moves
        self.difficulty: int = difficulty


    # Set colors based on who is playing first
    def set_color(self, player_first):
        if player_first:
            self.player_color = 'D'
            self.computer_color = 'L'
            self.actor_color = self.player_color
        else:
            self.player_color = 'L'
            self.computer_color = 'D'
            self.actor_color = self.computer_color

    # Print all moves made till now
    def print_history(self):
        i = 0
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
    def turn(self):
        global player_skipped, computer_skipped
        if self.actor_color == self.player_color:
            player_skipped = self.player_move()
            self.actor_color = self.computer_color
        else:
            computer_skipped = self.computer_move()
            self.actor_color = self.player_color

        if player_skipped and computer_skipped:
            return True

        return False

    # Select what happens when the player is playing
    def player_move(self):
        self.valid_moves = self.boardC.find_moves(self.player_color)
        if not self.valid_moves:  # Checks if list is empty
            print("No valid move player turn skipped!")
            return True
        if self.show_possible_moves:
            self.set_possible()

        print("Turn {}: Your move!".format(len(self.game_history) + 1))
        self.boardC.print_board()
        # random.seed(random.randint(0, 1001))
        # random_move = random.randint(0, len(self.valid_moves) - 1)  # TODO this will change, implement AI
        # self.set_board(self.valid_moves[random_move], self.player_color)  # TODO this will change, implement AI
        self.handle_player_input(input("Choose and action (move XY or history): "))
        return False

    def handle_player_input(self, player_input):
        self.reset_all_marks()
        input_split = player_input.split(" ")
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
        self.valid_moves = self.boardC.find_moves(self.computer_color)
        if not self.valid_moves:  # Checks if list is empty
            print("No valid move computer turn skipped!")
            return True
        print("Turn {}: Computer is playing...".format(len(self.game_history) + 1))
        self.boardC.print_board()

        # random.seed(54736 + random.randint(-1, 124125))
        # random_move = random.randint(0, len(self.valid_moves) - 1)  # TODO this will change, implement AI
        # (x, self.game_history) = self.boardC.set_board(self.valid_moves[random_move], self.computer_color,self.valid_moves, self.game_history,self.actor_color)  # TODO this will change, implement AI
        self.boardC.set_board(
            minimax.minimax_move(self.boardC, self.difficulty, self.player_color, self.computer_color),
            self.computer_color, self.valid_moves, self.game_history, self.actor_color)
        return False

    # Reset all X marks
    def reset_all_marks(self):
        for i in range(0, COLUMNS):
            for j in range(0, ROWS):
                if self.boardC.board[i][j] == 'X':
                    self.boardC.board[i][j] = ' '
        return

    def set_possible(self):
        # print("Valid Moves final: {}".format(self.valid_moves))
        for move in self.valid_moves:
            self.boardC.set_board(move, 'X', self.valid_moves, self.game_history, self.actor_color)

    # Starts the actual game
    def play(self):
        while True:
            # print("Printing possible moves children")
            # ch = self.boardC.get_children(self.actor_color)
            # for item in ch:
            #     item.print_board()
            # print("Board Value ", item.evaluate(self.computer_color))
            result = self.turn()
            if result:
                self.boardC.check_win_conditions(self.player_color, self.computer_color, True)
                self.print_history()
                break
        return 0


# Creates a Game item
def start_game(player_color, show_possible_moves, difficulty): # TODO switching color does not work
    if player_color is None:
        player_color = input("Do you want to play first? (Y/N): ")

    if player_color == 'Y':
        player_color = 'D' # TODO by convention dark plays first. Do you think that we should change it?
    else:
        player_color = 'L'

    game = Game(player_color, show_possible_moves, difficulty)
    return game
