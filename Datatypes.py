from enum import Enum
from pydantic import BaseModel

from Games.Connect4.Connect4Game import Connect4Game


class EGame(Enum):
    othello = 0
    tictactoe = 1
    connect4 = Connect4Game
    nim = 3
    checkers = 4
    go = 5
    waldmeister = 6


class RESPONSE(Enum):
    SUCCESS = 200
    ERROR = 400


class EGameMode(Enum):
    pp = "player_vs_player"
    pa = "player_vs_ai"
    paa = "playerai_vs_ai"
    papa = "playerai_vs_playerai"


class EDifficulty(Enum):
    easy = 0
    medium = 1
    hard = 2


class GameConfig(BaseModel):
    game: EGame
    mode: EGameMode
    difficulty: EDifficulty
