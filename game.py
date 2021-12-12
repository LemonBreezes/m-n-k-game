from time import sleep
from collections import deque

from ai import AI
from player import Player
from board import Board

class TicTacToe():
    def __init__(self, size, num_human_players, num_ai_players, ai_difficulty,
               winning_row_length, running_tests=False):
        self.board = Board(size=size, num_players=num_human_players + num_ai_players)
        self.size = size
        self.num_human_players = num_human_players
        self.num_ai_players = num_ai_players
        self.ai_difficulty = ai_difficulty
        self.winning_row_length = winning_row_length
        self.running_tests = running_tests

    def start(self):
        players = []
        for i in range(self.num_human_players):
            players.append(Player(player_id=i+1))
        for i in range(self.num_ai_players):
            players.append(AI(player_id=self.num_human_players+i+1,
                              difficulty=self.ai_difficulty,
                              num_players=self.num_human_players + self.num_ai_players,
                              winning_row_length=self.winning_row_length))

        if not self.running_tests:
            print(str(self.board))
        turn = 0
        while True:
            player = players[turn]
            x, y = player.get_move(self.board)
            if not self.running_tests:
                print('Player', player.player_id, 'marks', x, y, sep=' ')
            self.board.add_mark(x, y, player.player_id)
            if not self.running_tests:
                print(str(self.board))
            if self.board.get_player_score(player.player_id) >= self.winning_row_length:
                if self.running_tests:
                    self.winner = player.player_id
                else:
                    print('Player ' + str(player.player_id) + ' is the winner!')
                break
            elif self.board.is_game_over():
                if self.running_tests:
                    self.winner = -1
                else:
                    print('Draw!')
                break
            turn = (turn + 1) % len(players)

    def get_winner(self):
        return self.winner
