from __future__ import print_function
#import sys
#sys.path.append('..')
from Tools.i_game import IGame
from Games.nogo.NogoLogic import Board
from Games.nogo.board_util import GoBoardUtil, BLACK, WHITE, coord_to_point

import numpy as np

class NogoGame(IGame):
    square_content = {
        -1: "w",
        +0: "-",
        +1: "b"
    }


    @staticmethod
    def getSquarePiece(piece):
        return NogoGame.square_content[piece]


    def __init__(self, n=7):
        self.n = n
        self.board = Board(n)
        self.root = None

    def beginSearch(self):
        self.root = self.board.copy()
        self.board, self.root = self.board, self.root


    def inSearch(self):
        self.board = self.root.copy()


    def endSearch(self):
        self.board = self.root.copy()
        self.root = None

    def copy(self):
        copy = NogoGame(self.n)
        copy.board = self.board.copy()

    def getInitBoard(self):
        # return initial board (numpy board)
        self.board.reset(self.n)
        return self.get_pieces()

    def reset(self, size):
        self.board.reset(self.n)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n

    def getNextState(self, board, player, action, fast=False):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if fast:
            move = (int(action/self.n), action%self.n)
            board[move[0]][move[1]] = player
            return board, -player
        action = self.convert_point(action)
        self.board.play_move(action, self.board.current_player)
        return self.get_pieces(), self.convert_back_color()


    def convert_color(self, player):
        if player == 1:
            return BLACK
        elif player == -1:
            return WHITE
        else: return None

    def convert_back_color(self):
        if self.board.current_player == WHITE:
            return -1
        if self.board.current_player == BLACK:
            return 1
        else: return None

    def convert_coord(self, coord):
        return (self.n - coord[0] , coord[1] + 1)

    def convert_point(self, point):
        coord = (self.n - 1 - int(point/self.n), point%self.n)
        coord = self.convert_coord(coord)
        return coord_to_point(coord[0],coord[1],self.n)

    def convert_back_point(self, point):
        row, col = self.board._point_to_coord(point)
        return (row - 1)*(self.n) + (col - 1)

    def getValidMoves(self, board, player, search=False):
        # return a fixed size binary vector
        color = self.board.current_player
        moves = self.board.get_empty_points()
        if search:
            legal = moves
        else:
            legal = []
            for move in moves:
                if self.board.is_legal(move, color):
                    legal.append(move)
        valids = [0]*self.getActionSize()
        for point in legal:
            valids[self.convert_back_point(point)] = 1
        return np.array(valids)


    def getGameEnded(self, board, player, search=False):
        # return 0 if not ended, 1 if player won, -1 if player lost
        if search:
            return 0
        legal_moves = self.getValidMoves(board, player)
        if legal_moves.max() == 1:
            return 0
        else:
            return -self.convert_back_color()

    def get_pieces(self):
        pieces = GoBoardUtil.get_twoD_board(self.board)
        empty = (pieces == 0).astype(int)
        empty = np.multiply(-3,empty)
        pieces = np.multiply(-2,pieces)
        pieces = np.add(3, pieces)
        pieces = np.add(empty, pieces)
        return pieces

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2)
        pi_board = np.reshape(pi, (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()))]
        return l

    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    def translate(self, board: np.array, player: int, index: int):
        return index

    def drawTerminal(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
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
                print(NogoGame.square_content[piece], end=" ")
            print("|")

        print("-----------------------")

    def draw(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        import pygame
        row_count = len(board) #baord.size
        col_count = len(board[0]) #baord.size
        SQUARESIZE = 90
        WIDTH = row_count * SQUARESIZE
        HEIGHT = col_count * SQUARESIZE
        MARGIN = SQUARESIZE // 2  # Rand um das Spielbrett

        color_background = (251, 196, 103)  # light brown/cream
        color_grid = (0, 0, 0) # black
        color_ply_one = (0, 0, 0)  # black
        color_ply_minus_one = (255, 255, 255)  # white
        color_valid = (144, 238, 144)  # Light green for valid moves

        pygame.init()
        surface = pygame.Surface((WIDTH + 2 * MARGIN, HEIGHT + 2 * MARGIN), pygame.SRCALPHA)
        surface.fill(color_background)

        # Draw the board
        for row in range(row_count):
            for col in range(col_count):
                center = (col * SQUARESIZE + MARGIN, row * SQUARESIZE + MARGIN)
                radius = SQUARESIZE // 2 - 1

                pygame.draw.rect(surface, color_grid, (col * SQUARESIZE + MARGIN, row * SQUARESIZE + MARGIN, SQUARESIZE, SQUARESIZE), 1)

                valids = self.getValidMoves(board, cur_player)
                if valid_moves and valids[row * col_count + col]:
                    pygame.draw.circle(surface, color_valid, center, radius)

                if board[row][col] == 1:
                    pygame.draw.circle(surface, color_ply_one, center, radius)
                elif board[row][col] == -1:
                    pygame.draw.circle(surface, color_ply_minus_one, center, radius)
                    pygame.draw.arc(surface, (0, 0, 0), pygame.Rect(center[0] - radius, center[1] - radius, 2 * radius, 2 * radius), 0, np.pi * 2, 1)
        return surface
