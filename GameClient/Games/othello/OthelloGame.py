#from __future__ import print_function
#import sys
#sys.path.append('..')
#from Game import Game
import numpy as np
import pygame
from Tools.i_game import IGame
from .OthelloLogic import Board

class OthelloGame(IGame):
    square_content = {
        -1: "X",
        +0: "-",
        +1: "O"
    }

    @staticmethod
    def getSquarePiece(piece):
        return OthelloGame.square_content[piece]

    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.n*self.n:
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action/self.n), action%self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n*x+y]=1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)
        if b.has_legal_moves(player):
            return 0
        if b.has_legal_moves(-player):
            return 0
        if b.countDiff(player) > 0:
            return 1
        return -1

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2+1)  # 1 for pass
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
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    def getScore(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)
        return b.countDiff(player)

    def draw_terminal(self, board, valid_moves, *args: any):
        pass

    def draw(self, board, valid_moves, *args: any):
        row_count = board.shape[0]
        col_count = board.shape[1]
        SQUARESIZE = 100
        WIDTH = col_count * SQUARESIZE
        HEIGHT = row_count * SQUARESIZE

        color_board = (3, 138, 70)
        color_grid = (0, 0, 0)
        color_shadow = (50, 50, 50, 150)
        color_ply_one = (0, 0, 0) # black
        color_ply_minus_one = (255, 255, 255) # white
        color_valid = (144, 238, 144) # turquoise

        pygame.init()

        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        surface.fill(color_board)

        for row in range(len(board)):
            for col in range(len(board[row])):
                center = (col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE // 2)
                radius = SQUARESIZE // 3

                pygame.draw.rect(surface, color_grid,
                                 (col * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE),
                                 1)   # show grid
                if valid_moves and row == 0 and col in [i for (i, valid) in enumerate(self.getValidMoves(board, 0)) if valid]:
                    pygame.draw.circle(surface, color_valid,
                                       (col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE // 2),
                                       SQUARESIZE // 3)  # displaying valid moves
                if board[row][col] == 1: 
                    '''pygame.draw.circle(surface, color_shadow,
                                       (center[0] + 2, center[1] + 2), 
                                       radius + 1) # shadow'''
                    pygame.draw.circle(surface,  color_ply_one,
                                       (col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE // 2),
                                       SQUARESIZE // 3)
                elif board[row][col] == -1:
                    '''pygame.draw.circle(surface, color_shadow,
                                       (center[0] + 2, center[1] + 2), 
                                       radius + 1) # shadow'''
                    pygame.draw.circle(surface,  color_ply_minus_one,
                                       (col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE+ SQUARESIZE // 2),
                                       SQUARESIZE // 3)
                    pygame.draw.arc(surface, (0, 0, 0),
                                    pygame.Rect(center[0] - radius, center[1] - radius, 2 * radius, 2 * radius),
                                    0, np.pi * 2, 1)

        img = pygame.image.tostring(surface, 'RGBA')
        return img

"""
    @staticmethod
    def display(board):
        n = board.shape[0]
        print("   ", end="")
        for y in range(n):
            print(y, end=" ")
        print("")
        print("-----------------------")
        for y in range(n):
            print(y, "|", end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                print(OthelloGame.square_content[piece], end=" ")
            print("|")

        print("-----------------------")
        """
