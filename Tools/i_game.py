from abc import ABC, abstractmethod
import numpy as np


class IGame(ABC):

    @abstractmethod
    def getInitBoard(self) -> np.array:
        """
        Get the initial representation of the game board.
        As well resets all other data to initial state!

        Returns:
            startBoard (numpy.array): A representation of the initial game board.
                                      This representation is suitable for input to a neural network.

        This method returns a numpy array `startBoard` representing the initial state or
        configuration of the game board. The `startBoard` is intended to be a suitable input
        format for feeding into a neural network model for game evaluation or decision-making.

        Example:
            If implemented for a game like tic-tac-toe, `getInitBoard` might return a numpy array
            representing an empty 3x3 game board.

        Note:
            The `startBoard` should provide an accurate and meaningful representation of the
            initial state of the game board, which serves as the starting point for gameplay.
        """
        pass

    @abstractmethod
    def getBoardSize(self) -> int | tuple[int, int]:
        """
        Get the dimensions of the game board.

        Returns:
            x (int): the one-dimensional size of the game board.
            (x, y) (tuple[int, int]): A tuple representing the dimensions of the game board.
                                       - `x` (int): The number of rows in the board.
                                       - `y` (int): The number of columns in the board.

        This method returns a tuple `(x, y)` representing the dimensions (number of rows and columns)
        of the game board. The values `x` and `y` indicate the size or shape of the board grid.

        Example:
            If implemented for a game like tic-tac-toe, `getBoardSize` might return `(3, 3)`,
            representing a 3x3 grid for the game board.

        Note:
            The tuple `(x, y)` should accurately reflect the dimensions of the game board,
            providing information about its structure and layout.
        """
        pass

    @abstractmethod
    def getActionSize(self) -> int:
        """
        Get the total number of possible actions in the game.

        Returns:
            actionSize (int): The number of all possible actions available in the game.

        This method returns the total number of possible actions that can be taken by players
        in the game. The value `actionSize` represents the size of the action space, which
        defines the set of all valid actions that players can choose from during gameplay.

        Example:
            If implemented for a game like tic-tac-toe, `getActionSize` might return 9,
            representing the number of cells on the game board where a player can make a move.
        """
        pass

    @abstractmethod
    def getNextState(self, board: np.array, player: int, action: any) -> tuple[np.array, int]:
        """
        Generate the next game state after applying the specified action for the current player.

        Parameters:
            board (numpy.array): The current game board represented as a numpy array.
            player (int): The current player (1 for one player, -1 for the other player).
            action (any): The action taken by the current player on the board. Can be an int,
                        a tuple or anything else that represents an action for the chosen game.

        Returns:
            nextBoard (numpy.array): The game board after applying the specified action.
            nextPlayer (int): The player who plays in the next turn (should be `-player`).

        This method computes the next game state (`nextBoard`) after the specified `action`
        is applied by the `player` on the current `board`. It also determines the next player
        (`nextPlayer`) who will play in the subsequent turn.

        The `nextPlayer` is calculated as `-player`, which effectively alternates between players
        in each turn.
        """
        pass

    @abstractmethod
    def getValidMoves(self, board: np.array, player: int) -> np.array:
        """
        Determine the valid moves for the current player on the given board in binary form.

        Parameters:
            board (numpy.array): The current game board represented as a numpy array.
            player (int): The current player (1 for one player, -1 for the other player).

        Returns:
            validMoves (numpy.array): A binary vector indicating valid moves.
                                       - `1` for valid moves.
                                       - `0` for invalid moves.

        This method generates a binary vector `validMoves` indicating which moves are valid
        for the specified `player` on the current `board`. Each element of `validMoves`
        corresponds to a possible action or move in the game.

        The value `1` in `validMoves[i]` indicates that the move corresponding to index `i`
        is valid for the `player` on the given `board`, while `0` indicates that the move
        is invalid or not allowed.
        """
        pass

    @abstractmethod
    def getGameEnded(self, board: np.array, player: int) -> int | float:
        """
        Determine the outcome of the game for the given player on the current board state.

        Parameters:
            board (numpy.array): The current game board represented as a numpy array.
            player (int): The current player (1 for one player, -1 for the other player).

        Returns:
            result (int): An integer representing the game outcome for the specified player.
                          - `0` if the game has not ended.
                          - `1` if the `player` has won.
                          - `-1` if the `player` has lost.
                          - A small non-zero value (e.g., `0.1`) indicating a draw or game tie.

        This method evaluates the current game state on the given `board` and determines the outcome
        for the specified `player`. The `player` parameter indicates which player's perspective to consider
        when determining the game outcome.
        """
        pass

    @abstractmethod
    def getSymmetries(self, board: np.array, pi: np.array) -> list:
        """
        Generate symmetrical forms of the given board and corresponding policy vector.

        Parameters:
            board (numpy.array): The current game board represented as a numpy array.
            pi (numpy.array): The policy vector of size `self.getActionSize()`, providing action probabilities.

        Returns:
            symmForms (list): A list of tuples (board, pi) where each tuple represents a symmetrical
                              form of the board and the corresponding policy vector `pi`.

        This method generates symmetrical transformations of the given board along with the associated
        policy vector `pi`. The purpose is to create additional training data for the neural network by
        considering different orientations or reflections of the board, which helps in enhancing the
        model's ability to generalize across different board configurations.
        """
        pass

    @abstractmethod
    def translate(self, board: np.array, player: int, index: int) -> any:
        """
        Converts an index coming from alpha zero AI into an action.
        Comes into effect for games that do not just have a to_position (just an int as move).
        The output depends on the game getting implemented, most likely it's a pair tuple (from_position, to_position),
        but it can also be a triplet tuple and so on - depending on the game.
        Alpha-zero AI generates just an index that needs to get converted back into the original move by comparison
        with the valid_moves method from the logic.

        Parameters:
            index (int): The index of the move to translate.
            board (np.array): The current game board represented as a numpy array.
            player (int): The current player (1 for one player, -1 for the other player).

        Returns:
            action (any): The action fitting to the index.
        """

    def rotateMove(self, move: int | tuple[int, int]) -> int | tuple[int, int]:
        """
        For games like chess, checkers ...
        Stands in relation with displaying rotated board frontend-wise.
        Every player moves from bottom to top (black AND white).
        So the moves coming from frontend need to be rotated as well for one of the two players.

        Parameters:
            move (int | tuple[int, int]): The move to rotate.

        Returns:
            rotated move by 180 degree (int | tuple[int, int])
        """

    @abstractmethod
    def stringRepresentation(self, board: np.array) -> str:
        """
        Convert the current game board into a string format required for hashing, used by Monte Carlo Tree Search (MCTS).

        Parameters:
            board (numpy.array): The current game board represented as a numpy array.

        Returns:
            boardString (str): A string representation of the board suitable for hashing in MCTS.

        This method is used to convert the current game board into a string format that can be used as a unique identifier
        for the board state within the context of Monte Carlo Tree Search (MCTS). The resulting string representation is
        used for efficient state hashing and lookup during the MCTS simulation.
        """
        pass

    @abstractmethod
    def drawTerminal(self, board: np.array, valid_moves: bool, cur_player: int, *args: any) -> str:
        """
        Displays a terminal representation of the game board for debugging purposes.

        Parameters:
            board (numpy.array): The game board represented as a numpy array.
            valid_moves: Whether displaying / drawing valid moves or not.
            cur_player: The current player (1 for one player, -1 for the other player).
            args: first arg is from_pos (int): The from_pos to get the valid moves for.
                    That argument is only for games where to move tokens.
                    For Games in which to just one-time set tokens, this arg is redundant
                    and need to get no further attention.
                    Wrong indices need to raise a ValueError.

        Notes:
            -Needs to handle invalid from_pos for displaying valid moves (None / invalid pos). If invalid
            throw a ValueError.


        Returns:
            str: The terminal representation of the board.

        This method is intended to visually display the current state of the game board
        in a terminal/console environment.
        """
        pass

    @abstractmethod
    def draw(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        """
        Draw the game representation onto a Pygame surface.

        This method is responsible for rendering the current game state represented by `board`
        onto a Pygame surface. This surface will be returned in bytes format, twice.
        One representation for player1, the other one mirrored for player2.

        Parameters:
            board (np.array): A NumPy array representing the game state. The array should contain
                the necessary information to visualize the current state of the game.
            valid_moves: Whether displaying / drawing valid moves or not.
            cur_player: The player who is in turn (1 for one player, -1 for the other player).
            args: first arg is from_pos (int): The from_pos to get the valid moves for.
                    That argument is only for games where to move tokens.
                    For Games in which to just one-time set tokens, this arg is redundant
                    and need to get no further attention.
                    Wrong indices need to raise a ValueError.

        Returns:
            pygame.Surface

        Notes:
        - The `board` parameter should be a NumPy array representing the game state in a structured
          format suitable for visualization. The specific structure and meaning of the array's
          contents are defined by the concrete implementations of `Drawable`.

        - Needs to handle invalid from_pos for displaying valid moves (None / invalid pos). If invalid
          throw a ValueError.

        - The method should handle the rendering of the game state based on the provided `board`
          data and any additional optional arguments (`args`). The resulting surface should
          visually represent the game's current state.

        - Implementations of this method should ensure that the returned surface is ready for
          display within a Pygame environment, such as by initializing the Pygame library and
          handling any necessary graphical operations.

        Example Usage:
            # Example implementation for drawing a game state
            surface = pygame.Surface((800, 600))  # Create a Pygame surface
            surface.fill((255, 255, 255))         # Fill with white background

            # Render game state onto the surface based on `board` data
            # Example: Draw a grid based on the `board` content
            cell_size = 50
            for i in range(board.shape[0]):
                for j in range(board.shape[1]):
                    if board[i, j] == 1:
                        pygame.draw.rect(surface, (0, 0, 0), (j * cell_size, i * cell_size, cell_size, cell_size))

            return surface
        """
        pass

