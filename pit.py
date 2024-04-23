import Arena
from MCTS import MCTS
from TicTacToe.TicTacToeGame import TicTacToeGame
from TicTacToe.TicTacToePlayers import RandomPlayer, HumanTicTacToePlayer
from Keras.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

g = TicTacToeGame()

# all player
human = HumanTicTacToePlayer(g).play


# nnet players
n1 = NNet(g)
#n1.load_checkpoint("./pretrained/", "best.pth.tar") // missing files.
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
aiPlayer = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

arena = Arena.Arena(aiPlayer, human, g, display=TicTacToeGame.display)

print(arena.playGames(2, verbose=True))
