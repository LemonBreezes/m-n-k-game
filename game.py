"""@author: ***REMOVED***
@email: ***REMOVED***
game.py file
Contains main module of this repositry.
https://github.com/LemonBreezes/m-n-k-game"""
# Python module(s)
import random
from itertools import product
from math import sqrt
from time import time
from nop import NOP
from typing import Union, List, Tuple, Dict

# User module(s)
from gui import GUI
from cli import CLI

# Constants
PLAYER_ONE = 0
PLAYER_TWO = 1
BLANK_TILE = 2
NUM_PLAYERS = 2
MINUS_INF = -2
INF = 2
RANDOM = -1
DRAW = -1


class MnkGame:
    """Main module class used to play the (m,n,k) game.
    Attributes:
        num_rows (int): The number of rows in the game board.
        num_columns (int): The number of columns in the game board.
        winning_row_length (int): The length of a winning row.
        is_human_playing (bool): Is a human inputting moves interactively?
        ui (obj): An object which displays output and requests input.
        current_player (int): The player about to make a move.
        outcome (int, optional): The outcome of the current game, if finished.
        board (list): The game board.
        scores (list): The scores of each player.
        num_blanks (int): The number of blank tiles on the game board.
        move_history (list): The history of each move and score for each player.
        zobrist_table (list): A table of hashes for each possible tile state.
        zobrist_hash (int): A hash of the current game board state.
    Args:
        is_human_playing (bool): Disable/Enable AI
        graphic (bool or None): GUI(true), command line interface(false), or no interface (None)
        winning_row_length (int): Number of tiles required in a line to win.
        num_rows (int): Number of rows
        num_col (int): Number of columns
    Raises:
        TypeError: Expected 'int' for num_rows, num_columns, winning_row_length
        TypeError: Expected 'bool' for is_human_playing, graphic
        ValueError: Argument [num_rows, num_col, winning_row_length] needs to be positive
        ValueError: No winning combination possible in [num_rows, num_col, winning_row_length]"""

    def __init__(
        self,
        num_rows: int = 4,
        num_columns: int = 4,
        winning_row_length: int = 3,
        is_human_playing: bool = True,
        graphic: bool = True,
        opening_player: int = RANDOM,
    ) -> None:
        if not isinstance(is_human_playing, bool):
            raise TypeError(f"Expected 'bool' not {type(is_human_playing)}.")
        if not isinstance(graphic, bool) and graphic is not None:
            raise TypeError(f"Expected 'bool' or None not {type(graphic)}.")
        for var in (winning_row_length, num_rows, num_columns):
            if not isinstance(var, int):
                raise TypeError(f"Expected 'int' not {type(var)}")
            if var < 3:
                raise ValueError("All argument needs to be positive.")
            if var < winning_row_length:
                raise ValueError("No winning combination possible")

        self.num_rows: int = num_rows
        self.num_columns: int = num_columns
        self.winning_row_length: int = winning_row_length
        self.is_human_playing: int = is_human_playing

        if graphic == True:
            self.ui = GUI(num_rows, num_columns)
        elif graphic == False:
            self.ui = CLI(num_rows, num_columns)
        else:
            self.ui = NOP()

        self.current_player = (
            random.choice([PLAYER_ONE, PLAYER_TWO])
            if opening_player == RANDOM
            else opening_player
        )
        self.outcome: Union[int, None] = None

        self.board: List[List[int]] = [
            [BLANK_TILE for _ in range(num_columns)] for _ in range(num_rows)
        ]
        self.scores: List[int] = [0, 0]
        self.num_blanks: int = num_rows * num_columns
        self.move_history: List[Tuple[int, int, int]] = []

        # For memoizing minimax function
        self.zobrist_table: List[List[List[int]]] = [
            [
                [random.getrandbits(64) for _ in range(NUM_PLAYERS)]
                for _ in range(num_columns)
            ]
            for _ in range(num_rows)
        ]
        self.zobrist_hash: int = 0

    def start(self) -> None:
        """Main loop for the (m, n, k)-game."""
        self.ui.display_board(self.board)
        while True:
            x, y = self.get_move()
            self.ui.display_move(x, y, self.current_player)
            self.do_move(x, y)
            self.ui.display_board(self.board)
            self.outcome = self.get_game_outcome()
            if self.outcome != None:
                self.ui.display_outcome(self.outcome)
                break

    def get_other_player(self) -> int:
        """Returns the player not who will make the next move,
        if the game does not end before then."""
        return PLAYER_ONE if self.current_player is PLAYER_TWO else PLAYER_TWO

    def switch_players(self) -> None:
        """Changes the player who is currently playing to the other player."""
        self.current_player = self.get_other_player()

    def get_move(self) -> Tuple[int, int]:
        """Returns the move that the current player should make.
        Returns:
            (int, int) A pair of integers representing what point on the board the
            player should mark."""
        if self.current_player == PLAYER_ONE and self.is_human_playing:
            return self.ui.get_human_player_move(self.board)
        return self.get_optimal_move()

    def do_move(self, x, y, player: Union[int, None] = None) -> None:
        """Updates the game state to reflect the player's move choice.
        Args:
            x (int): The horizontal coordinate of the tile to be marked by player.
            y (int): The vertical coordinate of the tile to be marked by player.
            player (int): The player making this move.
        """
        is_simulating_player: bool = bool(player)
        if player is None:
            player = self.current_player

        self.board[x][y] = player
        self.zobrist_hash ^= self.zobrist_table[x][y][player]
        self.num_blanks -= 1
        self.move_history.append((x, y, self.scores[player]))
        for i, j in product(range(-1, 2), range(-1, 2)):
            if i == 0 and j == 0:
                continue

            def is_point_marked_by_current_player(x, y):
                return (
                    0 <= x < self.num_rows
                    and 0 <= y < self.num_columns
                    and self.board[x][y] == player
                )

            if is_point_marked_by_current_player(x + i, y + j):
                curr_score: int = 2
                c, d = x + i, y + j
                while is_point_marked_by_current_player(c + i, d + j):
                    curr_score += 1
                    c, d = c + i, d + j
                c, d = x, y
                while is_point_marked_by_current_player(c - i, d - j):
                    curr_score += 1
                    c, d = c - i, d - j
                self.scores[player] = max(self.scores[player], curr_score)
        if is_simulating_player:
            return
        self.switch_players()

    def undo_move(self, player: Union[int, None] = None) -> None:
        """Restores the board to its previous state.
        Args:
            player (int, optional): The last player to make a move."""
        is_simulating_player: bool = bool(player)
        if player is None:
            player = self.get_other_player()

        x, y, score = self.move_history.pop()
        self.board[x][y] = BLANK_TILE
        self.num_blanks += 1
        if is_simulating_player is False:
            self.switch_players()
        self.zobrist_hash ^= self.zobrist_table[x][y][player]
        self.scores[player] = score

    def get_game_outcome(self) -> Union[int, None]:
        """Returns the outcome of the current game, if it has finished.
        Returns:
            (int) An integer representing the game outcome or nothing at all if the
            game has not finished."""
        for player, score in enumerate(self.scores):
            if score >= self.winning_row_length:
                return player
        if self.num_blanks == 0:
            return DRAW

    def hash_point(self, x, y) -> int:
        """Computes an integer representation of the game board position.
        Args:
            x (int): The horizontal component of the given game board position.
            y (int): The vertical component of the given game board position.
        Returns:
            (int) An integer between 0 and `num_rows*num_columns - 1` representing
            the game board position given by `x` and `y`."""
        return self.num_columns * x + y

    def unhash_point(self, p) -> Tuple[int, int]:
        """Computes the game board position represented by an integer.
        Args:
            p (int): An integer between 0 and `num_rows*num_columns - 1`
            representing a game board position.
        Returns:
            (int, int) A pair of integers representing a game board position.
            """
        return (p // self.num_columns, p % self.num_columns)

    def get_optimal_move(self) -> Tuple[int, int]:
        """Returns the optimal move for the current player to make. When multiple
        moves are equal, the move which is closest to the previous move is selected.
        Returns:
            (int, int) A pair of integers representing a game board position."""
        heuristic_move: Union[Tuple[int, int], None] = self.get_heuristic_move()
        if heuristic_move:
            return heuristic_move

        scores: List[Union[int, None]] = self.score_possible_moves()

        scores = [score if score == max(scores) else None for score in scores]

        def distance(p: int, q: int) -> float:
            """Computes the Euclidean distance between two points.
            Args:
                p (int): A position on the game board in hashed form.
                q (int): Another position on the game board in hashed form.
            Returns:
                (float) The Euclidean distance between the two given points
                on the game board."""
            x, y = self.unhash_point(p)
            a, b = self.unhash_point(q)
            return sqrt(((x - a) ** 2) + ((y - b) ** 2))

        if len(self.move_history) >= 1:
            x, y, _ = self.move_history[-1]
        else:
            x, y = self.num_rows // 2, self.num_columns // 2
        bias: int = self.hash_point(x, y)

        scores = [
            1 / (distance(p, bias) + 1) if scores[p] != None else MINUS_INF
            for p in range(len(scores))
        ]

        return self.unhash_point(max(range(len(scores)), key=scores.__getitem__))

    def get_heuristic_move(self) -> Union[Tuple[int, int], None]:
        """Uses various heuristics to attempt to compute an optimal move without
        using the minimax algorithm. First, this function checks if this move is
        the first move. If so, it returns the most central position on the game
        board. Next, it checks if any player is about to win and returns that
        winning position.
        Returns:
            (int, int) A pair of integers representing the move, if any are
            computed."""
        if len(self.move_history) == 0:
            return self.num_columns // 2, self.num_rows // 2

        def get_winning_move_for_player(player: int) -> Union[Tuple[int, int], None]:
            """Searches for tiles on the game board which are winning moves
            for `player` and returns the first tile found, if any.
            Args:
                player (int): The player whose winning move we are searching for.
            Returns:
                (int, int, optional) The winning move, if any are found."""
            if self.scores[player] == self.winning_row_length - 1:
                for x, y in product(range(self.num_rows), range(self.num_columns)):
                    if self.board[x][y] != BLANK_TILE:
                        continue
                    self.do_move(x, y, player)
                    score: int = self.scores[player]
                    self.undo_move(player)
                    if score >= self.winning_row_length:
                        return x, y

        move: Tuple[int, int] = get_winning_move_for_player(self.current_player)
        if move:
            return move
        other_player: int = self.get_other_player()
        move = get_winning_move_for_player(other_player)
        if move:
            return move

    def score_possible_moves(self) -> List[int]:
        """Scores the possible moves the current player can make using the minimax algorithm.
        Returns:
            (list) A list of scores indexed by hashed board position."""
        result = [MINUS_INF for _ in range(self.num_rows * self.num_columns)]

        scores: Dict[int, int] = {}
        progress: int = 0
        start: float = time()
        for x, y in product(range(self.num_rows), range(self.num_columns)):
            if self.board[x][y] != BLANK_TILE:
                continue
            self.do_move(x, y)
            result[self.hash_point(x, y)] = self.minimax(scores=scores)
            progress += 1
            if time() - start >= 1:
                self.ui.display_progress(
                    progress, self.num_rows*self.num_columns - 1
                )
            self.undo_move()
        return result

    def minimax(
        self,
        is_maximizing: bool = False,
        alpha: int = MINUS_INF,
        beta: int = INF,
        scores: Dict[int, int] = {},
    ) -> int:
        """Recursively computes the score of the current game state.
        Args:
            is_maximizing (bool): True if the current player is the one who
            began the computation. That player is known as the maximizing player.
            prefers moves which lead to faster wins and slower losses.
            alpha (int): The highest score found so far, or -INF.
            beta (int): The lowest score found so far, or INF.
            scores (dict): A hash table of all the maximizing scores computed up to now.
        Returns:
            (int) The score of the game state as it was when this computation began."""
        score: int = scores.get(self.zobrist_hash, None)
        if score:
            return score

        outcome: int = self.get_game_outcome()
        if outcome == DRAW:
            return 0
        if outcome in (PLAYER_ONE, PLAYER_TWO):
            return -1 if is_maximizing else 1

        if is_maximizing:
            optimal_score: int = MINUS_INF
            for x, y in product(range(self.num_rows), range(self.num_columns)):
                if self.board[x][y] != BLANK_TILE:
                    continue
                self.do_move(x, y)
                score = self.minimax(False, alpha, beta, scores)
                scores[self.zobrist_hash] = score
                self.undo_move()
                optimal_score = max(optimal_score, score)
                alpha = max(score, optimal_score)
                if beta <= alpha:
                    break
            return optimal_score
        optimal_score: int = INF
        for x, y in product(range(self.num_rows), range(self.num_columns)):
            if self.board[x][y] != BLANK_TILE:
                continue
            self.do_move(x, y)
            score = self.minimax(True, alpha, beta, scores)
            scores[self.zobrist_hash] = score
            self.undo_move()
            optimal_score = min(optimal_score, score)
            beta = min(score, optimal_score)
            if beta <= alpha:
                break
        return optimal_score
