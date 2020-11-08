import numpy as np
ROWS = 8
COLUMNS = 8


def create_board():
    return [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 'D', 0, 0, 0, 0],
            [0, 0, 0, 'D', 'D', 0, 0, 0],
            [0, 0, 'L', 'L', 'L', 0, 0, 0],
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


def findPieces(board, play):
    # Finding darks and lights and adding the coordinates in tuple
    matrix = np.array(board)
    darks_ = np.where(matrix == 'D')
    darks = set()
    for i in range(0, len(darks_[0])):
        darks.add((darks_[0][i], darks_[1][i]))
    lights_ = np.where(matrix == 'L')
    lights = set()
    for i in range(0, len(lights_[0])):
        lights.add((lights_[0][i], lights_[1][i]))
    valid_moves = set()
    # Finding valid moves (valid=being around opposite color). Checking also border condition
    if play == 'L':
        for col, row in darks:
            if(col+1, row) not in darks and (col+1, row) not in lights and col != 7:
                valid_moves.add((col+1, row))
            if(col, row+1) not in darks and (col, row+1) not in lights and row != 7:
                valid_moves.add((col, row+1))
            if(col-1, row) not in darks and (col-1, row) not in lights and col != 0:
                valid_moves.add((col-1, row))
            if(col, row-1) not in darks and (col, row-1) not in lights and row != 0:
                valid_moves.add((col, row-1))
        # Finding diagonal
        diagonal = set()
        for col, row in lights:
            for i, j in zip(range(2, COLUMNS-col), range(2, ROWS-row)):
                diagonal.add((col+i, row+j))
                diagonal.add((col-i, row-j))
                diagonal.add((col-i, row+j))
                diagonal.add((col+i, row-j))
        # Finding actual valid moves
        for col_v, row_v in valid_moves.copy():
            for (col, row) in lights:
                if (col != col_v and row != row_v) and (col_v, row_v) not in diagonal:
                    if(col_v, row_v) in valid_moves:
                        valid_moves.remove((col_v, row_v))
    # Finding valid moves (valid=being around opposite color). Checking also border condition
    if play == 'D':
        for col, row in lights:
            if(col+1, row) not in darks and (col+1, row) not in lights and col != 7:
                valid_moves.add((col+1, row))
            if(col, row+1) not in darks and (col, row+1) not in lights and row != 7:
                valid_moves.add((col, row+1))
            if(col-1, row) not in darks and (col-1, row) not in lights and col != 0:
                valid_moves.add((col-1, row))
            if(col, row-1) not in darks and (col, row-1) not in lights and row != 0:
                valid_moves.add((col, row-1))
        # Finding diagonal
        diagonal = set()
        for col, row in darks:
            for i, j in zip(range(2, COLUMNS-col), range(2, ROWS-row)):
                diagonal.add((col+i, row+j))
                diagonal.add((col-i, row-j))
                diagonal.add((col-i, row+j))
                diagonal.add((col+i, row-j))
        # Finding actual valid moves
        for col_v, row_v in valid_moves.copy():
            for (col, row) in darks:
                if (col != col_v and row != row_v) and (col_v, row_v) not in diagonal:
                    if (col_v, row_v) in valid_moves:
                        valid_moves.remove((col_v, row_v))
    return valid_moves


print(findPieces(board_, 'D'))
