from arena import Arena
from Tools.mcts import MCTS
from Games.go.GoGame import GoGame as Game
from Games.go.pytorch.NNet import NNetWrapper as NNet


import numpy as np
from Tools.utils import *


human_vs_cpu = True


g = Game()

# nnet players
n1 = NNet(g)
n1.load_checkpoint('./temp/','best1.pth.tar')

args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x, y: np.argmax(mcts1.get_action_prob(x, y, temp=1))


n2 = NNet(g)
n2.load_checkpoint('./temp/','best2.pth.tar')
args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
mcts2 = MCTS(g, n2, args2)
n2p = lambda x, y: np.argmax(mcts2.get_action_prob(x, y, temp=1))


arena = Arena(n1p, n2p, g)

print(arena.playGames(2, verbose=False))
