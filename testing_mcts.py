import time

import numpy as np

from Tools.dynamic_imports import Importer
from Games.connect4.Connect4Game import Connect4Game
from Tools.Game_Config.difficulty import EDifficulty

importer = Importer("./Games")
game = Connect4Game()
board = game.getInitBoard()

diff = EDifficulty.easy

functions = importer.get_ai_func()

if len(functions) == 0:
    raise FileNotFoundError("path of Importer instance is not found")

mcts = importer.get_ai_func() .get("connect4").get(diff)
func = lambda x, y, n: np.argmax(mcts.get_action_prob(x, y, temp=(0.5 if n <= 6 else 0.)))

print("Staring calculation ...")
start_time = time.perf_counter()
action = func(board, 1, 0)
end_time = time.perf_counter()

print(f"Generating new action took '{end_time-start_time:.8}s' on '{diff.value} ({diff.name})' MCTS iterations.")
