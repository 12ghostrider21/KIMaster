from Tools.i_game import IGame, np
from Games.nim.NimLogic import Board


class NimGame(IGame):

    def __init__(self, rows=4):
        self.rows = rows
        self.winner = None

    def getInitBoard(self):
        """return initial board (numpy array)"""
        return Board(self.rows).pieces

    def getBoardSize(self):
        return self.rows

    def getActionSize(self):
        """return number of all possible actions"""
        b = Board(self.rows)
        return len(b.get_legal_moves())

    def getNextState(self, board, player, action):
        """if player takes action on board, return next (board,player)
          action must be a valid move"""
        b = Board(self.rows, np.copy(board))
        b.execute_action(action)
        if b.is_game_over():
            self.winner = player
        return b.pieces, -player

    def getValidMoves(self, board, player):
        """returns a binary np.array (1 = still valid action, 0 = invalid"""
        b = Board(self.rows)  # fresh game, all possible valid moves
        valids_new = b.get_legal_moves()

        b.pieces = np.copy(board)  # running game
        valids_input = b.get_legal_moves()

        return np.array([tuple(item) in valids_input for item in valids_new])

    def getGameEnded(self, board, player):
        """returns 0 if not ended, 1 if player won, -1 if player lost"""
        b = Board(self.rows, np.copy(board))
        if not b.is_game_over():
            return 0
        if self.winner == player:
            return 1
        if self.winner == -player:
            return -1

    def getCanonicalForm(self, board, player):
        """Does not matter with NimGame"""
        return board

    def getSymmetries(self, board, pi):
        """rows are interchangeable"""
        fresh_board = Board(self.rows)

        reshaped_pi = np.empty(self.rows, dtype=object)

        start_index = 0
        for i, num_elements in enumerate(fresh_board.pieces):
            reshaped_pi[i] = list(pi[start_index:(start_index + num_elements)])
            start_index += num_elements

        sym_board = self.permute(board.tolist())
        sym_pi = self.permute(reshaped_pi.tolist())
        sym_pi_flat = []
        for i in range(len(sym_pi)):
            sym_pi_flat.append([prob for sublist in sym_pi[i] for prob in sublist])
        symmetries = list(zip(sym_board, sym_pi_flat))

        return symmetries

    def permute(self, array):
        """used to swap all rows in all possible permutations/ symmetries"""
        if len(array) == 0:
            return []
        if len(array) == 1:
            return [array]

        permutations = []
        for i in range(len(array)):
            m = array[i]
            remaining_list = array[:i] + array[i + 1:]
            for p in self.permute(remaining_list):
                permutations.append([m] + p)
        return permutations

    def translate(self, board: np.array, player: int, index: int):
        b = Board(self.rows)
        valids = b.get_legal_moves()
        return valids[index]

    def stringRepresentation(self, board):
        return board.tostring()

    def drawTerminal(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        if valid_moves:
            b = Board(self.rows, np.copy(board))
            return str(b.get_legal_moves())
        else:
            s = "\n"
            i = 0
            for n in board:
                s += f"({i})  " + "I " * n + "\n"
                i += 1
            return s

    def draw(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        import pygame
        PIECE_HEIGHT = 110
        PIECE_WIDTH = 25
        HEIGHT = self.rows * (PIECE_HEIGHT + 40)
        WIDTH = HEIGHT
        CENTER = HEIGHT // 2
        OUTLINING = 4
        expand_factor = 0.25

        y_scale = HEIGHT / (self.rows + 1)
        x_scale = [0] * self.rows
        for i in range(self.rows):
            x_scale[i] = WIDTH / (board[i] + 1)

        color_background = (252, 252, 244)  # cream
        color_piece_detail = (172, 244, 230)  # light blue
        color_valid = (144, 238, 144)  # turquoise
        color_outline = (0, 0, 0)  # black
        color_piece = (0, 70, 175)  # dark blue

        pygame.init()

        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        surface.fill(color_background)

        color_detail = color_valid if valid_moves else color_piece_detail

        y = 1
        for pieces in board:
            for x in range(1, (pieces + 1)):
                stretch = (y * y_scale - CENTER) * expand_factor
                # stretch in order to get proportional more whitespace between the pieces in y direction

                pygame.draw.rect(surface, color_outline,
                                 pygame.Rect(x * x_scale[y - 1] - PIECE_WIDTH / 2 - OUTLINING / 2,
                                             y * y_scale + stretch - PIECE_HEIGHT / 2 - OUTLINING / 2,
                                             PIECE_WIDTH + OUTLINING,
                                             PIECE_HEIGHT + OUTLINING))  # grey outlining
                pygame.draw.rect(surface, color_piece,
                                 pygame.Rect(x * x_scale[y - 1] - PIECE_WIDTH / 2,
                                             y * y_scale + stretch - PIECE_HEIGHT / 2,
                                             PIECE_WIDTH,
                                             PIECE_HEIGHT))  # pieces themselves
                pygame.draw.rect(surface, color_detail,
                                 pygame.Rect(x * x_scale[y - 1] - PIECE_WIDTH / 3.55,
                                             y * y_scale + stretch - PIECE_HEIGHT / 2.2,
                                             PIECE_WIDTH - 10,
                                             PIECE_HEIGHT - 10))  # inner piece detail

            y += 1

        return surface
