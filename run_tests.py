import sys
import unittest

from game import *

PLAYER_ONE = 0
PLAYER_TWO = 1
BLANK_TILE = 2
DRAW = -1


class gameTests(unittest.TestCase):
    def test_undo(self):
        """Tests that undoing restores the game board to its previous state."""
        game = MnkGame(
            num_rows=3,
            num_columns=3,
            winning_row_length=3,
            is_human_playing=False,
            graphic=None,
            opening_player=PLAYER_ONE,
        )
        blank_board = [
            [BLANK_TILE for _ in range(game.num_columns)] for _ in range(game.num_rows)
        ]
        game.do_move(1, 1)
        game.undo_move()
        self.assertEqual(game.board, blank_board)
        game.do_move(1, 1)
        game.do_move(0, 1)
        game.undo_move()
        game.undo_move()
        self.assertEqual(game.board, blank_board)

    def test_switch_players(self):
        """Tests that switching players does not leave the current player
        unchanged."""
        game = MnkGame(
            num_rows=3,
            num_columns=3,
            winning_row_length=3,
            is_human_playing=False,
            graphic=None,
            opening_player=PLAYER_ONE,
        )
        player = game.current_player
        game.switch_players()
        self.assertIsNot(player, game.current_player)
        game.switch_players()
        self.assertEqual(player, game.current_player)

    def test_minimax(self):
        """Tests that our simulated AI versus AI games finish in the Nash
        equilibrium."""
        game = MnkGame(
            num_rows=3,
            num_columns=3,
            winning_row_length=3,
            is_human_playing=False,
            graphic=None,
            opening_player=PLAYER_ONE,
        )
        blank_board = [
            [BLANK_TILE for _ in range(game.num_columns)] for _ in range(game.num_rows)
        ]
        self.assertEqual(blank_board, game.board)
        game = MnkGame(
            num_rows=4,
            num_columns=4,
            winning_row_length=3,
            is_human_playing=False,
            graphic=None,
            opening_player=PLAYER_ONE,
        )
        game.start()
        self.assertEqual(game.outcome, PLAYER_ONE)
        game = MnkGame(
            num_rows=3,
            num_columns=3,
            winning_row_length=3,
            is_human_playing=False,
            graphic=None,
            opening_player=PLAYER_ONE,
        )
        game.start()
        self.assertEqual(game.outcome, DRAW)

    def test_get_move(self):
        """Tests that the AI does not modify the game board when computing its
        next move."""
        game = MnkGame(
            num_rows=3,
            num_columns=3,
            winning_row_length=3,
            is_human_playing=False,
            graphic=None,
            opening_player=PLAYER_ONE,
        )
        blank_board = [
            [BLANK_TILE for _ in range(game.num_columns)] for _ in range(game.num_rows)
        ]
        game.get_move()
        self.assertEqual(blank_board, game.board)

    def test_get_game_outcome(self):
        """Tests that we can detect when a player makes a winning row."""
        game = MnkGame(
            num_rows=3,
            num_columns=3,
            winning_row_length=3,
            is_human_playing=False,
            graphic=None,
            opening_player=PLAYER_ONE,
        )
        game.do_move(0, 0)
        game.do_move(1, 1)
        game.do_move(0, 1)
        game.do_move(1, 0)
        game.do_move(0, 2)
        self.assertEqual(game.get_game_outcome(), PLAYER_ONE)


def main():
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    unittest.TextTestRunner(verbosity=2).run(suite)
    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
