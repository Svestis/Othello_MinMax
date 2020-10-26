ROWS = 8
COLUMNS = 8


def create_board():
    return [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 'L', 'D', 0, 0, 0],
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
