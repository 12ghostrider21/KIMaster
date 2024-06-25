from Tools.i_game import IGame, np
from Games.go.GoLogic import Board


class GoGame(IGame):
    """
    Go Game class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, size: int = None, pieces: np.array = None):
        self._base_board = Board(size, pieces)
        self.size = self._base_board.size
        self.pieces = self._base_board.pieces

    def getInitBoard(self):
        return self._base_board.pieces

    def getBoardSize(self):
        return (self.size, self.size)

    def getActionSize(self):
        return self.size * self.size + 1

    def getNextState(self, board: np.array, player: int, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        # print("getting next state from perspect of player {} with action {}".format(player,action))

        if action == self.size * self.size:
            return (board, -player)

        b = Board(self.size, np.copy(board))
        move = (int(action / self.size), action % self.size)
        # display(b)
        # print(player,move)
        b.execute_move(move, player)
        # display(b)
        return (b.pieces, -player)

    # modified
    def getValidMoves(self, board: np.array, player: int):
        # return a fixed size binary vector
        valids = [0 for _ in range(self.getActionSize())]
        b = Board(self.size, np.copy(board))
        legalMoves = b.get_legal_moves(player)
        # display(board)
        # print("legal moves{}".format(legalMoves))
        valids[-1] = 1
        if len(legalMoves) == 0:
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.size * x + y] = 1
        # display(b)
        # print(legalMoves)
        return np.array(valids)

    # modified
    def getGameEnded(self, board: np.array, player: int, returnScore: bool = False):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1

        b = Board(self.size, np.copy(board))
        winner = 0

        (score_black, score_white) = self.getScore(b)
        by_score = 0.5 * (b.size * b.size + b.komi)

        if len(b.history) > 1:
            if (b.history[-1] is None and b.history[-2] is None
                    and player == -1):
                if score_black > score_white:
                    winner = -1
                elif score_white > score_black:
                    winner = 1
                else:
                    # Tie
                    winner = 1e-4
            elif score_black > by_score or score_white > by_score:
                if score_black > score_white:
                    winner = -1
                elif score_white > score_black:
                    winner = 1
                else:
                    # Tie
                    winner = 1e-4
        if np.count_nonzero(b.pieces == 0) == 0:  # checking whether every field is occupied = game over
            if score_black > score_white:
                winner = -1
            elif score_white > score_black:
                winner = 1
            else:
                # Tie
                winner = 1e-4
        if returnScore:
            return winner,(score_black, score_white)
        return winner

    def getScore(self, board: Board):
        score_white = np.sum(board.pieces == -1)
        score_black = np.sum(board.pieces == 1)
        empties = zip(*np.where(board.pieces == 0))
        for empty in empties:
            # Check that all surrounding points are of one color
            if board.is_eyeish(empty, 1):
                score_black += 1
            elif board.is_eyeish(empty, -1):
                score_white += 1
        score_white += board.komi
        score_white -= board.passes_white
        score_black -= board.passes_black
        return (score_black, score_white)

    def getCanonicalForm(self, board: np.array, player: int):
        # return state if player==1, else return -state if player==-1
        return board * player

    # modified
    def getSymmetries(self, board: np.array, pi: np.array):
        # mirror, rotational
        assert(len(pi) == self.size**2 + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.size, self.size))
        l = []
        b_pieces = np.copy(board)
        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(b_pieces, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def translate(self, board: np.array, player: int, index: int):
        return index

    def stringRepresentation(self, board):
        return board.tostring()

    def draw_terminal(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        if valid_moves:
            return str([i for (i, valid) in enumerate(self.getValidMoves(board, 1)) if valid])
        else:
            horizontal_border = '\t+' + '-' * (4 * self.size - 1) + '+\n'
            output = horizontal_border

            for row in range(self.size):
                row_str = f'{row}\t|'
                for col in range(self.size):
                    piece = board[row][col]
                    if piece == 0:
                        row_str += '   |'
                    elif piece == 1:
                        row_str += ' O |'  # Assuming 'o' for black stone
                    elif piece == -1:
                        row_str += ' X |'  # Assuming 'x' for white stone
                output += row_str + '\n' + horizontal_border

            # Add column indices below the board
            col_indices = '\t  ' + '   '.join([f'{col}' for col in range(self.size)]) + '\n'
            output += col_indices

            return output

    def draw(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        import pygame
        row_count = self.size
        col_count = self.size
        SQUARESIZE = 90
        WIDTH = row_count * SQUARESIZE
        HEIGHT = col_count * SQUARESIZE
        MARGIN = SQUARESIZE // 2

        color_background = (251, 196, 103)  # light brown/cream
        color_grid = (0, 0, 0)  # black
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
