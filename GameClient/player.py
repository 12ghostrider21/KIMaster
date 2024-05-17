import asyncio
from Tools.datatypes import EResponse


class Player:
    def __init__(self, game, game_client):
        self.game = game
        self.game_client = game_client
        self.move = None
        self.stop = False
        self.move_lock = asyncio.Lock()  # locks all variables inside the locked code block
        self.stop_lock = asyncio.Lock()  # locks all variables inside the locked code block
        self.player_pos = ""

    async def play(self, board):
        valid_moves = self.game.getValidMoves(board, 1)
        while True:
            async with self.stop_lock:
                if self.stop:
                    self.stop = False
                    return None
            async with self.move_lock:
                print("reached1")
                if self.move is not None:
                    print("reached2")
                    if valid_moves[self.move]:
                        tmp = self.move
                        self.move = None
                        await self.game_client.send_response(EResponse.SUCCESS, self.player_pos, "Valid move.")
                        break
                    else:
                        self.move = None
                        await self.game_client.send_response(EResponse.ERROR, self.player_pos, "Invalid move!")
            await asyncio.sleep(0.1)
        return tmp

    async def stop_game(self, flag: bool = True):
        async with self.stop_lock:
            self.stop = flag

    async def set_move(self, move, player_pos: str):
        async with self.move_lock:
            self.move = move
            self.player_pos = player_pos
