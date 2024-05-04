import numpy as np
from Network import GameClient
import asyncio

from Player import Player


class RandomPlayer(Player):
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a


class Connect4Player(Player):
    def __init__(self, game):
        self.game = game

    move = None
    stop_game = False

    async def play(self, board):
        valid_moves = self.game.getValidMoves(board, 1)

        while True:
            # move = int(input())
            if self.stop_game:
                break
            if self.move is not None:
                if valid_moves[self.move]:
                    self.move = None
                    break
                else:
                    print('Invalid move')  # send method
            await asyncio.sleep(0.1)
        if self.stop_game:
            stop_game = False
            return -1  # does not matter, even though in further games it may might be 2 ints (from, to)
        return self.move

    @staticmethod
    def stop_game(flag: bool = True):
        stop_game = flag

    @staticmethod
    def set_move(m):
        move = m

class OneStepLookaheadConnect4Player(Player):
    """Simple player who always takes a win if presented, or blocks a loss if obvious, otherwise is random."""
    def __init__(self, game, verbose=True):
        self.game = game
        self.player_num = 1
        self.verbose = verbose

    def play(self, board):
        valid_moves = self.game.getValidMoves(board, self.player_num)
        win_move_set = set()
        fallback_move_set = set()
        stop_loss_move_set = set()
        for move, valid in enumerate(valid_moves):
            if not valid: continue
            if self.player_num == self.game.getGameEnded(*self.game.getNextState(board, self.player_num, move)):
                win_move_set.add(move)
            if -self.player_num == self.game.getGameEnded(*self.game.getNextState(board, -self.player_num, move)):
                stop_loss_move_set.add(move)
            else:
                fallback_move_set.add(move)

        if len(win_move_set) > 0:
            ret_move = np.random.choice(list(win_move_set))
            if self.verbose: print('Playing winning action %s from %s' % (ret_move, win_move_set))
        elif len(stop_loss_move_set) > 0:
            ret_move = np.random.choice(list(stop_loss_move_set))
            if self.verbose: print('Playing loss stopping action %s from %s' % (ret_move, stop_loss_move_set))
        elif len(fallback_move_set) > 0:
            ret_move = np.random.choice(list(fallback_move_set))
            if self.verbose: print('Playing random action %s from %s' % (ret_move, fallback_move_set))
        else:
            raise Exception('No valid moves remaining: %s' % self.game.stringRepresentation(board))

        return ret_move
