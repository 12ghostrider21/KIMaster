from Tools.i_game import IGame, np
from Games.nim.NimLogic import Board


class NimGame(IGame):

    def __init__(self, rows=4):
        self.rows = rows
        self.winner = None

    def getInitBoard(self):
        """return initial board (numpy array)"""
        #@ return Board(self.rows).pieces
        return Board(self.rows)

    def getBoardSize(self):
        return self.rows

    def getActionSize(self):
        """return number of all possible actions"""
        #@ b = Board(self.rows)
        b = self.getInitBoard()
        return len(b.get_valid_actions())

    def getNextState(self, board, player, action):
        """if player takes action on board, return next (board,player)
          action must be a valid move"""
        b = Board(self.rows, np.copy(board))
        b.execute_action(action, player)
        if b.is_game_over():
            self.winner = player
        return b.pieces, -player

    def getValidMoves(self, board, player):
        """returns a binary np.array (1 = still valid action, 0 = invalid"""
        
        """@
        b = Board(self.rows, np.copy(board))
        valid_moves = b.get_valid_actions()
        valid_vector = np.zeros(self.getActionSize(), dtype=int)
        for move in valid_moves:
            idx = move[0] * self.rows + move[1] - 1  # Convert move to index
            valid_vector[idx] = 1
        return valid_vector
        """
        b = self.getInitBoard()  # fresh game, all possible valid moves
        valids_new = b.get_valid_actions()

        b.pieces = np.copy(board)  # running game
        valids_running = b.get_valid_actions()

        return np.isin(valids_new, valids_running)

    def getGameEnded(self, board, player):
        """returns 0 if not ended, 1 if player 1 won, -1 if player 1 lost"""
        
        """@
        b = Board(self.rows, np.copy(board))
        if not b.is_game_over():
            return 0
        return 1 if self.winner == 1 else -1
        """
        b = self.getInitBoard()
        b.pieces = np.copy(board)
        if not b.is_game_over():
            return 0
        return self.winner

    def getCanonicalForm(self, board, player):
        """Does not matter with NimGame"""
        return board

    def getSymmetries(self, board, pi):
        """rows are interchangeable"""

        """@
        symmetries = []
        for perm in self.permute(list(range(self.rows))):
            new_board = board[perm]
            new_pi = pi.reshape(self.rows, -1)[perm].flatten()
            symmetries.append((new_board, new_pi))
        return symmetries
        """

        b = self.getInitBoard()
        b.pieces = np.copy(board)

        # reshaping the valid actions based on their row indices to swap rows accordingly
        valids = b.get_valid_actions()
        reshaped_pi = np.empty(self.rows, dtype=object)
        for i in range(self.rows):
            reshaped_pi[i] = np.array([])
        for i in range(valids):
            action = valids[i]
            probability = pi[i]
            reshaped_pi[action[0]].append(probability)

        sym_board = self.permute(b.pieces)
        sym_pi = self.permute(reshaped_pi)
        symmetries = list(zip(sym_board, sym_pi))
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

    def stringRepresentation(self, board):
        return board.tostring()

    def draw_terminal(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        if valid_moves:
            #return str([i for (i, valid) in enumerate(self.getValidMoves(board, 1)) if valid])
            b = self.getInitBoard()
            b.pieces = np.copy(board)
            return b.get_valid_actions()
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
