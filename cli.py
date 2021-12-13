class CLI:
    def __init__(self):
        pass

    def display_board(self, board):
        print(str(board))

    def display_outcome(self, winner=-1):
        if winner > 0:
            print('Player {winner} is the winner!'.format(winner=winner))
        else:
            print('Draw!')

    def display_move(self, x, y, player):
        print('Player {player_id} marks {x} {y}'.format(player_id=player.player_id,x=x,y=y))

    def get_human_player_move(self, board):
        move = [int(x) - 1 for x in input('Make your move: ').split()]
        while (board.is_point_marked(move)):
            print('Your choice of move is invalid.')
            move = [int(x) - 1 for x in input('Make your move: ').split()]
        return move
