import numpy as np
ROWS = 8
COLUMNS = 8


def create_board():
    return [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 'D', 0, 0, 0, 0],
            [0, 0, 0, 'D', 'D', 0, 0, 0],
            [0, 0, 0, 'D', 'L', 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]


def set_board(row, column, value, board):
    if row > 8 or column > 8:
        raise IndexError("Row and column should be less than or equal to 8. Please try again")
    board[row][column] = value


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


board_ = create_board()
print_board(board_)


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
    print("Player pieces: {}".format(player_pieces))
    print("Opponent pieces: {}".format(opponent_pieces))
    # Finding valid moves (valid=being around opposite color). Checking also border condition
    for col, row in opponent_pieces:
        if(col+1, row) not in opponent_pieces and (col+1, row) not in player_pieces and col != 7:
            valid_moves.add((col+1, row))
        if(col, row+1) not in opponent_pieces and (col, row+1) not in player_pieces and row != 7:
            valid_moves.add((col, row+1))
        if(col-1, row) not in opponent_pieces and (col-1, row) not in player_pieces and col != 0:
            valid_moves.add((col-1, row))
        if(col, row-1) not in opponent_pieces and (col, row-1) not in player_pieces and row != 0:
            valid_moves.add((col, row-1))
    # Finding diagonal
    diagonal = set()
    print("Valid Moves: {}".format(valid_moves))
    for col, row in player_pieces:
        for i, j in zip(range(1, COLUMNS-col), range(1, ROWS-row)):
            diagonal.add((col+i, row+j))
            diagonal.add((col-i, row-j))
            diagonal.add((col-i, row+j))
            diagonal.add((col+i, row-j))
    # Finding actual valid moves
    for (col_v, row_v) in valid_moves.copy():
        exists_in_player = False
        for (col, row) in player_pieces:
            if col == col_v or row == row_v:
                exists_in_player = True
        if not exists_in_player:
            valid_moves.remove((col_v, row_v))
    return valid_moves

print(find_moves(board_, 'L'))