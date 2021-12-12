from itertools import product
from copy import deepcopy

class Board():
    def __init__(self, size, board=None, lines=None, num_blanks=None):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)] if board is None else board
        self.lines = [set() for p in range(size**2)] if lines is None else lines
        self.num_blanks = size**2 if num_blanks is None else num_blanks

    @classmethod
    def from_board(cls, class_instance):
        board = deepcopy(class_instance.board)
        size = class_instance.size
        lines = deepcopy(class_instance.lines)
        num_blanks = class_instance.num_blanks
        return cls(size=size, board=board, lines=lines, num_blanks=num_blanks)

    def hash(self, x, y):
        return x*self.size + y

    def unhash(self, p):
        return [p // self.size, p % self.size]

    def add_mark(self, x, y, player_id):
        self.board[x][y] = player_id
        self.num_blanks -= 1
        for i, j in product(range(-1,2), range(-1,2)):
            if i == 0 and j == 0:
                continue
            if self.is_point_marked_by_player(x+i, y+j, player_id):
                aligned_points = {self.hash(x, y), self.hash(x+i, y+j)}
                c, d = x+i, y+j
                while self.is_point_marked_by_player(c + i, d + j, player_id):
                    aligned_points.add((c + i, d + j))
                    c, d = c + i, d + j
                c, d = x, y
                while self.is_point_marked_by_player(c - i, d - j, player_id):
                    aligned_points.add((c - i, d - j))
                    c, d = c - i, d - j
                self.lines[self.hash(x,y)] = self.lines[self.hash(x+i,y+j)] = aligned_points

    def is_point_marked_by_player(self, x, y, player_id):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == player_id

    def is_point_marked(self, move):
        x, y = move
        return 0 <= x < self.size and 0 <= y <= self.size and self.board[x][y] != 0

    def get_player_with_score(self, score):
        for p, lines in enumerate(self.lines):
            if len(lines) >= score:
                x, y = self.unhash(p)
                return self.board[x][y]
        if self.num_blanks == 0:
            return -1
        return 0

    def __str__(self):
        board = '|\n|'.join(['|'.join(map(str, row)) for row in self.board])
        board = '_' * (self.size * 2) + '_\n|' + board
        board = board + '|\n‾' + '‾' * (self.size * 2)
        return board
