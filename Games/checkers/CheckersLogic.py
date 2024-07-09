import numpy as np
import math

'''
Board class for the game of Checkers (Russian variant).

Board size is default 8x8.
Board data:
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[7][0] is the bottom left square,
Squares are stored and manipulated as (row, col) tuples.
'''

WHITE_NON_KING = 1
WHITE_KING = 3
BLACK_NON_KING = -1
BLACK_KING = -3
EMPTY = 0

DEFAULT_SIZE = 8


class Board:
    """
    Checkers Board.
    """
    __directions_kings = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    __directions_white = [(-1, -1), (-1, 1)]
    __directions_black = [(1, -1), (1, 1)]

    def __init__(self, n: int = None, pieces: np.array = None, last_long_capture: bool = None):
        """Set up initial board configuration."""
        self.n = n or DEFAULT_SIZE

        # capture position for piece of the player that is staying in turn (jumping over multiple enemy pieces)
        self.last_long_capture = last_long_capture or None

        if pieces is None:
            # Create the init board array.
            self.pieces = np.zeros([self.n, self.n], dtype=int)
            self.setup_pieces()
        else:
            self.pieces = pieces
            assert self.pieces.shape == (self.n, self.n)

    def setup_pieces(self):
        for row in range(self.n):
            for col in range(self.n):
                if (row + col) % 2 == 1:
                    if row < (self.n // 2) - 1:
                        self.pieces[row][col] = BLACK_NON_KING
                    if row > (self.n // 2 if self.n % 2 == 0 else self.n // 2 + 1):
                        self.pieces[row][col] = WHITE_NON_KING

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    def get_action_size(self):
        square_from = (self.n * self.n) / 2  # half of all fields are possible positions for pieces
        move_vector = (self.n - 1) * 4  # at max n-1 fields times 4 directions
        size = square_from * move_vector  # size is always an even integer (odd or even * even = even)
        assert size % 2 == 0 and size.is_integer()
        size = int(size)
        sqrt_rounded = math.ceil(math.sqrt(size))
        square = sqrt_rounded * sqrt_rounded
        padding = square - size  # calculating padding in order to rotate pi vector in getSymmetries later
        return size, padding

    def is_within_bounds(self, row: int, col: int):
        return 0 <= row < self.n and 0 <= col < self.n

    def get_moves_for_square(self, row: int, col: int, color: int, captures_only: bool = False):
        piece = self.pieces[row][col]
        assert piece != EMPTY, f"Square ({row}, {col}) is empty."
        moves = []

        directions = self.__directions_white if color == WHITE_NON_KING else self.__directions_black
        if abs(piece) == 3:  # King can move in all directions
            directions = self.__directions_kings
        for d_row, d_col in directions:
            nrow, ncol = row + d_row, col + d_col
            if not captures_only and self.is_within_bounds(nrow, ncol) and self.pieces[nrow][ncol] == EMPTY:
                moves.append((row, col, nrow, ncol))
            elif (self.is_within_bounds(nrow + d_row, ncol + d_col) and self.pieces[nrow][ncol] * piece < 0 and
                  self.pieces[nrow + d_row][ncol + d_col] == EMPTY):
                if not captures_only:
                    moves.clear()
                    captures_only = True
                moves.append((row, col, nrow + d_row, ncol + d_col))

        return moves

    def get_legal_moves(self, color: int):
        """
        Performs the given move on the board
        :param color: player that is executing the move
        """
        legal_moves = []

        if self.last_long_capture:
            start_row, start_col = self.last_long_capture
            legal_moves.append(self.get_moves_for_square(start_row, start_col, color, True))
        else:
            captures_only = False
            for row in range(self.n):
                for col in range(self.n):
                    if self.pieces[row][col] * color > 0:  # checking whether field is not empty and it is an own piece
                        new_moves = self.get_moves_for_square(row, col, color, captures_only)
                        now_capturing = False
                        for i in new_moves:
                            row, col, nrow, ncol = i
                            if abs(nrow - row) > 1 and abs(ncol - col) > 1:
                                now_capturing = True
                        if not captures_only and now_capturing:
                            captures_only = True
                            legal_moves.clear()
                            legal_moves.append(new_moves)
                        elif captures_only:
                            legal_moves.append(new_moves)
                        else:
                            legal_moves.append(new_moves)
        return legal_moves

    def flat_legal_moves(self, color):
        legal_moves = self.get_legal_moves(color)
        moves = [move for moves_per_piece in legal_moves for move in moves_per_piece]
        return moves

    def has_legal_moves(self, color: int):
        moves = self.flat_legal_moves(color)
        return bool(moves)

    def one_d_to_two_d(self, action: tuple[int, int]) -> tuple[int, int, int, int]:
        return action[0] // self.n, action[0] % self.n, action[1] // self.n, action[1] % self.n

    def execute_action(self, action: tuple[int, int], color: int):
        """
        Performs the given move on the board
        :param action: tuple (from_row, from_column, to_row, to_column)
        :param color: player that is executing the move
        """
        if type(action) is not tuple:
            raise ValueError(f"Invalid move: {action}")
        if len(action) != 2:
            raise ValueError(f"Invalid move: {action}")
        action = self.one_d_to_two_d(action)
        if action not in self.flat_legal_moves(color):
            raise ValueError(f"Invalid move: {action}")

        row, col, nrow, ncol = action
        if color == BLACK_NON_KING and nrow == self.n - 1:
            self.pieces[nrow][ncol] = BLACK_KING
        elif color == WHITE_NON_KING and nrow == 0:
            self.pieces[nrow][ncol] = WHITE_KING
        else:
            self.pieces[nrow][ncol] = self.pieces[row][col]
        self.pieces[row][col] = EMPTY
        # captures
        if abs(nrow - row) == 2:
            c_row, c_col = (row + nrow) // 2, (col + ncol) // 2
            self.pieces[c_row][c_col] = EMPTY

            # Check for additional captures
            additional_captures = self.get_moves_for_square(nrow, ncol, color, captures_only=True)
            if additional_captures:
                self.last_long_capture = (nrow, ncol)
            else:
                self.last_long_capture = None
        else:
            self.last_long_capture = None
