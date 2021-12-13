from itertools import product
import pygame
pygame.font.init()

# constants
BLOCKSIZE = 90

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

class GUI:
    def __init__(self, num_rows, num_columns):
        # TODO Calculate window size from the Tic Tac Toe parameters
        self.width = num_rows * BLOCKSIZE
        self.height = num_columns * BLOCKSIZE
        self.screen = self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Python Tic Tac Toe')

        self.font = pygame.font.Font(None, 64)

    def display_board(self, board):
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, BLOCKSIZE))
        for x, y in product(range(0, self.width, BLOCKSIZE),
                         range(0, self.height,BLOCKSIZE)):
                rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

                text_surface = self.font.render(
                    str(board.board[x // BLOCKSIZE][y // BLOCKSIZE]), True, WHITE, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = (x + 0.5*BLOCKSIZE, y + 0.5*BLOCKSIZE)
                self.screen.blit(text_surface, text_rect)
        pygame.display.update()


    def display_outcome(self, player_id):
        pass

    def display_move(self, x, y, player):
        pass
