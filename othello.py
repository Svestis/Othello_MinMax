import numpy as np
import random

# STATICS
ROWS = 8
COLUMNS = 8
col_enumerator = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
row_enumerator = ('1', '2', '3', '4', '5', '6', '7', '8')


# Converts number to column letter
def col_enum(index):
    if index < len(col_enumerator):
        return col_enumerator[index]
    return False


# Converts number to row number
def row_enum(index):
    if index < len(row_enumerator):
        return row_enumerator[index]
    return False


# Get column index from element
def col_index(element):
    index = col_enumerator.index(element)
    return index


# Get row index from element
def row_index(element):
    index = row_enumerator.index(element)
    return index


class Game:

    def __init__(self, player_first, show_possible_moves):
        self.player_color = None
        self.computer_color = None
        self.actor_color = None
        self.set_color(player_first)
        self.game_history = []  # game history is saved as a list of (row, col, actor_color)
        self.board = self.create_board()
        self.valid_moves = []
        self.show_possible_moves = show_possible_moves

    @staticmethod
    def create_board():
        return [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 'L', 'D', 0, 0, 0],
                [0, 0, 0, 'D', 'L', 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

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

    # Add value to board coordinates
    def set_board(self, move, value):
        def move_exists():
            for valid_move in self.valid_moves:
                if (move[1], move[0]) == valid_move:
                    return True
            return False

        if move[0] > 8 or move[1] > 8:
            raise IndexError("Row and column should be less than or equal to 8. Please try again")
        if move_exists():
            self.board[move[1]][move[0]] = value
            if value == self.player_color or value == self.computer_color:
                self.game_history.append((move[0], move[1], value))
            return move
        else:
            print("Your piece can't be placed in {}{}. It is not a valid move.".format(col_enum(move[0]),
                                                                                       row_enum(move[1])))
            return False

    # Print the current board state
    def print_board(self):
        def print_header():
            print("     ", end='')
            for i in range(ord('A'), ord('I')):
                print(chr(i), end='')
                print("     ", end='')

        print_header()
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
        print_header()
        print()
        print()

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
                print("Turn {}: Dark player placed a piece in {}".format(i, col_enum(turn[0])) + row_enum(turn[1]))
            elif turn[2] == 'L':
                print("Turn {}: Light player placed a piece in {}".format(i, col_enum(turn[0])) + row_enum(turn[1]))
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
        self.valid_moves = self.find_moves(self.player_color)
        if not self.valid_moves:  # Checks if list is empty
            print("No valid move player turn skipped!")
            return True
        if self.show_possible_moves:
            self.set_possible()

        print("Turn {}: Your move!".format(len(self.game_history) + 1))
        self.print_board()
        self.handle_player_input(input("Choose and action (move XY or history): "))
        return False

    def handle_player_input(self, player_input):
        input_split = player_input.split(" ")
        if len(input_split) > 0 and input_split[0] == "move":
            if len(input_split) > 1:
                # if col_index(input_split[1].__getitem__(0).upper()) and row_index(input_split[1].__getitem__(1)):
                #     self.handle_player_input(input("Choose and action (move XY or history): "))
                try:
                    move = (
                    (col_index(input_split[1].__getitem__(0).upper())), row_index(input_split[1].__getitem__(1)))
                    new_piece = self.set_board(move, self.player_color)
                    if not new_piece:
                        self.handle_player_input(input("Choose and action (move XY or history): "))
                    else:
                        self.flip_opponent_pieces(new_piece)
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
        self.valid_moves = self.find_moves(self.computer_color)
        if not self.valid_moves:  # Checks if list is empty
            print("No valid move computer turn skipped!")
            return True
        print("Turn {}: Computer is playing...".format(len(self.game_history) + 1))
        self.print_board()

        random.seed(1412)
        random_move = random.randint(0, len(self.valid_moves) - 1, )  # TODO this will change, implement AI
        self.set_board(self.valid_moves[random_move], self.computer_color)  # TODO this will change, implement AI

        return False

    # Flip all opponent pieces
    def flip_opponent_pieces(self, move):

        self.reset_all_marks()
        return

    # Reset all X marks
    def reset_all_marks(self):
        for i in range(0, COLUMNS):
            for j in range(0, ROWS):
                if self.board[i][j] == 'X':
                    self.board[i][j] = 0
        return

    # Find all possible move for current round
    def find_moves(self, player_color):
        if player_color == 'L':
            opponent_color = 'D'
        else:
            opponent_color = 'L'
        # Finding darks and lights and adding the coordinates in tuple
        matrix = np.array(self.board)
        player_pieces_ = np.where(matrix == player_color)
        player_pieces = set()
        for i in range(0, len(player_pieces_[0])):
            player_pieces.add((player_pieces_[0][i], player_pieces_[1][i]))
        opponent_pieces_ = np.where(matrix == opponent_color)
        opponent_pieces = set()
        for i in range(0, len(opponent_pieces_[0])):
            opponent_pieces.add((opponent_pieces_[0][i], opponent_pieces_[1][i]))
        valid_moves = []
        diagonal = set()
        # print("Player pieces: {}".format(player_pieces))
        # print("Opponent pieces: {}".format(opponent_pieces))
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
                    piece[0] + 1, piece[1] + 1) not in player_pieces and piece[0] != 8 and piece[1] != 8:
                for y, x in zip(range(piece[0] - 1, -1, -1), range(piece[1] - 1, -1, -1)):
                    if (y, x) in player_pieces:
                        valid_moves.append((piece[0] + 1, piece[1] + 1))
                        diagonal.add((piece[0] + 1, piece[1] + 1))
                    elif self.board[y][x] == ' ':
                        break
            if (piece[0] + 1, piece[1] - 1) not in opponent_pieces and (
                    piece[0] + 1, piece[1] - 1) not in player_pieces and piece[0] != 8 and piece[1] != 0:
                for y, x in zip(range(piece[0] - 1, -1, -1), range(piece[1] + 1, 8)):
                    if (y, x) in player_pieces:
                        valid_moves.append((piece[0] + 1, piece[1] - 1))
                        diagonal.add((piece[0] + 1, piece[1] - 1))
                    elif self.board[y][x] == ' ':
                        break
            if (piece[0] - 1, piece[1] + 1) not in opponent_pieces and (
                    piece[0] - 1, piece[1] + 1) not in player_pieces and piece[0] != 0 and piece[1] != 8:
                for y, x in zip(range(piece[0] + 1, 8), range(piece[1] - 1, -1, -1)):
                    if (y, x) in player_pieces:
                        valid_moves.append((piece[0] - 1, piece[1] + 1))
                        diagonal.add((piece[0] - 1, piece[1] + 1))
                    elif self.board[y][x] == ' ':
                        break

        # print("Valid Moves before diagonal: {}".format(valid_moves))
        # Finding actual valid moves
        for (row_v, col_v) in valid_moves.copy():
            exists_in_player = False
            for (row, col) in player_pieces:
                if col == col_v or row == row_v or (row_v, col_v) in diagonal:
                    exists_in_player = True
            if not exists_in_player:
                valid_moves.remove((row_v, col_v))

        self.valid_moves = valid_moves
        return self.valid_moves

    def set_possible(self):
        # print("Valid Moves final: {}".format(self.valid_moves))
        for move in self.valid_moves:
            self.set_board(move, 'X')

    # Starts the actual game
    def play(self):
        while True:
            result = self.turn()
            if result:
                self.check_win_conditions()
                break
        return 0

    def check_win_conditions(self):
        player_score = 0
        computer_score = 0
        for i in range(0, COLUMNS):
            for j in range(0, ROWS):
                if self.board[i][j] == self.player_color:
                    player_score += 1
                elif self.board[i][j] == self.computer_color:
                    computer_score += 1
        if player_score > computer_score:
            print("Victory! Player wins with score {} over Computer's score {} !".format(player_score, computer_score))
        elif player_score < computer_score:
            print("Defeat! Computer wins with score {} over Player's score {} !".format(computer_score, player_score))
        elif player_score == computer_score:
            print("Draw! Player and Computer have equal score {} - {} !".format(player_score, computer_score))
        elif player_score == 0:
            print("Defeat! Computer wins with score {} over Player's score {} !".format(64, player_score))
        elif computer_score == 0:
            print("Victory! Player wins with score {} over Computer's score {} !".format(64, computer_score))
        self.print_history()


# Creates a Game item
def start_game(player_color, show_possible_moves):
    if player_color is None:
        player_color = input("Do you want to play first? (Y/N): ")

    if player_color == 'Y':
        player_color = 'D'
    else:
        player_color = 'L'

    game = Game(player_color, show_possible_moves)
    return game
