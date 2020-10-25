import othello
import minimax
import argparse


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Othello settings')


if __name__ == '__main__':
    print_hi('AUEB Artificial Intelligence Course Exerscise 1 2020-2021')
    board = othello.create_board()
    othello.print_board(board)
    othello.set_board(2, 2, 1, board)
    othello.print_board(board)
