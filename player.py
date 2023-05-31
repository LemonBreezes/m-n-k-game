class Player:
    def __init__(self, player_id):
        self.p_id = player_id

    def get_move(self, board):
        move = [int(x) - 1 for x in input('Make your move: ').split()]
        while (board.is_point_marked(move)):
            print('Your choice of move is invalid.')
            move = [int(x) - 1 for x in input('Make your move: ').split()]
        return move
