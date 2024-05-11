import asyncio
from DockerClient import IGame
from Datatypes import RESPONSE


class Player:
    def __init__(self, game: IGame, game_client):
        self.game = game
        self.game_client = game_client

    move = None
    stop = False
    move_lock = asyncio.Lock()  # locks all variables inside the locked code block (cls.move)
    stop_lock = asyncio.Lock()  # locks all variables inside the locked code block (cls.stop)

    async def play(self, board):
        valid_moves = self.game.getValidMoves(board, 1)
        while True:
            async with Player.stop_lock:
                if Player.stop:
                    Player.stop = False
                    return None
            async with Player.move_lock:
                if Player.move is not None:
                    if valid_moves[Player.move]:
                        tmp = Player.move
                        Player.move = None
                        await self.game_client.send_response(RESPONSE.SUCCESS, "Valid move")
                        break
                    else:
                        Player.move = None
                        await self.game_client.send_cmd("play", "make_move", {"response_code": RESPONSE.ERROR,
                                                                              "response_msg": "Invalid move"})
            await asyncio.sleep(0.1)
        return tmp

    @classmethod
    async def stop_game(cls, flag: bool = True):
        async with cls.stop_lock:
            cls.stop = flag

    @classmethod
    async def set_move(cls, move):
        async with cls.move_lock:
            cls.move = move
