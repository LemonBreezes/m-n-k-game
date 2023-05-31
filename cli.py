"""A UI class implementing a CLI for our game."""

# Python module(s)
from typing import Tuple, List

# Constants
DRAW: int = -1
PLAYER_ONE: int = 0
PLAYER_TWO: int = 1
BLANK_TILE: int = 2
TILES: Dict[str, int] = {PLAYER_ONE: "X", PLAYER_TWO: "O", BLANK_TILE: " "}


class CLI:
    def __init__(self, num_rows: int, num_columns: int) -> None:
        self.num_rows: int = num_rows
        self.num_columns: int = num_columns

    def display_board(self, board: List[List[int]]) -> None:
        board: str = "|\n|".join(["|".join(map(self.tile_to_string, row)) for row in board])
        board = "_" * (2 * self.num_columns) + "_\n|" + board
        board = board + "|\n‾" + "‾" * (2 * self.num_columns)
        print(board)

    def display_outcome(self, winner: int=DRAW) -> None:
        if winner != DRAW:
            print("Player {winner} has won!".format(winner=TILES[winner]))
        else:
            print("Draw!")

    def display_move(self, x: int, y: int, player: int) -> None:
        print(f"Player {player} marks {x} {y}")

    def is_move_invalid(self, x: int, y: int, board: List[List[int]]) -> None:
        return (
            x < 0
            or y < 0
            or x >= self.num_columns
            or y >= self.num_columns
            or board[x][y] != BLANK_TILE
        )

    def get_human_player_move(self, board: List[List[int]]) -> Tuple[int, int]:
        x, y = (int(x) - 1 for x in input("Make your move: ").split())
        while self.is_move_invalid(x, y, board):
            print("Your choice of move is invalid.")
            x, y = [int(x) - 1 for x in input("Make your move: ").split()]
        return x, y

    def tile_to_string(self, tile: int) -> str:
        return TILES[tile]
