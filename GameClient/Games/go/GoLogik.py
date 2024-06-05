from collections import namedtuple
import numpy as np

DEFAULT_SIZE = 19  # Standardgröße des Go-Bretts

WinState = namedtuple('WinState', 'is_ended winner')

class Board:
    """
    Go Board.
    """

    def __init__(self, size=None, np_pieces=None):
        "Set up initial board configuration."
        self.size = size or DEFAULT_SIZE

        if np_pieces is None:
            self.np_pieces = np.zeros([self.size, self.size], int)
        else:
            self.np_pieces = np_pieces
            assert self.np_pieces.shape == (self.size, self.size)