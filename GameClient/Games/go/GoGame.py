from Tools.Game_dev import IGame, np, pygame
from GoLogic import Board


class GoGame(IGame):
    """
    Go Game class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, size=None, np_pieces=None):
        self._base_board = Board(size, np_pieces)

    def getInitBoard(self):
        return self._base_board.np_pieces

    def getBoardSize(self):
        return (self._base_board.size, self._base_board.size)

    def getActionSize(self):
        return self._base_board.size * self._base_board.size + 1

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
        by_score = 0.5 * (board.size * board.size + board.komi)

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
        score_white = np.sum(board.np_pieces == -1)
        score_black = np.sum(board.np_pieces == 1)
        empties = zip(*np.where(board.np_pieces == 0))
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

        canonicalBoard.np_pieces= board.np_pieces * player

        # print('getting canon:')
        # print(b_pieces)
        return canonicalBoard

    # modified
    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.size**2 + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.size, self.size))
        l = []
        b_pieces = board.np_pieces
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
        return np.array(board.np_pieces).tostring()

    def stringRepresentation(self, board):
        return board.tostring()
    
    def draw_terminal(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        pass

    def draw(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
        pass

"""def display(board):
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

    print("   -----------------------")"""