"""@author: ***REMOVED***

@email: ***REMOVED***

main.py file for demonstrating the use of the m_n_k_game module.

https://github.com/LemonBreezes/m-n-k-game"""

# Python module(s)
import sys

# User module(s)
from game import MnkGame

def main():
    game = MnkGame()
    game.start()
    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
