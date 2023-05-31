import sys
from time import sleep
from itertools import product
import pygame
from pygame.locals import *
pygame.font.init()

# constants
BLOCKSIZE = 90

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

class GUI:
    def __init__(self, num_rows, num_columns):
        self.width = num_rows * BLOCKSIZE
        self.height = num_columns * BLOCKSIZE
        self.screen = self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Python Tic Tac Toe')


    def display_board(self, board):
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, BLOCKSIZE))
        for x, y in product(range(0, self.width, BLOCKSIZE),
                         range(0, self.height,BLOCKSIZE)):
                rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
                mark = board.board[x // BLOCKSIZE][y // BLOCKSIZE]
                if mark != 0:
                    self.draw_text(x + BLOCKSIZE // 2, y + BLOCKSIZE // 2, mark)
        pygame.display.update()


    def display_outcome(self, winner):
        message = ''
        if winner > 0:
            message = 'Player {player_id} has won!'.format(player_id=str(winner))
        else:
            message = 'Draw!'
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
                    x, y = [c  // BLOCKSIZE for c in pygame.mouse.get_pos()]
                    if board.board[x][y] == 0:
                        return [x, y]

    def draw_text(self, x, y, s):
        font_size = 64 if len(str(s)) < 7 else 32
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(
            str(s), True, WHITE, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
