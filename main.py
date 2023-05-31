"""This is a Python Tic Tac Toe game"""

# imports
import sys
from itertools import product
from numpy import matrix
from time import sleep
from random import randrange
from math import inf
from copy import deepcopy

# constants
board_size = 3
num_players = 2
winning_row_length = 3
AI_difficulty = 2

# exception classes

# interface functions

# classes
class TicTacToeBoard(object):
    def __init__(self, size, num_players, winning_row_length, board=None, last_player=0):
        self._size = size
        self._num_players = num_players
        self._winning_row_length = winning_row_length
        self._last_player = last_player
        self._board = [[0 for i in range(size)] for j in range(size)] if board is None else board

    @classmethod
    def from_board(cls, class_instance):
        board = deepcopy(class_instance._board)
        size = class_instance._size
        num_players = class_instance._num_players
        winning_row_length = class_instance._winning_row_length
        return cls(size=size, num_players=num_players, winning_row_length=winning_row_length, board=board)

    def display(self):
        board = '|\n|'.join(['|'.join(map(str, row)) for row in self._board])
        board = '_' * (self._size * 2) + '_\n|' + board
        board = board + '|\n‾' + '‾' * (self._size * 2)
        print(board)

    def getLastPlayer(self):
        return self._last_player
        
    def getBoard(self):
        return self._board
    
    def getSize(self):
        return self._size

    def getWinningRowLength(self):
        return self._winning_row_length
    
    def getNumPlayers(self):
        return self._num_players

    def addMark(self, x, y, player):
        x = x - 1
        y = y - 1
        board = self._board
        board[x][y] = player
        self._last_player = player

    def isPointMarked(self,x,y):
        return not (self._isPointInBoard(x,y) and self._board[x][y] == 0)

    def hashPoint(self,x,y):
        return y + self._size*x

    def unhashPoint(self,p):
        return (p // self._size, p % self._size)

    def getWinner(self):
        for lines in self.getSetOfLines():
            if len(lines) >= self._winning_row_length:
                p = next(iter(lines))
                player = self._board[p[0]][p[1]]
                return player
        return 0

    def isDraw(self):
        if self.getWinner():
            return False
        for x, y in product(range(self._size), range(self._size)):
            if self._board[x][y] == 0:
                return False
        return True
    
    def getSetOfLines(self):
        setOfLines = []
        for player in range(1,self._num_players + 1):
            for x, y in product(range(self._size), range(self._size)):
                p = (x,y)
                q = self._getSecondPoint(x,y,player)
                # print('The second point is: ' + str(q))
                if q: setOfLines.insert(0, self._getAlignedPoints(p, q, player))
        return setOfLines

    def _getSecondPoint(self, x, y, player):
        if self._board[x][y] != player:
            return False
        for i, j in product(range(-1,2),range(-1,2)):
            if (i == 0 and j == 0):
                continue
            if (self._isPointInBoard(x+i,y+j) and self._board[x+i][y+j] == player):
                return (x+i,y+j)

    def _getAlignedPoints(self, p, q, player):
        aligned_points = {p, q}
        curr = q 
        while (self._isPointInBoard(curr[0] + q[0] - p[0],
                                    curr[1] + q[1] - p[1])
               and self._board[curr[0] + q[0] - p[0]][curr[1] + q[1] - p[1]] == player):
            aligned_points.add((curr[0] + q[0] - p[0], curr[1] + q[1] - p[1]))
            curr = (curr[0] + q[0] - p[0], curr[1] + q[1] - p[1])
        curr = p
        while (self._isPointInBoard(curr[0] - q[0] + p[0],
                                    curr[1] - q[1] + p[1])
               and self._board[curr[0] - q[0] + p[0]][curr[1] - q[1] + p[1]] == player):
            aligned_points.add((curr[0] - q[0] + p[0], curr[1] - q[1] + p[1]))
            curr = (curr[0] - q[0] + p[0], curr[1] - q[1] + p[1])
        # print('The aligned points are: ' + str(aligned_points))
        return frozenset(aligned_points)
            

    def _isPointInBoard(self, x, y):
        return (0 <= x < self._size and 0 <= y < self._size)

    def clear(self):
        self._board = [[0 for i in range(self.size)] for j in range(self.size)]

class TicTacToeAI(object):
    def __init__(self, board, player_id, difficulty):
        self._board = board
        self._difficulty = difficulty
        self._id = player_id
        pass

    def makeNextMove(self):
        if (self._difficulty == 1):
            self.makeRandomMove()
        else:
            self.makeOptimalMove()

    def makeRandomMove(self):
        while (True):
            x = randrange(self._board.getSize())
            y = randrange(self._board.getSize())
            if (self._board.getBoard()[x][y] == 0):
                self._board.addMark(x+1,y+1,self._id)
                break

    def _getPossibleNextStates(self, board, last_player):
        next_states = [None for i in range(board.getSize()**2)]
        for x,y in product(range(board.getSize()), range(board.getSize())):
            if board.getBoard()[x][y] == 0:
                temp = board.from_board(board)
                temp.addMark(x+1,y+1,max(last_player + 1 % (num_players + 1), 1))
                next_states[board.hashPoint(x,y)] = temp
                # print(str(temp.getBoard()) + ' ' + 'x: ' + str(x) + ', y: ' + str(y) + ', board.getBoard()[x][y]: ' + str(board.getBoard()[x][y]))
        return next_states
    
    def _getPossibleGameStates(self, board):
        # Assumes two players only currently
        winner = board.getWinner()
        if winner != 0:
            return winner
        if board.isDraw():
            return 0
        next_states = [None for i in range(board.getSize()**2)]
        for x,y in product(range(board.getSize()), range(board.getSize())):
            if board.getBoard()[x][y] == 0:
                temp = board.from_board(board)
                temp.addMark(x+1,y+1,max(board.getLastPlayer() + 1 % (num_players + 1), 1))
                next_states[board.hashPoint(x,y)] = self._getPossibleGameStates(temp, board.getLastPlayer())
                # print(str(temp.getBoard()) + ' ' + 'x: ' + str(x) + ', y: ' + str(y) + ', board.getBoard()[x][y]: ' + str(board.getBoard()[x][y]))
        return next_states

    # This scoring function really doesn't work well right now.
    def _scoreState(self, board):
        if not board:
            return -inf
        next_possible_states = self._getPossibleNextStates(board, board.getLastPlayer())
        next_possible_winners = [state.getWinner() for state in next_possible_states if state]
        # print(str(nextPossibleWinners))
        if any([winner == self._id for winner in next_possible_winners]):
            return inf
        if (any([winner != self._id and winner > 0 for winner in next_possible_winners])):
            return -inf
        return 0

    def makeOptimalMove(self):
        board = self._board
        possible_next_states = self._getPossibleNextStates(board, board.getLastPlayer())
        # print(str([state.getBoard() for state in possibleNextStates if state]))
        next_state_scores = [self._scoreState(state) for state in possible_next_states]
        best_move = board.unhashPoint(max(range(len(next_state_scores)),
                                         key=next_state_scores.__getitem__))
        # print(str(next_state_scores))
        # print('AI ' + str(self._id) + ' marks ' + str(best_move))
        board.addMark(best_move[0] + 1,best_move[1] + 1,self._id)

class TicTacToeGame(object):
    def __init__(self, size, num_players, winning_row_length):
        self._board = TicTacToeBoard(size=size,
                                     num_players=num_players,
                                     winning_row_length=winning_row_length)

    def start(self):
        board = self._board
        AI = TicTacToeAI(board=board, player_id=2, difficulty=AI_difficulty)
        board.display()
        while True:
            move = [ int(x) for x in input('Make your move: ').split()]
            if (board.isPointMarked(move[0]-1,move[1]-1)):
                print('Your choice of move is invalid.')
                continue
            board.addMark(x=move[0],y=move[1],player=1)
            board.display()
            if (board.getWinner() == 1):
                print('You win!')
                break
            if (board.isDraw()):
                print('Draw!')
                break
            sleep(1)
            AI.makeNextMove()
            board.display()
            if (board.getWinner() > 1):
                print('You lost!')
                break
            if (board.isDraw()):
                print('Draw!')
                break

# internal functions & classes
def main():
    game = TicTacToeGame(board_size, num_players, winning_row_length)
    game.start()
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
