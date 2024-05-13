from enum import Enum
from dataclasses import dataclass
from GameClient.neural_net import NeuralNet

from Games.Connect4.Connect4Game import Connect4Game
from Games.Connect4.keras.NNet import NNetWrapper as Connect4NNet


class EResponse(Enum):
    SUCCESS = 200
    ERROR = 400


@dataclass
class Response:
    response_code: EResponse
    response_msg: str
    data: dict | None

    def __init__(self, response_code: EResponse, response_msg: str, data: dict | None = None):
        self.response_code = response_code
        self.response_msg = response_msg
        self.data = data


class EGame(Enum):
    # othello = "othello"
    # tictactoe = "tictactoe"
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
    game: list[EGame, NeuralNet] | Enum
    mode: EGameMode | Enum
    difficulty: EDifficulty | Enum

    def __call__(self) -> bool:
        for x in self.__dict__:
            if x is None:
                return False
        return True
