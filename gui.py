"""gui.py file

A GUI class for pygame.

Note: In this files pylint configured to ignore 'no member' because of C
    implementation of several pygame members like constants MOUSEBUTTONDOWN and
    methods like init()"""

# Python module(s)
import sys
from time import sleep
from itertools import product
import pygame
from pygame.locals import *

# Constants
BLOCKSIZE = 90
HALF_BLOCKSIZE = BLOCKSIZE // 2
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
DRAW = -1
PLAYER_ONE = 0
PLAYER_TWO = 1
BLANK_TILE = 2
TILES = {PLAYER_ONE: 'X', PLAYER_TWO: 'O', BLANK_TILE: ' '}

# Disabling pylint because of partial implementation of pygame in C, which is not
# recognizable by pylint.
# pylint: disable=no-member

class GUI:
    def __init__(self, num_rows, num_columns):
        self.width = num_rows * BLOCKSIZE
        self.height = num_columns * BLOCKSIZE

        pygame.init()
        pygame.font.init()
        self.screen = self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Python Tic Tac Toe")

    def display_board(self, board):
        self.draw_background()
        for x, y in product(
            range(0, self.width, BLOCKSIZE), range(0, self.height, BLOCKSIZE)
        ):
            self.draw_rect(x, y)
            tile = board[x // BLOCKSIZE][y // BLOCKSIZE]
            if tile != BLANK_TILE:
                self.draw_text(x + HALF_BLOCKSIZE, y + HALF_BLOCKSIZE, TILES[tile])
        pygame.display.update()

    def display_outcome(self, winner):
        message = ""
        if winner != DRAW:
            message = "Player {winner} has won!".format(winner=TILES[winner])
        else:
            message = "Draw!"
        self.draw_text(self.width // 2, self.height // 2, message)
        pygame.display.update()
        sleep(1.5)

    def display_move(self, x, y, player):
        pass

    def get_human_player_move(self, board):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = [c // BLOCKSIZE for c in pygame.mouse.get_pos()]
                    if board[x][y] == BLANK_TILE:
                        return [x, y]


    def display_progress(self, progress, total):
        pass

    def draw_text(self, x, y, s):
        font_size = 64 if len(str(s)) < 7 else 32
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(str(s), True, WHITE, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_rect(self, x, y):
        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(self.screen, WHITE, rect, 1)

    def draw_background(self):
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, BLOCKSIZE))
