from __future__ import print_function
import sys, os, datetime

sys.path.append('..')
from Tools.i_game import IGame, np
from Games.checkers.CheckersLogic import Board, Move

"""
Game class implementation for the game of Checkers (Russian variant).
"""


class CheckersGame(IGame):
    # input stack plain names
    __plain_names = ['own men', 'own kings', 'opponent''s men', 'opponent''s kings',
                     'long capture',
                     'no-progress count', 'king''s move count', 'repetition count']

    def __init__(self, height=None, width=None, win_length=None, np_pieces=None):
        # few methods of Board and Move support size=8 only
        self.n = 8

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board()
        return b
        #return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return Board.get_action_size()

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board(board)
        try:
            move = Move.parse_action(action)
        except:
            print(b.display())
            raise

        #if player == -1:
        #    move = move.clone().rotate()

        addedHalfMoves = b.execute_move(move, player)
        is_long_capture = addedHalfMoves == 0
        if is_long_capture:
            # the same player continues long capture
            return (b, player)
        # other player takes move 
        return (b, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()
        b = Board(board)
        legalMoves = b.get_legal_moves(player)
        board.legal_moves = b.legal_moves
        #display(board)
        #print("legalMoves = ", legalMoves)
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        moveIds = []
        for move in legalMoves:
            valids[move.move_id] = 1
            #if move.num_captures() > 3:
            #    print("move.num_captures: ", move.num_captures())
            assert move.move_id not in moveIds, "duplicated move_id detected: " + str(move) + "; " + str(legalMoves)
            moveIds.append(move.move_id)
        return np.array(valids)

    def getGameEnded(self, board, player):
        """ return 0 if not ended, 1 if the given player won, -1 if the given player lost, 0.0001 if the draw detected """
        b = board
        # draw has a very little value
        draw = 1e-4

        assert board.halfMoves < 1000, board.display() + " 1000 half-moves exceeded"

        result = b.get_game_result(player)
        if result != 0:
            return result
        #if b.is_win(-player):
        #    return -1
        # repetition rule
        if b.get_repetition_count() >= 3:
            #print("draw by repetitions: ", b.get_repetition_count())
            #b.display()
            #print("executed_moves: ", b.executed_moves)
            return draw
        # no-progress rules
        kingsOnBothSides = b.whiteKingCount > 0 and b.blackKingCount > 0
        if kingsOnBothSides:
            if b.count_pieces() <= 3:
                if b.noProgressCount / 2 >= 5:
                    #print("draw by no-progress: ", b.count_pieces(), " pieces :: ", b.noProgressCount/2, " move(s)")
                    return draw
            elif b.count_pieces() <= 5:
                if b.noProgressCount / 2 >= 30:
                    #print("draw by no-progress: ", b.count_pieces(), " pieces :: ", b.noProgressCount/2, " move(s)")
                    return draw
            elif b.count_pieces() <= 7:
                if b.noProgressCount / 2 >= 60:
                    #print("draw by no-progress: ", b.count_pieces(), " pieces :: ", b.noProgressCount/2, " move(s)")
                    return draw
        # 3 kings vs 1 king for 15 moves
        # TODO
        # kings only move for 15 moves
        if b.kingMoveCount / 2 >= 15:
            #print("draw by 15 king-moves: ", b.kingMoveCount, ", pieces:", b.count_pieces(), ", no-progress:", b.noProgressCount, " half-move(s)")
            return draw

        # TODO

        # continue the game
        return 0

    def getCanonicalForm(self, board, player) -> np.array:
        # return state if player==1, else return -state if player==-1
        #print("getCanonicalForm(), player: ", player)
        b = Board(board)
        b.pieces *= player

        if player == -1:
            #print("rotate90 x 2")
            b.pieces = np.rot90(b.pieces, 2)
            b.rotation = (board.rotation + 180) % 360
            if board.last_long_capture:
                b.last_long_capture = board.last_long_capture.clone().rotate()
            b.update_string_repr()

        #b.display()

        return b

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert (len(pi) == self.getActionSize())
        #pi_board = np.reshape(pi[:-1], (self.n, self.n))
        #l = []

        #for i in range(1, 5):
        #    for j in [True, False]:
        #        newB = np.rot90(board, i)
        #        newPi = np.rot90(pi_board, i)
        #        if j:
        #            newB = np.fliplr(newB)
        #            newPi = np.fliplr(newPi)
        #        l += [(newB, list(newPi.ravel()) + [pi[-1]])]

        # we apply no sym transformation
        image_stack = self.getImageStack(board)

        pi = np.copy(pi)
        l = [(image_stack, pi)]
        return l

    def stringRepresentation(self, board):
        return board.stringRepr

    def draw_terminal(self, board: np.array, valid_moves: bool, cur_player: int, *args: any):
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

    def getImageStackSize(self):
        """ Returns size of image stack that is used as input to NNet
            4 main images for pieces
            1 image for long_capture piece
            
            1 image for no-progress
            1 image for king-move-count 
            1 image for repetition-count            
            [x] half-moves plane is not used
            
        """
        return 8

    def getImageStack(self, board):
        """ Returns input stack for the given board
            [index of image] [description]
            [0] white men        bit map
            [1] white kings      bit map
            [2] black men        bit map
            [3] black kings      bit map
            [4] long_capture     bit map (one pixel on the given square)
            
            [5] no-progress              count
            [6] king's move count        count
            [7] repetition count         count
            [not used] [x] half moves    count
        """
        index = [None, 0, None, 1, 3, None, 2]  # indices of main plains
        # PLAYER = 4 # index of PLAYER's plain
        LONG_CAPTURE = 4  # index of LONG_CAPTURE's plain
        active_player = 1  # white always move
        # create image stack that will be an input to NNet 
        n = self.n
        main_planes = np.zeros(shape=(5, n, n), dtype=np.float32)
        # main images
        for y in range(n):
            for x in range(n):
                piece = board.pieces[x][y]
                if piece != 0:
                    main_planes[index[piece]][x][y] = 1
                # main_planes[PLAYER][x][y] = active_player

        # player/piece(s) making the move
        if board.last_long_capture:
            last = board.last_long_capture
            main_planes[LONG_CAPTURE][last.x1][last.y1] = 1

        # auxiliary images
        normNoProgressCount = board.noProgressCount / 128.0 if board.count_pieces() <= 7 else 0
        normKingMoveCount = board.kingMoveCount / 32.0
        normRepetitionCount = board.get_repetition_count() / 4.0

        no_progress = np.full((8, 8), normNoProgressCount, dtype=np.float32)
        king_move_count = np.full((8, 8), normKingMoveCount, dtype=np.float32)
        repetition_count = np.full((8, 8), normRepetitionCount, dtype=np.float32)
        auxiliary_planes = [no_progress, king_move_count, repetition_count]

        image_stack = np.asarray(auxiliary_planes, dtype=np.float32)
        image_stack = np.vstack((main_planes, auxiliary_planes))
        assert image_stack.shape == (self.getImageStackSize(), n, n)

        # debug image stack
        #if board.last_long_capture or board.kingMoveCount>0:
        #    self.print_image_stack(image_stack)

        return image_stack
