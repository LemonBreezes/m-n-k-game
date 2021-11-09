import sys
import unittest
from main import *
from numpy import array_equal

class TestTicTacToeBoard(unittest.TestCase):
    def test_addMark(self):
        board = TicTacToeBoard(size=3, num_players=1, winning_row_length=3)
        board.addMark(x=1,y=1,player=1)
        self.assertEqual(board.getBoard(), [[1, 0, 0], [0, 0, 0], [0, 0, 0]])
        board.addMark(x=1,y=2,player=1)
        self.assertEqual(board.getBoard(), [[1, 1, 0], [0, 0, 0], [0, 0, 0]])
        board.addMark(x=1,y=3,player=1)
        self.assertEqual(board.getBoard(), [[1, 1, 1], [0, 0, 0], [0, 0, 0]])
        
    def test_getWinner(self):
        board = TicTacToeBoard(size=3, num_players=1, winning_row_length=3)
        board._board = [[1, 1, 1],
                        [0, 0, 0],
                        [0, 0, 0]]
        self.assertEqual(board.getWinner(), 1)
        board._board = [[1, 0, 1],
                        [0, 1, 0],
                        [0, 0, 0]]
        self.assertEqual(board.getWinner(), 0)
        board._board = [[1, 1, 0],
                        [1, 0, 1],
                        [0, 1, 1]]
        self.assertEqual(board.getWinner(), 0)
        board._board = [[1, 1, 0],
                        [1, 1, 1],
                        [0, 1, 1]]
        self.assertEqual(board.getWinner(), 1)

def main():
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    unittest.TextTestRunner(verbosity=2).run(suite)
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
