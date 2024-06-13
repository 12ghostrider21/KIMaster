import json
from abc import ABC

import numpy as np
from websockets import connect
from Tools.rcode import RCODE


class AbstractConnectionManager(ABC):
    def __init__(self, host: str, port: int, key: str):
        self.websocket = None
        self.uri: str = f"ws://{host}:{port}/game?&login={key}"
        self.key: str = key

    async def connect(self):
        print("connect")
        self.websocket = await connect(self.uri, ping_interval=None)

    async def receive_json(self):
        json_string = await self.websocket.recv()
        return json.loads(json_string)

    async def send_response(self, code: RCODE, to: str | None, data: dict = None):  # to user
        cmd = {"response": code.value, "to": to, "key": self.key}
        if data is not None:
            cmd.update(data)
        await self.websocket.send(json.dumps(cmd))

    async def send_cmd(self, command: str, command_key: str, p_pos: str | None, data: dict = None):  # to socket server
        cmd = {"command": command, "command_key": command_key, "to": p_pos, "key": self.key}
        if data is not None:
            cmd.update(data)
        await self.websocket.send(json.dumps(cmd))

    async def send_board(self, board: np.array, cur_player: int, game_name: str, valid: bool):
        cmd = {"command": "draw", "command_key": game_name, "to": "p1" if cur_player == 1 else "p2", "key": self.key,
               "board": board.tolist(), "cur_player": cur_player, "valid": valid}
        await self.websocket.send(json.dumps(cmd))

    async def broadcast_board(self, board: np.array, cur_player: int, game_name: str, valid: bool):
        cmd = {"command": "draw", "command_key": game_name, "to": None, "key": self.key,
               "board": board.tolist(), "cur_player": cur_player, "valid": valid}
        await self.websocket.send(json.dumps(cmd))

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            print("WebSocket connection closed")
