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

    def get_move(self, board, ui):
        if self.difficulty == 1:
            return self.get_random_move(board)
        else:
            return self.get_optimal_move(board)

    def get_random_move(self, board):
        while (True):
            move = [randrange(board.num_rows), randrange(board.num_columns)]
            if not board.is_point_marked(move):
                return move

    def get_possible_next_states(self, board, curr_player):
        possible_next_states = [None for x, y in product(range(board.num_rows), range(board.num_columns))]
        for x, y in product(range(board.num_rows), range(board.num_columns)):
            if not board.is_point_marked([x, y]):
                temp = board.from_board(board)
                temp.add_mark(x, y, curr_player)
                possible_next_states[board.hash(x, y)] = temp
        return possible_next_states

    def get_optimal_move(self, board):
        possible_next_states = self.get_possible_next_states(board, self.player_id)
        scores = [self.score_state(state, prev_player=self.player_id)
                  if state is not None
                  else (- inf)
                  for state in possible_next_states]
        print('Minimax scores: {scores}'.format(
            p_id=self.player_id,scores=scores))
        return board.unhash(max(range(len(scores)), key=scores.__getitem__))

    def score_state(self, board, prev_player, depth=1, alpha=-inf, beta=inf):
        if board.get_player_score(prev_player) >= self.winning_row_length:
            return 1/depth if prev_player == self.player_id else -1/depth
        elif board.has_no_blanks():
            return 0

        current_player = max((prev_player+1)%(self.num_players+1),1)
        if current_player == self.player_id:
            optimal_score = -inf
            for x, y in product(range(board.num_rows), range(board.num_columns)):
                if board.is_point_marked([x, y]):
                    continue
                state = board.from_board(board)
                state.add_mark(x, y, current_player)
                score = self.score_state(state, current_player, depth+1, alpha, beta)
                optimal_score = max(optimal_score, score)
                alpha = max(score, optimal_score)
                if beta <= alpha:
                    break
            return optimal_score
        else:
            optimal_score = inf
            for x, y in product(range(board.num_rows), range(board.num_columns)):
                if board.is_point_marked([x, y]):
                    continue
                temp = board.from_board(board)
                temp.add_mark(x, y, current_player)
                score = self.score_state(temp, current_player, depth+1, alpha, beta)
                optimal_score = min(optimal_score, score)
                beta = min(score, optimal_score)
                if beta <= alpha:
                    break
            return optimal_score
