"""This is an (m,n,k)-game"""
import sys
from game import MnkGame

def main():
    game = MnkGame()
    game.start()
    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
