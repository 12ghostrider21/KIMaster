from enum import Enum
from pydantic import BaseModel
from DockerClient.e_game import EGame


class RESPONSE(Enum):
    SUCCESS = 200
    ERROR = 400


class EGameMode(Enum):
    player_vs_player = "player_vs_player"
    player_vs_ai = "player_vs_ai"
    playerai_vs_ai = "playerai_vs_ai"
    playerai_vs_playerai = "playerai_vs_playerai"


class EDifficulty(Enum):
    easy = 2
    medium = 10
    hard = 50


class GameConfig(BaseModel):
    game: EGame
    mode: EGameMode
    difficulty: EDifficulty
