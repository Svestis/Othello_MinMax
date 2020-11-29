import numpy as np
from copy import deepcopy

# STATICS
ROWS = 8
COLUMNS = 8
col_enumerator = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
row_enumerator = ('1', '2', '3', '4', '5', '6', '7', '8')


# STATICS (END)

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


class Board:
    def __init__(self, board: list = '', last_move: tuple = ''):
        if board == '':
            self.board = self.create_board()
        else:
            self.board = board
        self.last_move = last_move

    @staticmethod
    def create_board():
        return [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', 'L', 'D', ' ', ' ', ' '],
                [' ', ' ', ' ', 'D', 'L', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

    def set_board(self, move, value, valid_moves, game_history, actor_color):
        def move_exists():
            for valid_move in valid_moves:
                if (move[0], move[1]) == valid_move:
                    return True
            return False

        if move[0] > 8 or move[1] > 8:
            raise IndexError("Row and column should be less than or equal to 8. Please try again")
        if move_exists():
            self.board[move[0]][move[1]] = value
            if value == 'D' or value == 'L':
                game_history.append((move[0], move[1], value))
                self.last_move = (move[0], move[1])
                self.flip_opponent_pieces(move, actor_color)
            return move, game_history
        else:
            print("Your piece can't be placed in {}{}. It is not a valid move.".format(col_enum(move[1]),
                                                                                       row_enum(move[0])))
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
        print(self.last_move)

    def flip_opponent_pieces(self, piece, actor_color):
        if actor_color == 'L':
            opponent_color = 'D'
        else:
            opponent_color = 'L'
        # Finding darks and lights and adding the coordinates in tuple
        matrix = np.array(self.board)
        player_pieces_ = np.where(matrix == actor_color)
        player_pieces = set()
        for i in range(0, len(player_pieces_[0])):
            player_pieces.add((player_pieces_[0][i], player_pieces_[1][i]))
        opponent_pieces_ = np.where(matrix == opponent_color)
        opponent_pieces = set()
        for i in range(0, len(opponent_pieces_[0])):
            opponent_pieces.add((opponent_pieces_[0][i], opponent_pieces_[1][i]))
        pieces_to_flip = []
        # if (piece[0], piece[1] + 1) not in opponent_pieces and (piece[0], piece[1] + 1) not in player_pieces and piece[1] != 7:
        for x in range(piece[1] - 1, -1, -1):
            if (piece[0], x) in opponent_pieces:  # If next piece is opponent's add it to the list
                pieces_to_flip.append((piece[0], x))
            elif self.board[piece[0]][x] == actor_color:
                for single_piece in pieces_to_flip:  # If next piece is actor's flip it
                    self.board[single_piece[0]][single_piece[1]] = actor_color
                break
            elif self.board[piece[0]][x] == ' ':  # If next piece is blank
                break
        pieces_to_flip.clear()
        for y in range(piece[0] - 1, -1, -1):
            if (y, piece[1]) in opponent_pieces:
                pieces_to_flip.append((y, piece[1]))
            elif self.board[y][piece[1]] == actor_color:
                for single_piece in pieces_to_flip:
                    self.board[single_piece[0]][single_piece[1]] = actor_color
                break
            elif self.board[y][piece[1]] == ' ':
                break
        pieces_to_flip.clear()
        for x in range(piece[1] + 1, 8):
            if (piece[0], x) in opponent_pieces:
                pieces_to_flip.append((piece[0], x))
            elif self.board[piece[0]][x] == actor_color:
                for single_piece in pieces_to_flip:
                    self.board[single_piece[0]][single_piece[1]] = actor_color
                break
            elif self.board[piece[0]][x] == ' ':
                break
        pieces_to_flip.clear()
        for y in range(piece[0] + 1, 8):
            if (y, piece[1]) in opponent_pieces:
                pieces_to_flip.append((y, piece[1]))
            elif self.board[y][piece[1]] == actor_color:
                for single_piece in pieces_to_flip:
                    self.board[single_piece[0]][single_piece[1]] = actor_color
                break
            elif self.board[y][piece[1]] == ' ':
                break
        pieces_to_flip.clear()
        # Finding diagonal
        for y, x in zip(range(piece[0] + 1, 8), range(piece[1] + 1, 8)):
            if (y, x) in opponent_pieces:
                pieces_to_flip.append((y, x))
            elif self.board[y][x] == actor_color:
                for single_piece in pieces_to_flip:
                    self.board[single_piece[0]][single_piece[1]] = actor_color
                break
            elif self.board[y][x] == ' ':
                break
        pieces_to_flip.clear()
        for y, x in zip(range(piece[0] - 1, -1, -1), range(piece[1] - 1, -1, -1)):
            if (y, x) in opponent_pieces:
                pieces_to_flip.append((y, x))
            elif self.board[y][x] == actor_color:
                for single_piece in pieces_to_flip:
                    self.board[single_piece[0]][single_piece[1]] = actor_color
                break
            elif self.board[y][x] == ' ':
                break
        pieces_to_flip.clear()
        for y, x in zip(range(piece[0] - 1, -1, -1), range(piece[1] + 1, 8)):
            if (y, x) in opponent_pieces:
                pieces_to_flip.append((y, x))
            elif self.board[y][x] == actor_color:
                for single_piece in pieces_to_flip:
                    self.board[single_piece[0]][single_piece[1]] = actor_color
                break
            elif self.board[y][x] == ' ':
                break
        pieces_to_flip.clear()
        for y, x in zip(range(piece[0] + 1, 8), range(piece[1] - 1, -1, -1)):
            if (y, x) in opponent_pieces:
                pieces_to_flip.append((y, x))
            elif self.board[y][x] == actor_color:
                for single_piece in pieces_to_flip:
                    self.board[single_piece[0]][single_piece[1]] = actor_color
                break
            elif self.board[y][x] == ' ':
                break
        pieces_to_flip.clear()
        return self.board

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

        # print("Valid Moves before diagonal: {}".format(valid_moves))
        # Finding actual valid moves
        for (row_v, col_v) in valid_moves.copy():
            exists_in_player = False
            for (row, col) in player_pieces:
                if col == col_v or row == row_v or (row_v, col_v) in diagonal:
                    exists_in_player = True
            if not exists_in_player:
                valid_moves.remove((row_v, col_v))
        return valid_moves

    def get_children(self, player_color):
        children = []
        hr = []
        valid_moves = self.find_moves(player_color)
        for move in valid_moves:
            child = deepcopy(self)
            child.set_board(move, player_color, valid_moves, hr, player_color)
            children.append(child)
        return children

    def evaluate(self, computer_color):
        board_value = 0
        computer_value = 1
        player_value = -1
        if computer_color == 'L':
            player_color = 'D'
        else:
            player_color = 'L'
        for row in range(0, ROWS):
            for column in range(0, COLUMNS):
                if self.board[row][column] == computer_color:
                    board_value = board_value + computer_value
                elif self.board[row][column] == player_color:
                    board_value = board_value + player_value
            print(board_value)
        return board_value

    def check_win_conditions(self, player_color, computer_color):
        player_score = 0
        computer_score = 0
        for i in range(0, COLUMNS):
            for j in range(0, ROWS):
                if self.board[i][j] == player_color:
                    player_score += 1
                elif self.board[i][j] == computer_color:
                    computer_score += 1
        if player_score > computer_score:
            print("Victory! Player wins with score {} over Computer's score {} !".format(player_score, computer_score))
            return 'p'
        elif player_score < computer_score:
            print("Defeat! Computer wins with score {} over Player's score {} !".format(computer_score, player_score))
            return 'c'
        elif player_score == computer_score:
            print("Draw! Player and Computer have equal score {} - {} !".format(player_score, computer_score))
            return '-'
        elif player_score == 0:
            print("Defeat! Computer wins with score {} over Player's score {} !".format(64, player_score))
            return 'c'
        elif computer_score == 0:
            print("Victory! Player wins with score {} over Computer's score {} !".format(64, computer_score))
            return 'p'
