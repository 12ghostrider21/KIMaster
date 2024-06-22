import asyncio
from typing import Callable

import numpy as np

from Tools.i_game import IGame
from Tools.rcode import RCODE


class Arena:
    def __init__(self, game_client):
        self.game_client = game_client  # need to send information over websocket connection
        self.running: bool = False  # var to stop battle if necessary
        self.time_line_index_p1: int = 0
        self.time_line_index_p2: int = 0

        # configuration storage of current active battle
        self.history: list = []  # [board, cur_player, iteration]
        self.game: IGame | None = None
        self.game_name: str = ""
        self.player1 = None
        self.player2 = None

    def set_arena(self, game: IGame, game_name: str, play1: Callable, play2: Callable):
        self.game = game
        self.game_name = game_name
        self.player1 = play1
        self.player2 = play2
        self.history.clear()    # reset history on new game configuration

    async def play(self, board: np.array = None, cur_player: int = 1, it: int = 0):
        self.running = True

        # initialisation of game
        if board is None:
            board = self.game.getInitBoard()
        players = [self.player2, None, self.player1]  # array of play functions

        while self.running and self.game.getGameEnded(board, cur_player) == 0:
            await asyncio.sleep(0.0001)  # is needed because of optimiser!
            self.history.append([board, cur_player, it])
            await self.game_client.broadcast_board(board, cur_player, self.game_name, False)

            p = players[cur_player + 1]
            canonical_board = self.game.getCanonicalForm(board, cur_player)
            valids = self.game.getValidMoves(canonical_board, 1)
            if not any(valids[:-1]):  # check if a valid move is possible
                self.running = False
                winner = -1 if cur_player == "p1" else 1  # winner is the opposite player of the one who surrenders
                await self.game_client.send_response(code=RCODE.P_NOVALIDMOVES, to=None,
                                                     data={"result": winner})
                continue
            to = "p1" if cur_player == 1 else "p2"
            action = None
            while self.running:
                await asyncio.sleep(0.0001)  # is needed because of optimiser!
                action = p()    # action can be (None) no move set, (int, tuple) on play action, (bool) ai_move request
                if action is None:
                    continue
                if isinstance(action, bool):  # do a request to server with ai move
                    await self.game_client.send_cmd(command="ai_move", command_key=self.game_name, p_pos=to,
                                                    data={"board": board.tolist(),
                                                          "cur_player": cur_player,
                                                          "it": it,
                                                          "key": self.game_client.key})
                    continue
                if action >= len(valids):
                    await self.game_client.send_response(code=RCODE.P_INVALIDMOVE, to=to)
                    continue
                if valids[action]:
                    print(f"Valid ACTION of: {to}", action)
                    break
                await self.game_client.send_response(code=RCODE.P_INVALIDMOVE, to=to)
            if self.running:
                board, cur_player = self.game.getNextState(board, cur_player, action)
                it += 1

        if self.running:
            await self.game_client.broadcast_board(board, cur_player, self.game_name, False)
            await self.game_client.send_response(RCODE.P_GAMEOVER, None,
                                                 {"result": round(
                                                     cur_player * self.game.getGameEnded(board, cur_player)),
                                                     "turn": it})
        self.time_line_index_p1 = len(self.history)  # update index to history length
        self.time_line_index_p2 = len(self.history)  # update index to history length

    def stop(self):
        self.running = False
