from itertools import product
from copy import deepcopy


class Board:
    def __init__(
        self,
        num_rows=None,
        num_columns=None,
        num_players=None,
        board=None,
        lines=None,
        num_blanks=None,
        scores=None,
    ):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.board = (
            [[0 for _ in range(num_columns)] for _ in range(num_rows)]
            if board is None
            else board
        )
        self.scores = [0 for _ in range(num_players + 1)] if num_players else scores
        self.num_blanks = num_rows * num_columns if num_blanks is None else num_blanks

    @classmethod
    def from_board(cls, class_instance):
        board = deepcopy(class_instance.board)
        scores = deepcopy(class_instance.scores)
        num_rows = class_instance.num_rows
        num_columns = class_instance.num_columns
        num_blanks = class_instance.num_blanks
        return cls(
            num_rows=num_rows,
            num_columns=num_columns,
            board=board,
            scores=scores,
            num_blanks=num_blanks,
        )

    def hash(self, x, y):
        return self.num_columns * x + y

    def unhash(self, p):
        return [p // self.num_columns, p % self.num_columns]

    def add_mark(self, x, y, player_id):
        self.board[x][y] = player_id
        self.num_blanks -= 1
        for i, j in product(range(-1, 2), range(-1, 2)):
            if i == 0 and j == 0:
                continue
            if self.is_point_marked_by_player(x + i, y + j, player_id):
                curr_score = 2
                c, d = x + i, y + j
                while self.is_point_marked_by_player(c + i, d + j, player_id):
                    curr_score += 1
                    c, d = c + i, d + j
                c, d = x, y
                while self.is_point_marked_by_player(c - i, d - j, player_id):
                    curr_score += 1
                    c, d = c - i, d - j
                self.scores[player_id] = max(self.scores[player_id], curr_score)

    def is_point_marked_by_player(self, x, y, player_id):
        return (
            0 <= x < self.num_rows
            and 0 <= y < self.num_columns
            and self.board[x][y] == player_id
        )

    def is_point_marked(self, move):
        x, y = move
        return (
            0 <= x < self.num_rows
            and 0 <= y <= self.num_columns
            and self.board[x][y] != 0
        )

    def get_player_score(self, player_id):
        return self.scores[player_id]

    def has_no_blanks(self):
        return self.num_blanks == 0

    def __str__(self):
        board = "|\n|".join(["|".join(map(str, row)) for row in self.board])
        board = "_" * (2 * self.num_columns) + "_\n|" + board
        board = board + "|\n‾" + "‾" * (2 * self.num_columns)
        return board
