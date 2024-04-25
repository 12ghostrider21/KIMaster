from abc import ABC, abstractmethod
import numpy as np


class IPlayer(ABC):

    @abstractmethod
    def play(self, board: np.array) -> int:
        """
        Method representing a player's move in the game.

        Parameters:
            board (numpy.array): The current game board represented as a numpy array.

        Returns:
            action (int): The selected action to be played by the player.
        """
        pass
