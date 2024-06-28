from Tools.i_game import IGame, np
from Games.checkers_new.CheckersLogic import Board
import math


class CheckersGame(IGame):
    """
    Checkers Game class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, n=None):
        self.board = Board(n)
        self.n = n or self.board.n
        pass

    def getInitBoard(self):
        """return initial board (numpy array)"""
        b = Board(self.n)
        return b.pieces

    def getBoardSize(self):
        return (self.n, self.n)

    def getActionSize(self):
        """return number of all possible actions"""
        return self.board.get_action_size()[0] + self.board.get_action_size()[1]

    def getNextState(self, board, player, action):
        """if player takes action on board, return next (board,player)
          action must be a valid move"""
        b = Board(self.n, np.copy(board))
        b.execute_action(action, player)

        if b.last_long_capture:
            next_actions = b.get_moves_for_square(*b.last_long_capture, captures_only=True)
            if next_actions:
                return (b.pieces, player)  # Player continues with the same board state

        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        """returns a binary np.array (1 = still valid action, 0 = invalid)"""
        b = Board(self.n, pieces=np.copy(board))
        legal_moves = b.get_legal_moves(player)
        valid_moves = np.zeros(self.getActionSize(), dtype=int)
        
        for moves in legal_moves:
            for move in moves:
                x, y, nx, ny = move
                idx = self.calcValidMoveIndex(b, x, y, nx, ny)
                valid_moves[idx] = 1
        
        return valid_moves

    def getGameEnded(self, board, player):
        """returns 0 if not ended, 1 if player 1 won, -1 if player 1 lost"""
        b = Board(self.n, np.copy(board))
        if b.has_legal_moves(player):
            return 0
        if b.has_legal_moves(-player):
            return -1
        return 1

    def getCanonicalForm(self, board, player):
        """Board independent of the current player."""
        return player * board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        length = math.sqrt(len(pi))
        assert length.is_integer()
        length = int(length)
        pi_board = np.reshape(pi, (length, length))
        l = []

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
                    l.append((newB, list(newPi.ravel())))

        return l

    def translate(self, board: np.array, player: int, index: int) -> any:
        b = Board(self.n, np.copy(board))
        legal_moves = b.get_legal_moves(player)
        moves = [m for moves in legal_moves for m in moves]
        move_indices = [self.calcValidMoveIndex(b, m[0], m[1], m[2], m[3]) for m in moves]
        i = move_indices.index(index)
        return moves[i]

    def calcValidMoveIndex(self, board: Board, x: int, y: int, nx: int, ny: int):
        index = (((x * self.n + y) * (self.n - 1) * 4 + (nx - x + 1) * 2 + (ny - y + 1)) // 2) - 1
        padding = board.get_action_size()[1]
        if index > (self.getActionSize() - padding) // 2:
            index += padding
        return index

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
                        row_str += ' o |'  # o for Man
                    elif piece == 3:
                        row_str += ' @ |'  # @ for King
                    elif piece == -1:
                        row_str += ' x |'  # x for opponent's Man
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
                                 (col * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE))  #, 1

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
