import othello
import argparse


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Othello settings')


if __name__ == '__main__':
    print_hi('AUEB Artificial Intelligence Course Exerscise 1 2020-2021')
    # DEBUG MAIN (START)
    game = othello.start_game('Υ', True, 5)
    difficulty = game.difficulty  # TODO add reading from user and max value check at 10
    player_color = game.player_color
    game.play()
    # DEBUG MAIN (END)
