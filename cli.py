"""A UI class implementing a command line interface for our game."""

# Python module(s)
from typing import Tuple, List, Dict

# Constants
DRAW: int = -1
PLAYER_ONE: int = 0
PLAYER_TWO: int = 1
BLANK_TILE: int = 2
TILES: Dict[str, int] = {PLAYER_ONE: "X", PLAYER_TWO: "O", BLANK_TILE: " "}


class CLI:
    """The class for our game's command line interface.

    Attributes:
        width (int): The width in pixels of the game window.
        height (int): The height in pixels of the game window.

    Args:
        num_rows (int): The number of rows in the game board.
        num_columns (int): The number of columns in the game board."""

    def __init__(self, num_rows: int, num_columns: int) -> None:
        self.num_rows: int = num_rows
        self.num_columns: int = num_columns

    def display_board(self, board: List[List[int]]) -> None:
        """Prints out the game board.

        Args:
            board (list): The game board."""
        board: str = "|\n|".join(
            ["|".join(map(lambda player: TILES[player], row)) for row in board]
        )
        board = "_" * (2 * self.num_columns) + "_\n|" + board
        board = board + "|\n‾" + "‾" * (2 * self.num_columns)
        print(board)

    def display_outcome(self, winner: int = DRAW) -> None:
        """Prints out the outcome of the game.

        Args:
            winner (int): The player that won."""
        if winner != DRAW:
            print("Player {winner} has won!".format(winner=TILES[winner]))
        else:
            print("Draw!")

    def display_move(self, x: int, y: int, player: int) -> None:
        """Prints out the move the player made.

        Args:
            x (int): The horizontal coordinate of the tile to be marked by player.
            y (int): The vertical coordinate of the tile to be marked by player.
            player (int): The player making this move."""
        print(f"Player {player} marks {x+1} {y+1}")

    def is_move_invalid(self, x: int, y: int, board: List[List[int]]) -> None:
        """Determines if the coordinates given represent a blank tile on the
        game board.

        Args:
            x (int): A horizontal coordinate.
            y (int): A vertical coordinate.
            board (list): The game board."""
        return (
            x < 0
            or y < 0
            or x >= self.num_columns
            or y >= self.num_columns
            or board[x][y] != BLANK_TILE
        )

    def get_human_player_move(self, board: List[List[int]]) -> Tuple[int, int]:
        """Queries the player to make a move until they make a move which
        represents an unoccupied tile on the game board.

        Args:
            board (list): The game board.

        Returns:
            (int, int): The coordinates of the move the player has chosen."""
        x, y = (int(x) - 1 for x in input("Make your move: ").split())
        while self.is_move_invalid(x, y, board):
            print("Your choice of move is invalid.")
            x, y = [int(x) - 1 for x in input("Make your move: ").split()]
        return x, y
