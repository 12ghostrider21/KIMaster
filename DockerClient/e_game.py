from enum import Enum

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