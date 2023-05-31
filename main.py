"""This is an (m,n,k)-game"""

# imports
import sys
from game import mnkGame

DRAW = -1
GUI = True
CLI = False

# internal functions & classes
def main():
    game = mnkGame()
    game.start()
    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
