import numpy as np
import pygame
from Tools.i_game import IGame
from Connect4Logic import Board


class Connect4Game(IGame):
    """
    Connect4 Game class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, height=None, width=None, win_length=None, np_pieces=None):
        self._base_board = Board(height, width, win_length, np_pieces)

    def getInitBoard(self):
        return self._base_board.np_pieces

    def getBoardSize(self):
        return self._base_board.height, self._base_board.width

    def getActionSize(self):
        return self._base_board.width

    def getNextState(self, board, player, action):
        """Returns a copy of the board with updated move, original board is unmodified."""
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        b.add_stone(action, player)
        return b.np_pieces, -player

    def getValidMoves(self, board, player):
        "Any zero value in top row in a valid move"
        return self._base_board.with_np_pieces(np_pieces=board).get_valid_moves()

    def getGameEnded(self, board, player):
        b = self._base_board.with_np_pieces(np_pieces=board)
        winstate = b.get_win_state()
        if winstate.is_ended:
            if winstate.winner is None:
                # draw has very little value.
                return 1e-4
            elif winstate.winner == player:
                return +1
            elif winstate.winner == -player:
                return -1
            else:
                raise ValueError('Unexpected winstate found: ', winstate)
        else:
            # 0 used to represent unfinished game.
            return 0

    def getCanonicalForm(self, board, player) -> np.array:
        # Flip player from 1 to -1
        return board * player

    def getSymmetries(self, board, pi):
        """Board is left/right board symmetric"""
        return [(board, pi), (board[:, ::-1], pi[::-1])]

    def stringRepresentation(self, board):
        return board.tostring()

    def draw_terminal(self, board, valid_moves, *args: any):
        if valid_moves:
            return str([i for (i, valid) in enumerate(self.getValidMoves(board, 1)) if valid])
        else:
            horizontal_border = '+' + '-' * (4 * len(board[0]) - 1) + '+\n'

            output = horizontal_border # board
            for row in range(len(board)):
                row_str = '|'
                for col in range(len(board[row])):
                    if board[row][col] == 0:
                        row_str += '   |'
                    elif board[row][col] == 1:
                        row_str += ' O |'
                    else:
                        row_str += ' X |'
                output += row_str + '\n' + horizontal_border

            output += horizontal_border # board index
            column_numbers = '|'
            for col in range(len(board[0])):
                column_numbers += f' {col + 1} |'
            output += column_numbers + '\n'

            return output

    def draw(self, board: np.array, valid_moves: bool, *args: any):
        row_count = board.shape[0]
        col_count = board.shape[1]
        SQUARESIZE = 100
        WIDTH = col_count * SQUARESIZE
        HEIGHT = (row_count + 1) * SQUARESIZE
        TOKENSIZE = SQUARESIZE // 2

        color_filling = (252, 252, 244) # colorscheme = "light"  # when implementing dark mode / high contrast
        color_ply_one = (252, 239, 0) # yellow
        color_ply_minus_one = (244, 58, 58) # red
        color_valid = (144, 238, 144) # turquoise

        pygame.init()

        # creating empty surface and filling it with the appropriate color
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        surface.fill((45, 116, 216))
        pygame.draw.rect(surface, color_filling, pygame.Rect(0, 0, WIDTH, SQUARESIZE))

        """ when implementing dark mode / high contrast
        # setting color based on color arg
        if args:
            if "colorscheme" in args[1]:
                colorscheme = args[1]["colorscheme"]
            if colorscheme == "dark":
                color = (71, 71, 71)
        """

        # draw board
        for col in range(col_count):
            for row in range(row_count):
                pygame.draw.circle(surface, color_filling, 
                                   (col * SQUARESIZE + TOKENSIZE, (row + 1) * SQUARESIZE + TOKENSIZE), 
                                   TOKENSIZE - 5)  # holes in the board
                if valid_moves and row == 0 and col in [i for (i, valid) in enumerate(self.getValidMoves(board, 0)) if valid]:
                    pygame.draw.circle(surface, color_valid,
                                       (col * SQUARESIZE + TOKENSIZE, row * SQUARESIZE + TOKENSIZE), 
                                       TOKENSIZE - 5)  # displaying valid moves
                if board[row][col] == -1:
                    self.draw_chip(surface, color_ply_minus_one, (col * SQUARESIZE + TOKENSIZE, (row + 1) * SQUARESIZE + TOKENSIZE), TOKENSIZE - 5)
                elif board[row][col] == 1:
                    self.draw_chip(surface, color_ply_one, (col * SQUARESIZE + TOKENSIZE, (row + 1) * SQUARESIZE + TOKENSIZE), TOKENSIZE - 5)
        return surface

    def draw_chip(self, surface, color, position, radius):
        pygame.draw.circle(surface, color, position, radius)
        dark_edge_color = (color[0] // 2, color[1] // 2, color[2] // 2)
        pygame.draw.circle(surface, dark_edge_color, position, radius, 3)
