from __future__ import print_function
import sys
from io import BytesIO

import pygame
from PIL import Image

sys.path.append('..')
from TicTacToe_PyGame.Interfaces.Game import Game
from TicTacToeLogic import Board
import numpy as np

"""
TicTacToe_PyGame class implementation for the game of TicTacToe.
Based on the OthelloGame then getGameEnded() was adapted to new rules.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloGame by Surag Nair.
"""


class TicTacToeGame(Game):
    def __init__(self, n=3):
        super().__init__()
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return self.n, self.n

    def getActionSize(self):
        # return number of actions
        return self.n * self.n + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.n * self.n:
            return board, -player
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action / self.n), action % self.n)
        b.execute_move(move, player)
        return b.pieces, -player

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n * x + y] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)

        if b.is_win(player):
            return 1
        if b.is_win(-player):
            return -1
        if b.has_legal_moves():
            return 0
        # draw has a very little value 
        return 1e-4

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player * board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert (len(pi) == self.n ** 2 + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    @staticmethod
    def display(board):
        n = board.shape[0]

        print("   ", end="")
        for y in range(n):
            print(y, "", end="")
        print("")
        print("  ", end="")
        for _ in range(n):
            print("-", end="-")
        print("--")
        for y in range(n):
            print(y, "|", end="")  # print the row #
            for x in range(n):
                piece = board[y][x]  # get the piece to print
                if piece == -1:
                    print("X ", end="")
                elif piece == 1:
                    print("O ", end="")
                else:
                    if x == n:
                        print("-", end="")
                    else:
                        print("- ", end="")
            print("|")

        print("  ", end="")
        for _ in range(n):
            print("-", end="-")
        print("--")

    @staticmethod
    def display_pyGame(board: np.array):
        n = board.shape[0]

        square_size = 100  # Size of each square in pixels
        board_size = square_size * n
        line_width = 5
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)

        surface = pygame.Surface(size=(board_size, board_size))
        surface.fill((255, 255, 255))  # Fill the surface with white background

        # draw grid
        for i in range(1, n):
            pygame.draw.line(surface=surface, color=(0, 0, 0), start_pos=(0, i * 100), end_pos=(n * 100, i * 100),
                             width=line_width)
            pygame.draw.line(surface=surface, color=(0, 0, 0), start_pos=(i * 100, 0), end_pos=(i * 100, n * 100),
                             width=line_width)

        for y, row in enumerate(board):
            for x, elem in enumerate(row):
                if elem == -1:
                    pygame.draw.line(surface, RED, (0+x*100, 0+y*100), (100*x+100, 100+y*100), line_width)
                    pygame.draw.line(surface, RED, (0+x*100, 100*y+100), (100*x+100, 0+y*100), line_width)
                if elem == 1:
                    size = square_size / 2
                    pygame.draw.circle(surface, BLUE, (x * square_size + size, y * square_size + size),
                                       min(square_size, square_size) // n, line_width)

        # to look the image
        pygame.image.save(surface, 'tictactoe_board.png')

        # Convert Pygame surface to string format
        image_string = pygame.image.tostring(surface, 'RGBA')

        # Create PIL image from string data
        image = Image.frombytes('RGBA', surface.get_size(), image_string)

        # Create in-memory file object
        img_byte_array = BytesIO()

        # Save PIL image to in-memory file object as PNG
        image.save(img_byte_array, format='PNG')

        # Get bytes data from in-memory file object
        img_byte_array.seek(0)
        png_bytes = img_byte_array.getvalue()

        return png_bytes
