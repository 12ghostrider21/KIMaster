import numpy as np
import requests

from IPlayer import IPlayer
from IGame import IGame

"""
Random and Human-ineracting players for the game of TicTacToe.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloPlayers by Surag Nair.

"""


class RandomPlayer(IPlayer):
    def __init__(self, game):
        self.game = game

    def play(self, board: np.array) -> int:
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanTicTacToePlayer(IPlayer):
    def __init__(self, game):
        self.game = game

    def play(self, board: np.array) -> int:
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                print(int(i / self.game.n), int(i % self.game.n))
        while True:
            # Python 3.x
            a = input()
            # Python 2.x 
            # a = raw_input()

            x, y = [int(x) for x in a.split(' ')]
            a = self.game.n * x + y if x != -1 else self.game.n ** 2
            if valid[a]:
                break
            else:
                print('Invalid')
        return a


class HumanAPIPlayer(IPlayer):
    def __init__(self, game):
        self.game = game

    def play(self, board: np.array) -> int:
        url = 'http://127.0.0.1:8000/play'  # Update with your FastAPI server URL

        # Send a POST request with the NumPy array converted to JSON
        try:
            response = requests.post(url, json=board.tolist())
            if response.status_code == 200:
                response_data = response.json()
                return response_data
            else:
                print(f"Failed to send array. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
        return -1
