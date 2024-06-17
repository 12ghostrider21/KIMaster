import json

import numpy as np

from Tools.Game_Config.difficulty import EDifficulty
from Tools.mcts import MCTS
from Tools.utils import dotdict

from Tools.dynamic_imports import Importer

i = Importer("./Games")
game = i.get_games()["connect4"]
func = i.get_ai_func().get(("connect4", EDifficulty.easy))

# arena
players = [func, None, func]
it = 0
cur_player = 1
board = game.getInitBoard()
while game.getGameEnded(board, cur_player) == 0:  # 0 if game is not finished

    p = players[cur_player + 1]
    canonical_board = game.getCanonicalForm(board, cur_player)
    valids = game.getValidMoves(canonical_board, cur_player)

    payload = {"board": board.tolist(),
               "cur_player": cur_player,
               "dtype": str(board.dtype),
               "shape": board.shape}
    j_board = json.dumps(payload)
    payload = json.loads(j_board)
    board = np.array(payload["board"], dtype=payload["dtype"]).reshape(payload["shape"])

    while True:
        print(board.shape, func)
        action = func[0](game.getCanonicalForm(board, cur_player))
        if action > len(valids):
            print("INVALID", action)
            continue
        break
    print(action, len(valids), valids)

    board, cur_player = game.getNextState(board, cur_player, action)
    print(board)
    it += 1
print(cur_player, board, it)
