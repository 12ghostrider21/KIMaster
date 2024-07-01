from Tools.i_game import IGame, np
from Games.checkers_new.CheckersLogic import Board
import math


class CheckersGame(IGame):
    """
    Checkers Game class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, n: int = None):
        self.board = Board(n)
        self.n = n or self.board.n
        self.turn = 1  # reason: CheckersLogic get_legal_moves
        self.board_history = []
        self.board_history.append(self.board.pieces)
        # self.board_turn_history = {}
        # self.board_history.update({self.stringRepresentation(self.board.pieces): self.turn})
        self.turn_history = []
        self.turn_history.append(self.turn)
        self.redundant = 0

    def getInitBoard(self):
        """return initial board (numpy array)"""
        b = Board(self.n)
        return b.pieces

    def getBoardSize(self):
        return self.n, self.n

    def getActionSize(self):
        """return number of all possible actions"""
        return self.board.get_action_size()[0] + self.board.get_action_size()[1]

    def getNextState(self, board: np.array, player: int, action: tuple[int, int, int, int]):
        """if player takes action on board, return next (board,player)
          action must be a valid move"""
        self.calcTurn(board)
        b = Board(self.n, np.copy(board))
        pre_amount_pieces = np.count_nonzero(b.pieces)
        b.execute_action(action, player, self.turn)
        post_amount_pieces = np.count_nonzero(b.pieces)
        if pre_amount_pieces == post_amount_pieces:
            self.redundant += 1
        else:
            self.redundant = 0

        if b.last_long_capture:
            next_actions = b.get_moves_for_square(*b.last_long_capture, self.turn, captures_only=True)
            if next_actions:
                self.board_history.append(self.getCanonicalForm(b.pieces, player))
                self.turn_history.append(self.turn)
                return b.pieces, player  # Player continues with the same board state
        self.turn = -self.turn
        self.board_history.append(self.getCanonicalForm(b.pieces, -player))
        self.turn_history.append(self.turn)
        return b.pieces, -player

    def getValidMoves(self, board: np.array, player: int):
        """returns a binary np.array (1 = still valid action, 0 = invalid)"""
        self.calcTurn(board)
        b = Board(self.n, pieces=np.copy(board))
        legal_moves = b.get_legal_moves(player, self.turn)
        valid_moves = np.zeros(self.getActionSize(), dtype=int)

        for moves in legal_moves:
            for move in moves:
                index = self.calcValidMoveIndex(b, move)
                valid_moves[index] = 1

        return valid_moves

    def getGameEnded(self, board: np.array, player: int):
        """returns 0 if not ended, 1 if player 1 won, -1 if player 1 lost"""
        if self.redundant >= 30:
            self.redundant = 0
            return 1e-4  # draw
        self.calcTurn(board)
        b = Board(self.n, np.copy(board))
        if b.has_legal_moves(player, self.turn):
            return 0
        if b.has_legal_moves(-player, -self.turn):
            return -1
        return 1

    def getCanonicalForm(self, board: np.array, player: int):
        """Board independent of the current player."""
        return player * board

    def getSymmetries(self, board: np.array, pi: list):
        # mirror, rotational
        length = math.sqrt(len(pi))
        assert length.is_integer()  # otherwise padding would be wrong
        length = int(length)
        pi_board = np.reshape(pi, (length, length))
        lst = []

        for i in [2, 4]:
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
        """
        print("len(board_history)_pre", len(self.board_history))
        print("board_history_pre", self.board_history[-3:])
        print("self.turn_history_pre", self.turn_history)
        print("self.turn_pre", self.turn)
        """
        self.calcTurn(board)
        """
        print("len(board_history)_post", len(self.board_history))
        print("board_history_pre", self.board_history[-4:-1])
        print("self.turn_history_post", self.turn_history)
        print("self.turn_post", self.turn)
        """
        b = Board(self.n, np.copy(board))
        legal_moves = b.get_legal_moves(player, self.turn)
        moves = [m for moves in legal_moves for m in moves]
        move_indices = [self.calcValidMoveIndex(b, m) for m in moves]
        # print("move_indices", move_indices)
        i = move_indices.index(index)
        return moves[i]

    def calcValidMoveIndex(self, board: Board, move: tuple[int, int, int, int]):
        row, col, nrow, ncol = move
        index = ((((row * self.n + col) * (self.n - 1) * 4 + (nrow - row + 1) * 2 + (ncol - col + 1) * 2) // 2) +
                 (self.n - 3))
        padding = board.get_action_size()[1]
        if index > ((self.getActionSize() - padding) // 2):
            index += padding
        return index - 1  # because array starts with index 0

    def calcTurn(self, board: np.array):
        """
        Calculating turn based on occurrence of board in self.board_history.
        A simple switch of turns in getNextState without having calcTurn is not enough because of function "undo".
        """
        # print("boardCalcTurn", board)
        index = -1
        for i, b in enumerate(self.board_history):
            if np.array_equal(b, board):
                index = i
        # print("indexCalc", index)
        if index != -1:
            self.board_history = self.board_history[:(index + 1)]
            self.turn_history = self.turn_history[:(index + 1)]
            self.turn = self.turn_history[-1]

    def stringRepresentation(self, board):
        return board.tostring()

    def drawTerminal(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        if valid_moves:
            return str([i for (i, valid) in enumerate(self.getValidMoves(board, 1)) if valid])
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
        king_white_img = pygame.image.load('king_white.png')
        king_black_img = pygame.image.load('king_black.png')

        SQUARESIZE = 100
        WIDTH = self.n * SQUARESIZE
        HEIGHT = self.n * SQUARESIZE

        color_light_square = (252, 252, 244)  # Cream
        color_dark_square = (139, 81, 19)  # Brown
        color_piece_white = (255, 255, 255)  # White
        color_piece_black = (31, 21, 11)  # Dark Brown
        color_valid = (144, 238, 144)  # Light green for valid moves

        pygame.init()
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

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
                    pygame.draw.circle(surface, color_piece_black, center, radius)
                elif piece == -3:
                    king_image = king_black_img
                    if cur_player == -1:
                        king_image = pygame.transform.rotate(king_image, 180)
                    king_image = pygame.transform.scale(king_image, (SQUARESIZE, SQUARESIZE))
                    surface.blit(king_image, (col * SQUARESIZE, row * SQUARESIZE))
                elif piece == 1:
                    pygame.draw.circle(surface, color_piece_white, center, radius)
                elif piece == 3:
                    king_image = king_white_img
                    if cur_player == -1:
                        king_image = pygame.transform.rotate(king_image, 180)
                    king_image = pygame.transform.scale(king_image, (SQUARESIZE, SQUARESIZE))
                    surface.blit(king_image, (col * SQUARESIZE, row * SQUARESIZE))

                # Highlight valid moves if necessary
                if valid_moves:
                    valids = self.getValidMoves(board, cur_player)
                    if valids[(row * len(board[row])) + col]:
                        pygame.draw.circle(surface, color_valid, center, radius)

        if cur_player == -1:
            surface = pygame.transform.rotate(surface, 180)  # Rotate board for player -1

        return surface
