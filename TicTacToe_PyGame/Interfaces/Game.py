from abc import ABC, abstractmethod

import numpy as np


class Game(ABC):
    """
    This class specifies the base TicTacToe_PyGame class. To define your own game, subclass
    this class and implement the functions below. This works when the game is
    two-player, adversarial and turn-based.

    Use 1 for player1 and -1 for player2.

    See othello/OthelloGame.py for an example implementation.
    """
    def __init__(self):
        pass

    @abstractmethod
    def getInitBoard(self) -> np.array:
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        pass

    @abstractmethod
    def getBoardSize(self) -> tuple[int, int]:
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        pass

    @abstractmethod
    def getActionSize(self) -> int:
        """
        Returns:
            actionSize: number of all possible actions
        """
        pass

    @abstractmethod
    def getNextState(self, board: np.array, player: int, action) -> tuple[np.array, int]:
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        pass

    @abstractmethod
    def getValidMoves(self, board: np.array, player: int) -> np.array:
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        pass

    @abstractmethod
    def getGameEnded(self, board: np.array, player: int) -> int:
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        pass

    @abstractmethod
    def getCanonicalForm(self, board: np.array, player: int) -> int:
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        pass

    @abstractmethod
    def getSymmetries(self, board: np.array, pi) -> list:
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        pass

    @abstractmethod
    def stringRepresentation(self, board: np.array) -> str:
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        pass