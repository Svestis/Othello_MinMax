"""
exercise1 file including game start
"""
# Importing needed modules
import othello
import argparse


def print_hi(name: str):
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
    parser.add_argument('pf', metavar='play_first', help="Do you want to play first? (True to play first or "
                                                         "False to play second)")
    parser.add_argument('po', metavar='print_output', help="Do you want to print the output? ('True' or "
                                                           "'False')")
    parser.add_argument('df', metavar='difficulty', type=int, help="Difficulty level (max=10)")
    return parser.parse_args()


if __name__ == '__main__':
    """
    Initiating game play
    """
    arguments = vars(parse_arguments())
    if arguments['pf'] != 'False' and arguments['pf'] != 'True' and arguments['po'] != 'False' \
            and arguments['po'] != 'True' and (arguments['df'] > 10 or arguments['df'] < 0
                                               or not (isinstance(arguments['df'], int))):
        print('Problem in one of the arguments passed.\nUsing standard arguments True True 5')
        df = 5
        pf = True
        po = True
    else:
        pf = False
        po = False
        if arguments.get('pf') == 'True':
            pf = True
        if arguments.get('po') == 'True':
            po = True
        df: int = arguments.get('df')

    name: str = input("Welcome, what's your name?\n")
    print_hi(name)
    # DEBUG MAIN (START)
    game = othello.start_game(pf, po, int(df))
    game.play()
    # DEBUG MAIN (END)
