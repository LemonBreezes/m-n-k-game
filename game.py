from time import sleep
from collections import deque

from ai import AI
from player import Player
from board import Board

class TicTacToe():
    def __init__(self, size, num_players, num_ai_players, ai_difficulty, winning_row_length):
        self.board = Board(size=size)
        self.size = size
        self.num_players = num_players
        self.num_ai_players = num_ai_players
        self.ai_difficulty = ai_difficulty
        self.winning_row_length = winning_row_length

    def start(self):
        players = []
        for i in range(self.num_players):
            players.append(Player(player_id=i+1))
        for i in range(self.num_ai_players):
            players.append(AI(player_id=self.num_players+i+1,
                              difficulty=self.ai_difficulty,
                              num_players=self.num_players + self.num_ai_players,
                              winning_row_length=self.winning_row_length))

        self.board.display()
        turn = 0
        while True:
            x, y = players[turn].get_move(self.board)
            self.board.add_mark(x, y, turn+1)
            self.board.display()
            winner = self.board.get_player_with_score(self.winning_row_length)
            if winner == -1:
                print('Draw!')
                break
            elif winner != 0:
                print('Player ' + str(winner) + ' is the winner!')
                break
            turn = (turn + 1) % len(players)
            sleep(1)
