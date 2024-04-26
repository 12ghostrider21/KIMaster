"""
Board class for the game of TicTacToe.
Default board size is 3x3.
Board data:
  1=white(O), -1=black(X), 0=empty
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[2][0] is the bottom left square,
Squares are stored and manipulated as (x,y) tuples.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the board for the game of Othello by Eric P. Nichols.

"""


# from bkcharts.attributes import color
class Board:
    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    def __init__(self, n=3):
        """Set up initial board configuration."""
        self.n = n
        self.pieces: list = [[0] * self.n] * self.n

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    def get_legal_moves(self) -> list[tuple[int, int]]:
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        """
        moves = set()  # stores the legal moves.

        # Get all the empty squares (color==0)
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 0:
                    new_move = (x, y)
                    moves.add(new_move)
        return list(moves)

    def has_legal_moves(self) -> bool:
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 0:
                    return True
        return False

    def is_win(self, color: int) -> bool:
        """Check whether the given player has collected a triplet in any direction; 
        @param color (1=white,-1=black) defines a player
        """
        win = self.n
        # check y-strips
        for y in range(self.n):
            count = 0
            for x in range(self.n):
                if self[x][y] == color:
                    count += 1
            if count == win:
                return True
        # check x-strips
        for x in range(self.n):
            count = 0
            for y in range(self.n):
                if self[x][y] == color:
                    count += 1
            if count == win:
                return True
        # check two diagonal strips
        count = 0
        for d in range(self.n):
            if self[d][d] == color:
                count += 1
        if count == win:
            return True
        count = 0
        for d in range(self.n):
            if self[d][self.n - d - 1] == color:
                count += 1
        if count == win:
            return True

        return False

    def execute_move(self, move: tuple[int, int], color: int) -> None:
        """Perform the given move on the board; 
        color gives the color pf the piece to play (1=white,-1=black)
        """

        (x, y) = move

        # Add the piece to the empty square.
        assert self[x][y] == 0
        self[x][y] = color
