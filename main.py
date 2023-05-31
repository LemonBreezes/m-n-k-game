"""This is a Python Tic Tac Toe game"""

# imports
import sys
from game import TicTacToe

# internal functions & classes
def main():
    game = TicTacToe()
    game.start()
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
