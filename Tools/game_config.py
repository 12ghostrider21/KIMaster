from enum import Enum
from dataclasses import dataclass
from Tools.neural_net import NeuralNet


from Games.tictactoe.TicTacToeGame import TicTacToeGame
from Games.tictactoe.keras.NNet import NNetWrapper as TicTacToeNNet
from Games.othello.OthelloGame import OthelloGame
from Games.othello.pytorch.NNet import NNetWrapper as OthelloNNet
from Games.connect4.Connect4Game import Connect4Game
from Games.connect4.keras.NNet import NNetWrapper as Connect4NNet



# imports for ...
class EGame(Enum):
    tictactoe = (TicTacToeGame, TicTacToeNNet)
    othello = (OthelloGame, OthelloNNet)
    connect4 = (Connect4Game, Connect4NNet)
    # nim = "nim"
    # checkers = "checkers"
    # go = "go"
    # waldmeister = "waldmeister"


class EGameMode(Enum):
    player_vs_player = "player_vs_player"
    player_vs_ai = "player_vs_ai"
    playerai_vs_ai = "playerai_vs_ai"
    playerai_vs_playerai = "playerai_vs_playerai"


class EDifficulty(Enum):
    easy = 2
    medium = 10
    hard = 50


@dataclass
class GameConfig:
    game: list[EGame, NeuralNet] | Enum = None
    mode: EGameMode | Enum = None
    difficulty: EDifficulty | Enum = None

    def __call__(self) -> bool:
        if self.game is None:
            return False
        if self.mode is None:
            return False
        if self.difficulty is None:
            return False
        return True
