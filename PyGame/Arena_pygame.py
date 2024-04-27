import time
from io import BytesIO
from enum import Enum

import numpy as np
import pygame
import uvicorn
import requests
from PIL import Image

from IPlayer import IPlayer
from IGame import IGame


class STAGES(Enum):
    INIT = 0
    ACTION = 1
    PRINT = 2
    END = 3


class Arena:
    def __init__(self, player1: IPlayer, player2: IPlayer, game: IGame):
        self.player1: IPlayer = player1
        self.player2: IPlayer = player2
        self.game: IGame = game
        pygame.init()  # starting pygame instance

        self.action = None

    def playGame(self):
        players = [self.player2, None, self.player1]
        curPlayer = 1
        board = self.game.getInitBoard()
        it = 0
        while self.game.getGameEnded(board, curPlayer) == 0:
            it += 1
            print("Turn ", str(it), "Player ", str(curPlayer))
            self.sendSurface(self.game.draw(board))
            action: int = players[curPlayer + 1].play(self.game.getCanonicalForm(board, curPlayer))
            print(action)
            time.sleep(2)
            valids = self.game.getValidMoves(self.game.getCanonicalForm(board, curPlayer), 1)
            print(valids)
            #assert valids[action] > 0
            board, curPlayer = self.game.getNextState(board, curPlayer, action)
            #print("Game over: Turn ", str(it), "Result ", str(self.game.getGameEnded(board, 1)))
            #surface = self.game.draw(board)
        return curPlayer * self.game.getGameEnded(board, curPlayer)

    def sendSurface(self, surface: pygame.surface):
        image_buffer = BytesIO()
        pygame.image.save(surface, image_buffer, "PNG")
        image_buffer.seek(0)  # Reset the buffer position to the start

        url = 'http://127.0.0.1:8000/png'
        # Prepare the payload with the BytesIO buffer as a file
        files = {'file': ('surface.png', image_buffer, 'image/png')}
        try:
            response = requests.post(url, files=files)
            #print(response.json())

        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)


if __name__ == "__main__":
    from TicTacToePlayers import HumanTicTacToePlayer, HumanAPIPlayer
    from TicTacToeGame import TicTacToeGame
    g = TicTacToeGame()
    #p1 = HumanTicTacToePlayer(g)
    p1 = HumanAPIPlayer(g)
    p2 = HumanTicTacToePlayer(g)
    a = Arena(p1, p2, g)
    a.playGame()
