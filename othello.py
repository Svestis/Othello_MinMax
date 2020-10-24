ROWS = 8
COLUMNS = 8


def create_board():
    board = [[0] * COLUMNS] * ROWS
    return board


def set_board(row, column, value, board):
    if row > 8 or column > 8:
        raise IndexError("Row and column should be less than or equal to 8. Please try again")

    board[row][column] = value
    return board


def print_board(board):
    print_header()
    for i in range(0, ROWS):
        print("")
        print("  -------------------------------------------------")
        print(str(i+1) + " ", end='')

        for j in range(0, COLUMNS):
            print("| ", board[i][j], " ", end='')

        print("| ", end='')
        print(str(i+1) + " ", end='')
    print("")
    print("  -------------------------------------------------")
    print_header()


def print_header():
    print("     ", end='')
    for i in range(ord('a'), ord('i')):
        print(chr(i), end='')
        print("     ", end='')


board_ = create_board()
print_board(board_)