import json
import numpy as np
import websockets
from abc import ABC
from Tools.rcode import RCODE


class WebSocketConnectionManager(ABC):
    def __init__(self, host: str, port: int, key: str):
        self.connection = None
        self.uri: str = f"ws://{host}:{port}/game?&login={key}"
        self.key: str = key

    async def connect(self):
        print("Connecting...")
        try:
            self.connection = await websockets.connect(uri=self.uri, ping_interval=None)
            print("Connected!")
        except ConnectionRefusedError:
            print(f"Connection failed to: '{self.uri}'")
            exit(1)

    async def receive_json(self):
        return json.loads(await self.connection.recv())

    async def send_response(self, code: RCODE, to: str | None, data: dict = None):
        cmd = {"response": code.value, "to": to, "key": self.key}
        if data is not None:
            cmd.update(data)
        await self.__send_json(json.dumps(cmd))

    async def send_cmd(self, command: str, command_key: str, p_pos: str | None, data: dict = None):  # to socket server
        cmd = {"command": command, "command_key": command_key, "to": p_pos, "key": self.key}
        if data is not None:
            cmd.update(data)
        await self.__send_json(json.dumps(cmd))

    async def send_board(self, board: np.array, cur_player: int, game_name: str, valid: bool, from_pos: int | None):
        cmd = {"command": "draw", "command_key": game_name, "to": "p1" if cur_player == 1 else "p2", "key": self.key,
               "board": board.tolist(), "cur_player": cur_player, "valid": valid, "from_pos": from_pos}
        await self.__send_json(json.dumps(cmd))

    async def broadcast_board(self, board: np.array, cur_player: int, game_name: str, valid: bool):
        cmd = {"command": "draw", "command_key": game_name, "to": None, "key": self.key,
               "board": board.tolist(), "cur_player": cur_player, "valid": valid}
        await self.__send_json(json.dumps(cmd))

    async def close(self):
        if self.connection:
            await self.connection.close()
            print("WebSocket connection closed")

    async def __send_json(self, obj: json):
        await self.connection.send(obj)
