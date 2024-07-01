
# IGame Interface Documentation

## Overview

The `IGame` interface defines the essential methods for implementing various types of games. This interface provides a standardized way to interact with game states, making it suitable for integrating with neural network models and Monte Carlo Tree Search (MCTS) algorithms.

## Methods

### getInitBoard

```python
@abstractmethod
def getInitBoard(self) -> np.array:
```

**Description:**
Returns the initial representation of the game board as a NumPy array.

**Returns:**
- `startBoard (numpy.array)`: A representation of the initial game board, suitable for input to a neural network.

### getBoardSize

```python
@abstractmethod
def getBoardSize(self) -> int | tuple[int, int]:
```

**Description:**
Returns the dimensions of the game board.

**Returns:**
- `x (int)`: The one-dimensional size of the game board.
- `(x, y) (tuple[int, int])`: A tuple representing the dimensions of the game board (number of rows and columns).

### getActionSize

```python
@abstractmethod
def getActionSize(self) -> int:
```

**Description:**
Returns the total number of possible actions in the game.

**Returns:**
- `actionSize (int)`: The number of all possible actions available in the game.

### getNextState

```python
@abstractmethod
def getNextState(self, board: np.array, player: int, action: any) -> tuple[np.array, int]:
```

**Description:**
Generates the next game state after applying the specified action for the current player.

**Parameters:**
- `board (numpy.array)`: The current game board.
- `player (int)`: The current player (1 for one player, -1 for the other player).
- `action (any)`: The action taken by the current player.

**Returns:
- `nextBoard (numpy.array)`: The game board after applying the specified action.
- `nextPlayer (int)`: The player who plays in the next turn.

### getValidMoves

```python
@abstractmethod
def getValidMoves(self, board: np.array, player: int) -> np.array:
```

**Description:**
Determines the valid moves for the current player on the given board in binary form.

**Parameters:**
- `board (numpy.array)`: The current game board.
- `player (int)`: The current player.

**Returns:**
- `validMoves (numpy.array)`: A binary vector indicating valid moves.

### getGameEnded

```python
@abstractmethod
def getGameEnded(self, board: np.array, player: int) -> int | float:
```

**Description:**
Determines the outcome of the game for the given player on the current board state.

**Parameters:**
- `board (numpy.array)`: The current game board.
- `player (int)`: The current player.

**Returns:**
- `result (int)`: The game outcome for the specified player (0: ongoing, 1: win, -1: loss, small non-zero value: draw).

### getCanonicalForm

```python
@abstractmethod
def getCanonicalForm(self, board: np.array, player: int) -> np.array:
```

**Description:**
Returns the canonical form of the board that is independent of the current player.

**Parameters:**
- `board (numpy.array)`: The current game board.
- `player (int)`: The current player.

**Returns:**
- `canonicalBoard (numpy.array)`: The canonical form of the board.

### getSymmetries

```python
@abstractmethod
def getSymmetries(self, board: np.array, pi: np.array) -> list:
```

**Description:**
Generates symmetrical forms of the given board and corresponding policy vector.

**Parameters:**
- `board (numpy.array)`: The current game board.
- `pi (numpy.array)`: The policy vector providing action probabilities.

**Returns:**
- `symmForms (list)`: A list of tuples (board, pi) representing symmetrical forms of the board and the policy vector.

### translate

```python
@abstractmethod
def translate(self, board: np.array, player: int, index: int) -> any:
```

**Description:**
Converts an index into an action.

**Parameters:**
- `index (int)`: The index of the move to translate.
- `board (np.array)`: The current game board.
- `player (int)`: The current player.

**Returns:**
- `action (any)`: The action fitting to the index.

### stringRepresentation

```python
@abstractmethod
def stringRepresentation(self, board: np.array) -> str:
```

**Description:**
Converts the current game board into a string format required for hashing, used by Monte Carlo Tree Search (MCTS).

**Parameters:**
- `board (numpy.array)`: The current game board.

**Returns:**
- `boardString (str)`: A string representation of the board suitable for hashing in MCTS.

### drawTerminal

```python
@abstractmethod
def drawTerminal(self, board: np.array, valid_moves: bool, cur_player: int) -> str:
```

**Description:**
Displays a terminal representation of the game board for debugging purposes.

**Parameters:**
- `board (numpy.array)`: The game board.
- `valid_moves (bool)`: Whether to display valid moves.
- `cur_player (int)`: The current player.

**Returns:**
- `str`: The terminal representation of the board.

### draw

```python
@abstractmethod
def draw(self, board: np.array, valid_moves: bool, cur_player: int):
```

**Description:**
Draws the game representation onto a Pygame surface.

**Parameters:**
- `board (np.array)`: The current game board.
- `valid_moves (bool)`: Whether to display valid moves.
- `cur_player (int)`: The current player.

**Returns:**
- `pygame.Surface`: The Pygame surface representing the game state.

**Notes:**
- Handles invalid `from_pos` for displaying valid moves (None/invalid pos). If invalid, raises a `ValueError`.
- Initializes the Pygame library and handles graphical operations for rendering the game state.
