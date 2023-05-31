"""This is a Python Tic Tac Toe game"""

# imports
import sys
from game import TicTacToe

<<<<<<< HEAD
# constants
board_size = 4
num_human_players = 1
num_ai_players = 1
winning_row_length = 3
ai_difficulty = 2

=======
>>>>>>> 77584fe (Began writing GUI)
# internal functions & classes
def main():
    game = TicTacToe()
    game.start()
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
