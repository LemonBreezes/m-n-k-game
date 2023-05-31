from time import sleep
from collections import deque
import pygame

from ai import AI
from player import Player
from board import Board
from gui import GUI

class TicTacToe():
    def __init__(self,
               num_rows=3,
               num_columns=3,
               num_human_players=1,
               num_ai_players=1,
               ai_difficulty=2,
               winning_row_length=3,
               graphical=True):
        self.board = Board(num_rows=num_rows,
                           num_columns=num_columns,
                           num_players=num_human_players + num_ai_players)
        self.num_human_players = num_human_players
        self.num_ai_players = num_ai_players
        self.ai_difficulty = ai_difficulty
        self.winning_row_length = winning_row_length
        self.num_rows = num_rows
        self.num_columns = num_columns

        self.graphical = graphical

    def display_move(self, x, y, player):
        player_id = player.player_id
        if self.graphical:
            self.gui.display_move(x, y, player_id)
        elif self.graphical == False:
            print('Player {player_id} marks {x} {y}'.format(player_id,x,y))

    def display_board(self):
        if self.graphical:
            self.gui.display_board(self.board)
        elif self.graphical == False:
            print(str(self.board))

    def display_outcome(self, winner=-1):
        if self.graphical:
            self.gui.display_outcome(winner)
        elif self.graphical == False:
            if winner > 0:
                print('Player {winner} is the winner!'.format(winner))
            else:
                print('Draw!')

    def get_game_outcome(self, player_id):
        if self.board.get_player_score(player_id) >= self.winning_row_length:
            return player_id
        elif self.board.has_no_blanks():
            return 'Draw'

    def do_turn(self, player):
        x, y = player.get_move(self.board)
        self.display_move(x, y, player)
        self.board.add_mark(x, y, player.player_id)
        self.display_board()

    def start(self):
        players = []
        for i in range(self.num_human_players):
            players.append(Player(player_id=i+1))
        for i in range(self.num_ai_players):
            players.append(AI(player_id=self.num_human_players+i+1,
                              difficulty=self.ai_difficulty,
                              num_players=self.num_human_players + self.num_ai_players,
                              winning_row_length=self.winning_row_length))

        if self.graphical:
            self.gui = GUI(self.num_rows, self.num_columns)
        self.display_board()
        turn = 0
        while True:
            player = players[turn]
            self.do_turn(player)
            self.winner = self.get_game_outcome(player.player_id)
            if self.winner:
                self.display_outcome(winner=self.winner)
                break
            turn = (turn + 1) % len(players)

    def get_winner(self):
        return self.winner
