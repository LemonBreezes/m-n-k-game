import sys
import unittest
from main import *
from numpy import array_equal

class TestTicTacToeBoard(unittest.TestCase):
    def test_addMark(self):
        board = TicTacToeBoard(3)
        board.addMark(x=1,y=1,player=1)
        self.assertEqual(board._board, [[1, 0, 0], [0, 0, 0], [0, 0, 0]])
        board.addMark(x=1,y=2,player=1)
        self.assertEqual(board._board, [[1, 1, 0], [0, 0, 0], [0, 0, 0]])
        
    def test_getWinner(self):
        pass

def main():
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    unittest.TextTestRunner(verbosity=2).run(suite)
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
