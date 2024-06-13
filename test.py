import json

import numpy as np

from Games.connect4.Connect4Game import Connect4Game
from Games.connect4.keras.NNet import NNetWrapper
from Tools.mcts import MCTS
from Tools.utils import dotdict

folder = r"C:\Users\alex\OneDrive\02_DEV\01_Python\SWTP\REWORK\Games\connect4\keras"
file = "best.h5"


def init_nn(game, nnet, folder: str, file: str):
    nn = nnet(game)
    nn.load_checkpoint(folder, file)
    args = dotdict({'numMCTSSims': 5, 'cpuct': 1.0})
    mcts = MCTS(game, nn, args)
    return mcts


game = Connect4Game()
mcts = init_nn(game, NNetWrapper, folder, file)
func = lambda x: mcts.getActionProb(x, temp=0)

players = [func, None, func]
it = 0
cur_player = 1
board = game.getInitBoard()
while game.getGameEnded(board, cur_player) == 0:  # 0 if game is not finished

    p = players[cur_player + 1]
    canonical_board = game.getCanonicalForm(board, cur_player)
    valids = game.getValidMoves(canonical_board, 1)

    payload = {"board": board.tolist(),
               "cur_player": cur_player,
               "dtype": str(board.dtype),
               "shape": board.shape}
    j_board = json.dumps(payload)
    payload = json.loads(j_board)
    board = np.array(payload["board"], dtype=payload["dtype"]).reshape(payload["shape"])

    action = np.argmax(func(game.getCanonicalForm(board, cur_player)))
    print(action)

    board, cur_player = game.getNextState(board, cur_player, action)
    print(board)
    it += 1
print(cur_player, board, it)
