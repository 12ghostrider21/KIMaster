from Tools.Game_dev import IGame, np, pygame
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

    def __init__(self, n=6):
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
        if b.has_legal_moves(player):
            return 0
        if b.has_legal_moves(-player):
            return 0
        if b.countDiff(player) > 0:
            return 1
        return -1

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player * board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert (len(pi) == self.n ** 2 + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        x = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                x += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return x

    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    def getScore(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)
        return b.countDiff(player)

    def draw_terminal(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        if valid_moves:
            return str([i for (i, valid) in enumerate(self.getValidMoves(board, 1)) if valid])
        else:
            horizontal_border = '+' + '-' * (4 * len(board[0]) - 1) + '+\n'
            output = horizontal_border

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

            '''column_letters = '|'
            for col in range(len(board[0])):
                column_letters += f' {chr(col + 65)} |'
            output += column_letters + '\n' + horizontal_border'''

            return output

    def draw(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        row_count = board.shape[0]
        col_count = board.shape[1]
        SQUARESIZE = 100
        WIDTH = col_count * SQUARESIZE
        HEIGHT = row_count * SQUARESIZE

        color_background = (252, 252, 244)  # cream
        color_grid = (172, 244, 230)  # light blue
        color_shadow = (50, 50, 50, 150)
        color_ply_one = (0, 0, 0)  # black
        color_ply_minus_one = (255, 255, 255)  # white
        color_valid = (144, 238, 144)  # turquoise

        pygame.init()

        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        surface.fill(color_background)

        for row in range(len(board)):
            for col in range(len(board[row])):
                center = (col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE // 2)
                radius = SQUARESIZE // 3

                pygame.draw.rect(surface, color_grid,
                                 (col * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE),
                                 1)  # show grid
                valids = self.getValidMoves(board, cur_player)
                if valid_moves and valids[(row * len(board[row])) + col]:
                    pygame.draw.circle(surface, color_valid,
                                       (col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE // 2),
                                       SQUARESIZE // 3)  # displaying valid moves
                if board[row][col] == 1:
                    pygame.draw.circle(surface, color_ply_one,
                                       (col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE // 2),
                                       SQUARESIZE // 3)
                elif board[row][col] == -1:
                    pygame.draw.circle(surface, color_ply_minus_one,
                                       (col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE // 2),
                                       SQUARESIZE // 3)
                    pygame.draw.arc(surface, (0, 0, 0),
                                    pygame.Rect(center[0] - radius, center[1] - radius, 2 * radius, 2 * radius),
                                    0, np.pi * 2, 1)
        return surface
