"""This is a Python Tic Tac Toe game"""

# imports
import sys
from itertools import product
from numpy import matrix

# constants
board_size = 3
num_players = 1
winning_row_length = 3

# exception classes

# interface functions

# classes
class TicTacToeBoard(object):
    def __init__(self, size, num_players, winning_row_length):
        self._size = size
        self._num_players = num_players
        self._winning_row_length = winning_row_length
        self._board = [[0 for i in range(size)] for j in range(size)]
        self._adjacency_matrices = [matrix([[0 for p in range(size**2)]
                                            for q in range(size**2)])
                                    for player in range(self._num_players)]

    def display(self):
        board = '|\n|'.join(['|'.join(map(str, row)) for row in self._board])
        board = '_' * (self._size * 2) + '_\n|' + board
        board = board + '|\n‾' + '‾' * (self._size * 2)
        print(board)

    def _hashCoordinate(self, x, y):
        return x + y*self._size

    def addMark(self, x, y, player):
        x = x - 1
        y = y - 1
        board = self._board
        board[x][y] = player
        for i, j in product(range(-1,2),range(-1,2)):
            if (i == 0 and j == 0):
                continue
            p = self._hashCoordinate(x, y)
            q = self._hashCoordinate(x+i,y+j)
            r = self._hashCoordinate(x-i,y-j)
            # print('player,x,y,i,j,p,q,r are: ' + str(player) + ' '
            #       + str(x) + ' ' + str(y) + ' ' + str(i) + ' ' + str(j) + ' '
            #       + str(p) + ' ' + str(q) + ' ' + str(r))
            if (0 <= x+i < self._size and 0 <= y+j < self._size and board[x+i][y+j] == player):
                if (0 <= x-i < self._size and 0 <= y-j < self._size
                    and board[x-i][y-j] == player):
                    self._adjacency_matrices[player-1][q,p] = 1
                else:
                    self._adjacency_matrices[player-1][p,q] = 1

    def getWinner(self):
        for player in range(self._num_players):
            m = self._adjacency_matrices[player]**(self._winning_row_length - 1)
            # print(m)
            for i, j in product(range(self._size**2), range(self._size**2)):
                if (m[i,j] == 1 and abs(j - i) in {self._winning_row_length**2 - 1,
                                           self._winning_row_length - 1,
                                           self._winning_row_length**2 - self._winning_row_length}):
                    return player + 1

    def clear(self):
        self._board = [[0 for i in range(self.size)] for j in range(self.size)]
        self._adjacency_matrices = [matrix([[0 for p in range(self.size**2)]
                                            for q in range(self.size**2)])
                                    for player in range(self._num_players)]

class TicTacToeGame(object):
    def __init__(self, size, num_players, winning_row_length):
        self.board = TicTacToeBoard(size, num_players, winning_row_length)

    def start(self):
        board = self.board
        board.display()
        while True:
            move = [ int(x) for x in input('Make your move: ').split()]
            board.addMark(x=move[0],y=move[1],player=1)
            board.display()
            if (board.getWinner() == 1):
                print('You win!')
                break

# internal functions & classes
def main():
    game = TicTacToeGame(board_size, num_players, winning_row_length)
    game.start()
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
