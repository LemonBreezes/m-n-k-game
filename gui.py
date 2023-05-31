"""A UI class implementing a GUI for with PyGame.

Note: In this files pylint configured to ignore 'no member' because of C
    implementation of several pygame members like constants MOUSEBUTTONDOWN and
    methods like init()"""

# Python module(s)
import sys
from time import sleep
from itertools import product
import pygame
from pygame.locals import *
from typing import Tuple, Dict, List, TypeVar

# Constants
BLOCKSIZE: int = 90
HALF_BLOCKSIZE: int = BLOCKSIZE // 2
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (200, 200, 200)
DRAW: int = -1
PLAYER_ONE: int = 0
PLAYER_TWO: int = 1
BLANK_TILE: int = 2
TILES: Dict[str, int] = {PLAYER_ONE: "X", PLAYER_TWO: "O", BLANK_TILE: " "}

# Disabling pylint because of partial implementation of pygame in C, which is not
# recognizable by pylint.
# pylint: disable=no-member


class GUI:
    """UI class for PyGame GUI.
    Attributes:
        width (int): The width in pixels of the game window.
        height (int): The height in pixels of the game window.
        screen (obj): An object representing the game window.
    Args:
        num_rows (int): The number of rows in the game board.
        num_columns (int): The number of columns in the game board."""

    def __init__(self, num_rows: int, num_columns: int) -> None:
        """Initializes a blank game window."""
        self.width: int = num_rows * BLOCKSIZE
        self.height: int = num_columns * BLOCKSIZE

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Python Tic Tac Toe")

    def display_board(self, board: List[List[int]]) -> None:
        """Draws the background and game board onto the game window."""
        self.draw_background()
        for x, y in product(
            range(0, self.width, BLOCKSIZE), range(0, self.height, BLOCKSIZE)
        ):
            self.draw_rect(x, y)
            tile: int = board[x // BLOCKSIZE][y // BLOCKSIZE]
            if tile != BLANK_TILE:
                self.draw_text(x + HALF_BLOCKSIZE, y + HALF_BLOCKSIZE, TILES[tile])
        pygame.display.update()

    def display_outcome(self, winner: int) -> None:
        """Displays the outcome of the game on the game window."""
        message: str = ""
        if winner != DRAW:
            message = "Player {winner} has won!".format(winner=TILES[winner])
        else:
            message = "Draw!"
        self.draw_text(self.width // 2, self.height // 2, message)
        pygame.display.update()
        sleep(1.5)

    def display_move(self, x: int, y: int, player: int) -> None:
        """This function does not currently do anything."""
        pass

    def get_human_player_move(self, board: List[List[int]]) -> Tuple[int, int]:
        """Waits until the user enters a game move or closes the window."""
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = [c // BLOCKSIZE for c in pygame.mouse.get_pos()]
                    if board[x][y] == BLANK_TILE:
                        return (x, y)

    def draw_text(self, x: int, y: int, s: str) -> None:
        """Draws text onto the game window at the given coordinates"""
        font_size: int = 64 if len(str(s)) < 7 else 32
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(str(s), True, WHITE, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_rect(self, x: int, y: int) -> None:
        """Draws a rectangle onto the game window at the given coordinates."""
        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(self.screen, WHITE, rect, 1)

    def draw_background(self) -> None:
        """Draws the background for the game window."""
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, BLOCKSIZE))
