import numpy as np


class Board:
    def __init__(self, rows=4, pieces: np.array = None):
        """Set up initial board configuration."""
        assert rows > 1
        self.rows = rows
        self.pieces = pieces
        if self.pieces is None:
            n = 1
            self.pieces = np.zeros(rows, dtype=int)
            for i in range(rows):
                self.pieces[i] = n
                n += 2

    def get_legal_moves(self,):
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
        valid_moves = self.get_legal_moves()
        if len(valid_moves) == 0:
            return False
        return True

    def is_game_over(self):
        """Checks whether the game is over"""
        return not self.has_valid_actions()

    def execute_action(self, action):
        """
        Performs the given move on the board
        :param action: tuple (row, pieces_to_remove)
        """
        if action not in self.get_legal_moves():
            raise ValueError(f'Invalid action: {action}')
        self.pieces[action[0]] -= action[1]
