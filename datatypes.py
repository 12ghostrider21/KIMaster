from enum import Enum
from pydantic import BaseModel

from Games.Connect4.Connect4Game import Connect4Game

"""
from Games.Othello.OthelloGame import OthelloGame
from Games.TicTacToe.TicTacToeGame import TicTacToeGame
from Games.Nim.NimGame import NimGame
from Games.Checkers.CheckersGame import CheckersGame
from Games.Go.GoGame import GoGame
from Games.Waldmeister.WaldmeisterGame import WaldmeisterGame
"""


class RESPONSE(Enum):
    SUCCESS = 200
    ERROR = 400


class EGame(Enum):
    # othello = "othello"
    # tictactoe = "tictactoe"
    connect4 = "connect4"
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
    easy = "easy"
    medium = "medium"
    hard = "hard"


class GameConfig(BaseModel):
    game: EGame
    mode: EGameMode
    difficulty: EDifficulty
