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


class EGame(Enum):
    # othello = OthelloGame()
    # tictactoe = TicTacToeGame()
    connect4 = Connect4Game()
    # nim = NimGame()
    # checkers = CheckersGame()
    # go = GoGame()
    # waldmeister = WaldmeisterGame()


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
