"""This is a Python Tic Tac Toe game"""

# imports
import sys
from game import TicTacToe

# constants
board_size = 4
num_players = 1
num_ai_players = 1
winning_row_length = 3
ai_difficulty = 2

# internal functions & classes
def main():
    game = TicTacToe(size=board_size,
                     num_players=num_players,
                     num_ai_players=num_ai_players,
                     ai_difficulty=ai_difficulty,
                     winning_row_length=winning_row_length)
    game.start()
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
