from enum import Enum
from dataclasses import dataclass
from Tools.neural_net import NeuralNet

# imports for Connect4
from Games.Connect4.Connect4Game import Connect4Game
from Games.Connect4.keras.NNet import NNetWrapper as Connect4NNet


# imports for ...
class EGame(Enum):
    connect4 = (Connect4Game, Connect4NNet)
    # othello = "othello"
    # tictactoe = "tictactoe"
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
    game: list[EGame, NeuralNet] | Enum
    mode: EGameMode | Enum
    difficulty: EDifficulty | Enum

    def __call__(self) -> bool:
        if self.game is None:
            return False
        if self.mode is None:
            return False
        if self.difficulty is None:
            return False
        return True
