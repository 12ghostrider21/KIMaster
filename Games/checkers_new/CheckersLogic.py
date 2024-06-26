import numpy as np

'''
Board class for the game of Checkers (Russian variant).

Board size is default 8x8.
Board data:
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[7][0] is the bottom left square,
Squares are stored and manipulated as (x,y) tuples.
'''

WHITE_MAN = -1
WHITE_KING = -3
BLACK_MAN = +1
BLACK_KING = +3
EMPTY = 0

DEFAULT_SIZE = 8


class Board():
    """
    Checkers Board.
    """
    __directions_kings = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    __directions_white = [(-1, -1), (-1, 1)]
    __directions_black = [(1, -1), (1, 1)]

    def __init__(self, n=None, pieces=None, last_long_capture=None):
        """Set up initial board configuration."""
        self.n = n or DEFAULT_SIZE
        self.last_long_capture = last_long_capture or None

        if pieces is None:
            # Create the empty board array.
            self.pieces = np.zeros([self.n, self.n], int)
        else:
            # Add board config.
            self.pieces = pieces
            assert self.pieces.shape == (self.n, self.n)
            self.setup_pieces()

    def setup_pieces(self):
        rows_for_pieces = self.n // 2 - 1
        for x in range(rows_for_pieces):
            for y in range(self.n):
                if (x + y) % 2 == 1:
                    self.pieces[x][y] = BLACK_MAN
                    self.pieces[self.n - 1 - x][y] = WHITE_MAN

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    def get_action_size(self):
        square_from = (self.n * self.n) // 2
        move_vector = (self.n - 1) * 4
        return square_from * move_vector

    def is_within_bounds(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.n

    def get_moves_for_square(self, x, y, captures_only=False):
        piece = self.pieces[x][y]
        assert piece != EMPTY, f"Square ({x}, {y}) is empty."
        moves = set()

        directions = self.__directions_white if piece == WHITE_MAN else self.__directions_black
        if abs(piece) == 3:  # King can move in all directions
            directions = self.__directions_kings

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_within_bounds(nx, ny) and self.pieces[nx][ny] == EMPTY and not captures_only:
                moves.add((x, y, nx, ny))
            elif self.is_within_bounds(nx + dx, ny + dy) and self.pieces[nx][ny] * piece < 0 and self.pieces[nx + dx][
                ny + dy] == EMPTY:
                if not captures_only:   # statt den zwei Zeilen darunter? => ansonsten wenn in beide Richtungen jmd
                    moves.clear()       # schlagen können, nur eine Richtung erfasst als Zug, oder?
                    captures_only = True

                moves.add((x, y, nx + dx, ny + dy))

        return moves

    def get_legal_moves(self, color):
        legal_moves = set()

        if self.last_long_capture:
            start_x, start_y = self.last_long_capture
            legal_moves.update(self.get_moves_for_square(start_x, start_y, True))
        else:
            captures_only = False
            for x in range(self.n):
                for y in range(self.n):
                    if self.pieces[x][y] * color > 0:
                        new_moves = self.get_moves_for_square(x, y, captures_only)
                        # if not captures_only and (abs(nx-x) == 2 and abs(ny-y) == 2 for x, y, nx, ny in new_moves): ??
                        if not captures_only and any(self.pieces[ny][nx] == EMPTY for _, _, nx, ny in new_moves): # Bedingung würde für
                            captures_only = True  # normalen Zug doch auch gelten, oder? ..nicht nur für Schlag-Move
                            legal_moves.clear()
                            legal_moves.update(new_moves)
                        elif captures_only:
                            legal_moves.update(new_moves)

        return list(legal_moves)

    def has_legal_moves(self, color):
        return bool(self.get_legal_moves(color))

    def execute_action(self, action, color):
        """
        Performs the given move on the board
        :param action: tuple (from_row, from_column, to_row, to_column)
        :param color: player that is executing the move
        """

        # Moving own man/king
        if action not in self.get_legal_moves(color):
            raise ValueError(f"Invalid move: {action}")
        x, y, nx, ny = action
        if color == BLACK_MAN and nx == self.n - 1:
            self.pieces[nx][ny] = BLACK_KING
        elif color == WHITE_MAN and nx == 0:
            self.pieces[nx][ny] = WHITE_KING
        else:
            self.pieces[nx][ny] = self.pieces[x][y]
        self.pieces[x][y] = EMPTY

        # captures
        if abs(nx - x) == 2:
            cx, cy = (x + nx) // 2, (y + ny) // 2
            self.pieces[cx][cy] = EMPTY

            # Check for additional captures
            additional_captures = self.get_moves_for_square(nx, ny, captures_only=True)
            if additional_captures:
                self.last_long_capture = (nx, ny)
            else:
                self.last_long_capture = None
        else:
            self.last_long_capture = None
