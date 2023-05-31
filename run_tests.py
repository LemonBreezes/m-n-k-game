import sys
import unittest

from board import Board
from game import TicTacToe

class BoardTests(unittest.TestCase):
    def test_add_mark(self):
        board = Board(size=3)
        board.add_mark(0,0,player_id=1)
        self.assertEqual(board.board, [[1, 0, 0], [0, 0, 0], [0, 0, 0]])
        board.add_mark(0,1,player_id=1)
        self.assertEqual(board.board, [[1, 1, 0], [0, 0, 0], [0, 0, 0]])
        board.add_mark(0,2,player_id=1)
        self.assertEqual(board.board, [[1, 1, 1], [0, 0, 0], [0, 0, 0]])
        
    def test_get_player_with_score(self):
        board = Board(size=3)
        # board.board = [[1, 1, 1],
        #                [0, 0, 0],
        #                [0, 0, 0]]
        board.add_mark(0,0,1)
        board.add_mark(1,0,1)
        board.add_mark(2,0,1)
        self.assertEqual(board.get_player_with_score(3), 1)
        board = Board(size=3)
        # board.board = [[1, 0, 1],
        #                [0, 1, 0],
        #                [0, 0, 0]]
        board.add_mark(0,0,1)
        board.add_mark(0,2,1)
        board.add_mark(1,1,1)
        self.assertEqual(board.get_player_with_score(3), 0)
        # board.board = [[1, 2, 1],
        #                 [2, 1, 2],
        #                 [2, 1, 2]]
        board.add_mark(0,1,2)
        board.add_mark(1,0,2)
        board.add_mark(1,2,2)
        board.add_mark(2,0,2)
        board.add_mark(2,1,1)
        board.add_mark(2,2,2)
        self.assertEqual(board.get_player_with_score(3), -1)
        board = Board(size=3)
        # board.board = [[1, 1, 0],
        #                 [1, 0, 1],
        #                 [0, 1, 1]]
        board.add_mark(0,0,1)
        board.add_mark(0,1,1)
        board.add_mark(1,0,1)
        board.add_mark(1,2,1)
        board.add_mark(2,1,1)
        board.add_mark(2,2,1)
        self.assertEqual(board.get_player_with_score(3), 0)
        # board.board = [[1, 1, 0],
        #                 [1, 1, 1],
        #                 [0, 1, 1]]
        board.add_mark(1,1,1)
        self.assertEqual(board.get_player_with_score(3), 1)


class AITests(unittest.TestCase):
    def test_minimax(self):
        game = TicTacToe(size=3,
                         num_players=0,
                         num_ai_players=2,
                         ai_difficulty=2,
                         winning_row_length=3,
                         running_tests = True)
        game.start()
        self.assertEqual(game.get_winner(), -1)

def main():
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    unittest.TextTestRunner(verbosity=2).run(suite)
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
