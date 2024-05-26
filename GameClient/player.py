import asyncio
from Tools.Response import *


class Player:
    def __init__(self, game, game_client, eval: bool = False, ):
        self.game = game
        self.game_client = game_client
        self.move = None
        self.stop = False
        self.move_lock = asyncio.Lock()  # locks all variables inside the locked code block
        self.stop_lock = asyncio.Lock()  # locks all variables inside the locked code block
        self.player_pos = ""
        self.eval = eval

    async def play(self, board):
        valid_moves = self.game.getValidMoves(board, 1)
        while True:
            async with self.stop_lock:
                if self.stop:
                    self.stop = False
                    return None
            async with self.move_lock:
                if self.move is not None:
                    if self.move >= len(valid_moves):
                        self.move = None
                        if not self.eval:
                            await self.game_client.send_response(R_CODE.P_INVALIDMOVE, self.player_pos, "Invalid move!")
                    elif valid_moves[self.move]:
                        tmp = self.move
                        self.move = None
                        if not self.eval:
                            await self.game_client.send_response(R_CODE.P_VALIDMOVE, self.player_pos, "Valid move.")
                        break
                    else:
                        self.move = None
                        if not self.eval:
                            await self.game_client.send_response(R_CODE.P_INVALIDMOVE, self.player_pos, "Invalid move!")
            await asyncio.sleep(0.025)
        return tmp

    async def stop_play(self, flag: bool = True):
        async with self.stop_lock:
            self.stop = flag

    async def set_move(self, move, player_pos: str):
        async with self.move_lock:
            self.move = move
            self.player_pos = player_pos
