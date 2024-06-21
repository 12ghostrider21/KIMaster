import numpy as np


class Board:
    def __init__(self, rows=4, pieces: np.array = None):
        """Set up initial board configuration."""
        assert rows > 1
        self.rows = rows
        self.pieces = pieces
        if pieces is None:
            n = 1
            self.pieces = np.zeros(rows)
            for i in range(rows):
                self.pieces[i] = n
                n += 2

    def get_valid_actions(self):
        """Returns all legal moves"""
        moves = []
        for row in range(self.rows):
            pieces = self.pieces[row]
            if pieces == 0:
                continue
            for i in range(1, (pieces + 1)):
                moves.append((row, i))
        return moves

    def has_valid_actions(self):
        valid_moves = self.get_valid_actions()
        if len(valid_moves) == 0:
            return False
        return True

    def is_game_over(self):
        """Checks whether the game is over"""
        return not self.has_valid_actions()

    def execute_action(self, action, player):
        """
        Performs the given move on the board
        :param action: tuple (row, pieces_to_remove)
        :param player: player that is executing the move
        """
        assert action in self.get_valid_actions()
        self.pieces[action[0]] -= action[1]
