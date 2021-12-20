DRAW = -1
PLAYER_ONE = 0
PLAYER_TWO = 1
BLANK_TILE = 2
TILES = {PLAYER_ONE: "X", PLAYER_TWO: "O", BLANK_TILE: " "}


class CLI:
    def __init__(self, num_rows, num_columns):
        self.num_rows = num_rows
        self.num_columns = num_columns

    def display_board(self, board):
        board = "|\n|".join(["|".join(map(self.tile_to_string, row)) for row in board])
        board = "_" * (2 * self.num_columns) + "_\n|" + board
        board = board + "|\n‾" + "‾" * (2 * self.num_columns)
        print(board)

    def display_outcome(self, winner=DRAW):
        if winner != DRAW:
            print("Player {winner} has won!".format(winner=TILES[winner]))
        else:
            print("Draw!")

    def display_move(self, x, y, player):
        print(f"Player {player} marks {x} {y}")

    def is_move_invalid(self, x, y, board):
        return (
            x < 0
            or y < 0
            or x >= self.num_columns
            or y >= self.num_columns
            or board[x][y] != BLANK_TILE
        )

    def get_human_player_move(self, board):
        x, y = (int(x) - 1 for x in input("Make your move: ").split())
        while self.is_move_invalid(x, y, board):
            print("Your choice of move is invalid.")
            x, y = [int(x) - 1 for x in input("Make your move: ").split()]
        return x, y

    def tile_to_string(self, tile):
        return TILES[tile]

    def display_progress(self, progress, total):
        loading = '.' * total
        print('\r%s Scored %3d percent of all possible moves!' % (loading, progress*100/total), end='')
        loading = loading[:progress] + '#' + loading[progress+1:]
        if progress == total:
            print()
