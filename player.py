class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    def get_move(self, board, ui):
        return ui.get_human_player_move(board)
