from Tools.i_game import IGame, np
from Games.checkers.CheckersLogic import Board
import math


class CheckersGame(IGame):
    """
    Checkers Game class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, n: int = None):
        self.board = Board(n)
        self.n = n or self.board.n
        self.redundancy = 0
        self.ll_capture_hist = {}  # necessity of having a hist because undo function

    def getInitBoard(self):
        """return initial board (numpy array) and resets data"""
        self.resetData()
        return np.copy(self.board.pieces)

    def getBoardSize(self):
        return self.n, self.n

    def getActionSize(self):
        """return number of all possible actions"""
        return self.board.get_action_size()[0] + self.board.get_action_size()[1]

    def getNextState(self, board: np.array, player: int, action: tuple[int, int]):
        """if player takes action on board, return next (board,player)
          action must be a valid move"""
        b = Board(self.n, np.copy(board))

        if (self.stringRepresentation(b.pieces), player) in self.ll_capture_hist:
            b.last_long_capture = self.ll_capture_hist[(self.stringRepresentation(b.pieces), player)]

        pre_amount_pieces = np.count_nonzero(b.pieces)
        b.execute_action(action, player)
        post_amount_pieces = np.count_nonzero(b.pieces)
        if pre_amount_pieces == post_amount_pieces:
            self.redundancy += 1
        else:
            self.redundancy = 0

        if b.last_long_capture:
            next_actions = b.get_moves_for_square(*b.last_long_capture, player, captures_only=True)
            if next_actions:
                self.ll_capture_hist.update({(self.stringRepresentation(b.pieces), player): b.last_long_capture})
                return b.pieces, player  # player stays in turn if being able to capture another piece after capture

        return b.pieces, -player

    def getValidMoves(self, board: np.array, player: int):
        """returns a binary np.array (1 = valid action, 0 = invalid)"""
        b = Board(self.n, np.copy(board))

        if (self.stringRepresentation(b.pieces), player) in self.ll_capture_hist:
            b.last_long_capture = self.ll_capture_hist[(self.stringRepresentation(b.pieces), player)]
        legal_moves = b.get_legal_moves(player)
        valid_moves = np.zeros(self.getActionSize(), dtype=int)

        for moves_per_piece in legal_moves:
            for move in moves_per_piece:
                index = self.calcValidMoveIndex(b, move)
                valid_moves[index] = 1

        return valid_moves

    def getGameEnded(self, board: np.array, player: int):
        """returns 0 if not ended, 1 if player won, -1 if player lost"""
        if self.redundancy >= 30:
            self.redundancy = 0
            return 1e-4  # draw
        b = Board(self.n, np.copy(board))
        if b.has_legal_moves(player) and b.has_legal_moves(-player):
            return 0
        if b.has_legal_moves(player):
            self.redundancy = 0
            return 1
        if b.has_legal_moves(-player):
            self.redundancy = 0
            return -1
        self.redundancy = 0
        return 1e-4

    def getSymmetries(self, board: np.array, pi: list):
        """mirror, rotational"""
        length = math.sqrt(len(pi))
        assert length.is_integer()  # otherwise padding would be wrong
        length = int(length)

        # therefore the padding:
        # => getting a pi distribution in form of a square two-dimensional array according to all the valid moves
        # in validMoves
        # => being able to rotate pi vector in the same manner as the board
        # ==> moves getting their according pi probability
        pi_board = np.reshape(pi, (length, length))
        lst = []

        for i in [2, 4]:  # rotate by 180 degree
            for fliplr in [False, True]:
                for flipud in [False, True]:
                    newB = np.rot90(board, i)
                    newPi = np.rot90(pi_board, i)
                    if fliplr and flipud:
                        continue
                    if fliplr:
                        newB = np.fliplr(newB)
                        newPi = np.fliplr(newPi)
                    if flipud:
                        newB = np.flipud(newB)
                        newPi = np.flipud(newPi)
                    lst.append((newB, list(newPi.ravel())))

        return lst

    def translate(self, board: np.array, player: int, index: int) -> any:
        """translates index calculated by nnet model to actual move"""
        b = Board(self.n, np.copy(board))
        if (self.stringRepresentation(b.pieces), player) in self.ll_capture_hist:
            b.last_long_capture = self.ll_capture_hist[(self.stringRepresentation(b.pieces), player)]
        moves = b.flat_legal_moves(player)
        move_indices = [self.calcValidMoveIndex(b, m) for m in moves]
        i = move_indices.index(index)
        move = moves[i]
        one_d_move = self.two_d_to_one_d(move)
        return one_d_move

    def rotateMove(self, move: int | tuple[int, int]):
        """for our frontend - both players play from bottom to top
        => necessity to rotate move for one of the players"""
        empty_board = np.zeros([self.n, self.n], dtype=int)
        if type(move) is tuple:
            to_rotate = [*move]
        else:
            to_rotate = [move]
        rotated = []
        for pos in to_rotate:
            empty_board[pos // self.n, pos % self.n] = 1
            rot_board = np.rot90(empty_board, 2)
            rotated.append([i for i, pos in enumerate(rot_board.flatten()) if pos == 1][0])
            empty_board[pos // self.n, pos % self.n] = 0
        return rotated[0] if len(rotated) == 1 else (rotated[0], rotated[1])

    def resetData(self):
        self.redundancy = 0
        self.ll_capture_hist.clear()
        self.board = Board(self.n)

    def two_d_to_one_d(self, move: tuple[int, int, int, int]) -> tuple[int, int]:
        row, col, nrow, ncol = move
        return row * self.n + col, nrow * self.n + ncol

    def calcValidMoveIndex(self, board: Board, move: tuple[int, int, int, int]):
        """calculates unique index for every move in range getActionsSize for method validMoves ..."""
        row, col, nrow, ncol = move
        index = ((((row * self.n + col) * (self.n - 1) * 4 + (nrow - row + 1) * 2 + (ncol - col + 1) * 2) // 2) +
                 (self.n - 3))
        padding = board.get_action_size()[1]
        if index > ((self.getActionSize() - padding) // 2):  # inserting padding "in the middle"
            index += padding
        return index - 1  # because array starts with index 0

    def stringRepresentation(self, board):
        return board.tostring()

    def drawTerminal(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        if valid_moves:
            b = Board(self.n, pieces=np.copy(board))
            if (self.stringRepresentation(b.pieces), cur_player) in self.ll_capture_hist:
                b.last_long_capture = self.ll_capture_hist[(self.stringRepresentation(b.pieces), cur_player)]
            legal_moves = b.flat_legal_moves(cur_player)
            if args and len(args) > 0:  # returns valid moves only for the demanded position
                from_pos = args[0]
                one_dim_moves = [self.two_d_to_one_d(move) for move in legal_moves]
                return str([(f_pos, t_pos) for (f_pos, t_pos) in one_dim_moves if from_pos == f_pos])
            else:  # returns all valid moves
                return str([self.two_d_to_one_d(move) for move in legal_moves])

        else:
            horizontal_border = '  +' + '-' * (4 * self.n - 1) + '+\n'
            output = horizontal_border

            for row in range(self.n):
                row_str = f'{row} |'
                for col in range(self.n):
                    piece = board[row][col]
                    if piece == 0:
                        row_str += '   |'
                    elif piece == 1:
                        row_str += ' O |'  # O for Non_King
                    elif piece == 3:
                        row_str += ' @ |'  # @ for King
                    elif piece == -1:
                        row_str += ' X |'  # X for opponent's Non_King
                    elif piece == -3:
                        row_str += ' K |'  # K for opponent's King
                output += row_str + '\n' + horizontal_border

            # Add column indices below the board
            col_indices = '    ' + '   '.join([f'{col}' for col in range(self.n)]) + '\n'
            output += col_indices

            return output

    def draw(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        import pygame
        b = Board(self.n, np.copy(board))
        if (self.stringRepresentation(b.pieces), cur_player) in self.ll_capture_hist:
            b.last_long_capture = self.ll_capture_hist[(self.stringRepresentation(b.pieces), cur_player)]

        king_white_img = pygame.image.load('../Games/checkers/king_white.png')
        king_black_img = pygame.image.load('../Games/checkers/king_black.png')
        king_valid = pygame.image.load('../Games/checkers/king_valid.png')

        SQUARESIZE = 100
        WIDTH = self.n * SQUARESIZE
        HEIGHT = self.n * SQUARESIZE

        color_light_square = (252, 252, 244)  # Cream
        color_dark_square = (211, 178, 104)  # Sand
        color_piece_white = (255, 255, 255)  # White
        color_piece_black = (0, 0, 0)  # Black
        color_valid = (144, 238, 144)  # Light green for valid moves

        pygame.init()
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        valid_squares = []

        if valid_moves and args and len(args) > 0:  # for drawing highlighting where moves are possible
            from_pos = args[0]

            legal_moves = b.flat_legal_moves(cur_player)
            one_dim_moves = [self.two_d_to_one_d(move) for move in legal_moves]
            indices = [(i, f_pos) for i, (f_pos, t_pos) in enumerate(one_dim_moves) if from_pos == f_pos]
            for i, from_pos in indices:
                to_pos = one_dim_moves[i][1]
                row, col = to_pos // self.n, to_pos % self.n
                valid_squares.append((row, col, from_pos))  # destin. row and col and the pos from where the move came

        # Draw the board
        for row in range(self.n):
            for col in range(self.n):
                if (row + col) % 2 == 0:
                    square_color = color_light_square
                else:
                    square_color = color_dark_square

                # Draw grid
                pygame.draw.rect(surface, square_color,
                                 (col * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE))  # 1

                piece = board[row][col]
                center = (col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE // 2)
                radius = SQUARESIZE // 3

                if piece == -1:
                    self.drawToken(surface, color_piece_black, color_piece_white, center, radius)
                elif piece == -3:
                    king_image = king_black_img
                    if cur_player == -1:
                        king_image = pygame.transform.rotate(king_image, 180)
                    king_image = pygame.transform.scale(king_image, (SQUARESIZE, SQUARESIZE))
                    surface.blit(king_image, (col * SQUARESIZE, row * SQUARESIZE))
                elif piece == 1:
                    self.drawToken(surface, color_piece_white, color_piece_black, center, radius)
                elif piece == 3:
                    king_image = king_white_img
                    if cur_player == -1:
                        king_image = pygame.transform.rotate(king_image, 180)
                    king_image = pygame.transform.scale(king_image, (SQUARESIZE, SQUARESIZE))
                    surface.blit(king_image, (col * SQUARESIZE, row * SQUARESIZE))

                if valid_moves and args and len(args) > 0:
                    for a, b, from_pos in valid_squares:
                        if (row, col) == (a, b):
                            piece = board[from_pos // self.n][from_pos % self.n]
                            if abs(piece) == 1:
                                pygame.draw.circle(surface, color_valid, center, radius * 0.6)
                            if abs(piece) == 3:
                                king_image = king_valid
                                if cur_player == -1:
                                    king_image = pygame.transform.rotate(king_image, 180)
                                king_image = pygame.transform.scale(king_image,
                                                                    (SQUARESIZE * 0.6, SQUARESIZE * 0.6))

                                surface.blit(king_image, (col * SQUARESIZE + SQUARESIZE // 5,
                                                          row * SQUARESIZE + SQUARESIZE // 5))

        if cur_player == -1:
            surface = pygame.transform.rotate(surface, 180)  # Rotate board for player -1

        return surface

    def drawToken(self, surface, color1, color2, center, radius):
        import pygame
        pygame.draw.circle(surface, color2, center, radius * 1.05)
        pygame.draw.circle(surface, color1, center, radius)
        pygame.draw.circle(surface, color2, center, radius * 0.80)
        pygame.draw.circle(surface, color1, center, radius * 0.72)
