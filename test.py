import json

import numpy as np

from Tools.Game_Config.difficulty import EDifficulty
from Tools.dynamic_imports import Importer
from Tools.i_game import IGame

from Tools.mcts import MCTS
from Tools.trained_folder_dataclass import TrainedFolder
from Tools.utils import *

#i = Importer("./Games")

#game = i.get_games()["connect4"]
#func = i.get_ai_func().get(("connect4", EDifficulty.hard))

from Games.othello.OthelloGame import OthelloGame as game
from Games.othello.pytorch.NNet import NNetWrapper as nnet


def __init_nn(game: IGame, nnet, trained_folder: TrainedFolder, difficulty: EDifficulty):
    nn = nnet(game)
    nn.load_checkpoint(trained_folder.folder, trained_folder.file)
    mcts = MCTS(game, nn, dotdict({
        'numMCTSSims': difficulty.value,
        'fpu': 0.,
        'universes': 1,
        'cpuct': 1,
        'prob_fullMCTS': 1.,
        'forced_playouts': False,
        'no_mem_optim': False,
    }))
    return mcts

game = game()

mcts = __init_nn(game, nnet, TrainedFolder("./Games/othello/pytorch", "6x100x25_best.pth.tar"), EDifficulty.easy)


# arena
#players = [func, None, func]
it = 0
cur_player = 1
board = game.getInitBoard()

while game.getGameEnded(board, cur_player) == 0:  # 0 if game is not finished

    #p = players[cur_player + 1]
    canonical_board = game.getCanonicalForm(board, cur_player)
    valids = game.getValidMoves(canonical_board, cur_player)

    payload = {"board": board.tolist(),
               "cur_player": cur_player,
               "dtype": str(board.dtype),
               "shape": board.shape}
    j_board = json.dumps(payload)
    payload = json.loads(j_board)
    board = np.array(payload["board"], dtype=payload["dtype"]).reshape(payload["shape"])
    func = lambda x, n: np.argmax(mcts.getActionProb(x, temp=(0.5 if n <= 6 else 0.)))
    print(board.shape, func)
    action = func(game.getCanonicalForm(board, cur_player), it)
    print(action, len(valids), valids)

    converted_action = game.translate(board, cur_player, action)
    board, cur_player = game.getNextState(board, cur_player, converted_action)
    print(board)
    it += 1
print(cur_player, board, it)
