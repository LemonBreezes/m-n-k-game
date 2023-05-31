from random import randrange
from functools import lru_cache
from itertools import product
from math import inf

from board import Board

class AI():
    def __init__(self, player_id, difficulty, num_players, winning_row_length):
        self.difficulty = difficulty
        self.player_id = player_id
        self.num_players = num_players
        self.winning_row_length = winning_row_length

    def get_move(self, board):
        if self.difficulty == 1:
            return self.get_random_move(board)
        else:
            return self.get_optimal_move(board)

    def get_random_move(self, board):
        while (True):
            move = [randrange(board.size), randrange(board.size)]
            if not board.is_point_marked(move):
                return move

    def get_possible_next_states(self, board, curr_player):
        possible_next_states = [None for x, y in product(range(board.size), range(board.size))]
        for x, y in product(range(board.size), range(board.size)):
            if not board.is_point_marked([x, y]):
                temp = board.from_board(board)
                temp.add_mark(x, y, curr_player)
                possible_next_states[board.hash(x, y)] = temp
        return possible_next_states

    def get_optimal_move(self, board):
        if board.num_blanks == 9 and board.size == 3:
            return [1, 1]
        possible_next_states = self.get_possible_next_states(board, self.player_id)
        scores = [self.score_state(state, prev_player=self.player_id)
                  if state is not None
                  else (- inf)
                  for state in possible_next_states]
        return board.unhash(max(range(len(scores)), key=scores.__getitem__))

    def score_state(self, board, prev_player, depth = 0):
        winner = board.get_player_with_score(self.winning_row_length)
        next_player = max((prev_player + 1) % (self.num_players + 1),1)
        if winner == -1:
            return 0
        elif winner > 0:
            return depth + 1 if winner == self.player_id else -(depth + 1)
        possible_next_states = self.get_possible_next_states(board, next_player)
        if prev_player != self.player_id:
            return max([self.score_state(state, next_player, depth + 1)
                   if state
                   else (- inf)
                   for state in possible_next_states])
        else:
            return min([self.score_state(state, next_player, depth + 1)
                   if state
                   else inf
                   for state in possible_next_states])