from Tools.i_game import IGame, np
from Games.go.GoLogic import Board


class GoGame(IGame):
    def __init__(self, n=19):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return b

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n * self.n + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        # print("getting next state from perspect of player {} with action {}".format(player,action))

        b = board.copy()
        if action == self.n * self.n:
            return (b, -player)

        move = (int(action / self.n), action % self.n)
        # display(b)
        # print(player,move)
        b.execute_move(move,player)
        # display(b)
        return (b, -player)

    # modified
    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0 for i in range(self.getActionSize())]
        b = board.copy()
        legalMoves = b.get_legal_moves(player)
        # display(board)
        # print("legal moves{}".format(legalMoves))
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n * x + y] = 1
        # display(b)
        # print(legalMoves)
        return np.array(valids)

    # modified
    def getGameEnded(self, board, player,returnScore=False):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1

        winner = 0
        (score_black, score_white) = self.getScore(board)
        by_score = 0.5 * (board.n*board.n + board.komi)

        if len(board.history) > 1:
            if (board.history[-1] is None and board.history[-2] is None\
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
        if returnScore:
            return winner,(score_black, score_white)
        return winner

    def getScore(self, board):
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

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        canonicalBoard=board.copy()

        canonicalBoard.pieces= board.pieces* player

        # print('getting canon:')
        # print(b_pieces)
        return canonicalBoard

    # modified
    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2 + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []
        b_pieces = board.pieces
        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(b_pieces, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return np.array(board.pieces).tostring()

    def translate(self, board: np.array, player: int, index: int):
            return index

    def stringRepresentation(self, board):
        return board.tostring()

    def drawTerminal(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
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
                        row_str += ' O |'  # Assuming 'O' for black stone
                    elif piece == -1:
                        row_str += ' X |'  # Assuming 'X' for white stone
                output += row_str + '\n' + horizontal_border

            # Add column indices below the board
            col_indices = '\t  ' + '   '.join([f'{col}' for col in range(10)])
            col_indices += '   ' + '  '.join([f'{col}' for col in range(10, self.size)]) + '\n'
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


def display(board):
    b_pieces = np.array(board.pieces)

    n = b_pieces.shape[0]

    for y in range(n):
        print(y, "|", end="")
    print("")
    print(" -----------------------")
    for y in range(n):
        print(y, "|", end="")    # print the row #
        for x in range(n):
            piece = b_pieces[y][x]    # get the piece to print
            if piece == 1:
                print("b ", end="")
            elif piece == -1:
                print("W ", end="")
            else:
                if x == n:
                    print("-", end="")
                else:
                    print("- ", end="")
        print("|")

    print("   -----------------------")