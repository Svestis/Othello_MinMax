"""
exercise1 file including game start
"""
# Importing needed modules
import othello
import argparse


def print_hi(name: str ):
    """
    Printing the welcoming message
    :param name: The name of the player
    :type name: str
    :return: Nothing
    :rtype: N/A
    """
    print(f'Hi, {name}')
    print()


def parse_arguments():
    """
    Parsing the passed arguments
    :return: Nothing
    :rtype: N/A
    """
    parser = argparse.ArgumentParser(description='Othello settings')


if __name__ == '__main__':
    """
    Initiating game play
    """
    print_hi('AUEB Artificial Intelligence Course Exerscise 1 2020-2021')
    # DEBUG MAIN (START)
    game = othello.start_game('Υ', True, 4)
    difficulty = game.difficulty  # TODO add reading from user and max value check at 10
    player_color = game.player_color
    game.play()
    # DEBUG MAIN (END)
