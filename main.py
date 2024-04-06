"""@author: LemonBreezes

main.py file for demonstrating the use of the m_n_k_game module.

https://github.com/LemonBreezes/m-n-k-game"""

# Python module(s)
import sys
from argparse import ArgumentParser, BooleanOptionalAction

# User module(s)
from game import MnkGame

# Constants
RANDOM = 0


def main():
    parser = ArgumentParser(description="Play an (m, n, k)-game.")
    parser.add_argument(
        "-r",
        "--rows",
        type=int,
        default=4,
        help="Set the number of rows that are in the game board.",
    )
    parser.add_argument(
        "-c",
        "--columns",
        type=int,
        default=4,
        help="Set the number of columns that are in the game board.",
    )
    parser.add_argument(
        "-w",
        "--winning-row-length",
        type=int,
        default=3,
        help="Set how many aligned tiles are required to win.",
    )
    parser.add_argument(
        "-ai",
        "--ai-only",
        action=BooleanOptionalAction,
        default=False,
        help="Watch two AIs play against each other.",
    )
    parser.add_argument(
        "-nw",
        "--no-window",
        action=BooleanOptionalAction,
        default=False,
        help="Play in a commandline interface.",
    )
    parser.add_argument(
        "-o",
        "--opening-player",
        type=int,
        default=RANDOM,
        help="""What turn do you want to make your first move on?
        Set to either 1, 2, or -1 for a random player order.""",
    )
    args = parser.parse_args()

    game = MnkGame(
        num_rows=args.rows,
        num_columns=args.columns,
        winning_row_length=args.winning_row_length,
        is_human_playing=not args.ai_only,
        graphic=not args.no_window,
        opening_player=args.opening_player - 1,
    )
    game.start()
    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
