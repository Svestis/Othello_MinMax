import numpy as np

ROWS = 8
COLUMNS = 8
col_enumerator = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
row_enumerator = ('1', '2', '3', '4', '5', '6', '7', '8')


def col_enum(id):
    return col_enumerator[id]


def row_enum(id):
    return row_enumerator[id]


def col_index(element):
    return col_enumerator.index(element)


def row_index(element):
    return row_enumerator.index(element)


def create_board():
    return [[' ', ' ', 'L', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'D', 'L', 'L', 'L', 'L', ' '],
            [' ', ' ', ' ', 'D', 'D', 'L', ' ', ' '],
            [' ', ' ', ' ', 'L', 'L', 'D', ' ', ' '],
            ['D', 'D', 'L', 'L', 'D', 'D', 'D', ' '],
            [' ', 'L', 'L', ' ', 'D', 'D', 'D', ' '],
            ['L', ' ', ' ', ' ', 'D', 'D', ' ', ' '],
            [' ', ' ', ' ', ' ', 'D', ' ', ' ', ' ']]


def set_board(move, value, board):
    if move[0] > 8 or move[1] > 8:
        raise IndexError("Row and column should be less than or equal to 8. Please try again")
    board[move[0]][move[1]] = value


def print_board(board):
    def print_header():
        print("     ", end='')
        for i in range(ord('a'), ord('i')):
            print(chr(i), end='')
            print("     ", end='')

    print_header()
    for i in range(0, ROWS):
        print("")
        print("  -------------------------------------------------")
        print(str(i + 1) + " ", end='')

        for j in range(0, COLUMNS):
            print("| ", board[i][j], " ", end='')

        print("| ", end='')
        print(str(i + 1) + " ", end='')
    print("")
    print("  -------------------------------------------------")
    print_header()
    print()
    print()


def find_moves(board, player_color):
    if player_color == 'L':
        opponent_color = 'D'
    else:
        opponent_color = 'L'
    # Finding darks and lights and adding the coordinates in tuple
    matrix = np.array(board)
    player_pieces_ = np.where(matrix == player_color)
    player_pieces = set()
    for i in range(0, len(player_pieces_[0])):
        player_pieces.add((player_pieces_[0][i], player_pieces_[1][i]))
    opponent_pieces_ = np.where(matrix == opponent_color)
    opponent_pieces = set()
    for i in range(0, len(opponent_pieces_[0])):
        opponent_pieces.add((opponent_pieces_[0][i], opponent_pieces_[1][i]))
    valid_moves = set()
    diagonal = set()
    print("Player pieces: {}".format(player_pieces))
    print("Opponent pieces: {}".format(opponent_pieces))
    # Finding valid moves (valid=being around opposite color). Checking also border condition
    for piece in opponent_pieces:
        if (piece[0], piece[1] + 1) not in opponent_pieces and (piece[0], piece[1] + 1) not in player_pieces and piece[1] != 7:
            for x in range(piece[1] - 1, -1, -1):
                if (piece[0], x) in player_pieces:
                    valid_moves.add((piece[0], piece[1] + 1))
                elif board[piece[0]][x] == ' ':
                    break
        if (piece[0] + 1, piece[1]) not in opponent_pieces and (piece[0] + 1, piece[1]) not in player_pieces and piece[0] != 7:
            for y in range(piece[0] - 1, -1, -1):
                if (y, piece[1]) in player_pieces:
                    valid_moves.add((piece[0] + 1, piece[1]))
                elif board[y][piece[1]] == ' ':
                    break
        if (piece[0], piece[1] - 1) not in opponent_pieces and (piece[0], piece[1] - 1) not in player_pieces and piece[1] != 0:
            for x in range(piece[1] + 1, 8):
                if (piece[0], x) in player_pieces:
                    valid_moves.add((piece[0], piece[1] - 1))
                elif board[piece[0]][x] == ' ':
                    break
        if (piece[0] - 1, piece[1]) not in opponent_pieces and (piece[0] - 1, piece[1]) not in player_pieces and piece[0] != 0:
            for y in range(piece[0] + 1, 8):
                if (y, piece[1]) in player_pieces:
                    valid_moves.add((piece[0] - 1, piece[1]))
                elif board[y][piece[1]] == ' ':
                    break
        # Finding diagonal
        if (piece[0] - 1, piece[1] - 1) not in opponent_pieces and (piece[0] - 1, piece[1] - 1) not in player_pieces and piece[0] != 0 and piece[1] != 0:
            for y, x in zip(range(piece[0] + 1, 8), range(piece[1] + 1, 8)):
                if (y, x) in player_pieces:
                    valid_moves.add((piece[0] - 1, piece[1] - 1))
                    diagonal.add((piece[0] - 1, piece[1] - 1))
                elif board[y][x] == ' ':
                    break
        if (piece[0] + 1, piece[1] + 1) not in opponent_pieces and (piece[0] + 1, piece[1] + 1) not in player_pieces and piece[0] != 8 and piece[1] != 8:
            for y, x in zip(range(piece[0] - 1, -1, -1), range(piece[1] - 1, -1, -1)):
                if (y, x) in player_pieces:
                    valid_moves.add((piece[0] + 1, piece[1] + 1))
                    diagonal.add((piece[0] + 1, piece[1] + 1))
                elif board[y][x] == ' ':
                    break
        if (piece[0] + 1, piece[1] - 1) not in opponent_pieces and (piece[0] + 1, piece[1] - 1) not in player_pieces and piece[0] != 8 and piece[1] != 0:
            for y, x in zip(range(piece[0] - 1, -1, -1), range(piece[1] + 1, 8)):
                if (y, x) in player_pieces:
                    valid_moves.add((piece[0] + 1, piece[1] - 1))
                    diagonal.add((piece[0] + 1, piece[1] - 1))
                elif board[y][x] == ' ':
                    break
        if (piece[0] - 1, piece[1] + 1) not in opponent_pieces and (piece[0] - 1, piece[1] + 1) not in player_pieces and piece[0] != 0 and piece[1] != 8:
            for y, x in zip(range(piece[0] + 1, 8), range(piece[1] - 1, -1, -1)):
                if (y, x) in player_pieces:
                    valid_moves.add((piece[0] - 1, piece[1] + 1))
                    diagonal.add((piece[0] - 1, piece[1] + 1))
                elif board[y][x] == ' ':
                    break

    print("Valid Moves before diagonal: {}".format(valid_moves))
    # Finding actual valid moves
    for (row_v, col_v) in valid_moves.copy():
        exists_in_player = False
        for (row, col) in player_pieces:
            if col == col_v or row == row_v or (row_v, col_v) in diagonal:
                exists_in_player = True
        if not exists_in_player:
            valid_moves.remove((row_v, col_v))

    return valid_moves


def set_possible(board, moves):
    print("Valid Moves final: {}".format(moves))
    for move in moves:
        set_board(move, 'X', board)


board_ = create_board()

set_possible(board_, find_moves(board_, 'D'))
print_board(board_)
