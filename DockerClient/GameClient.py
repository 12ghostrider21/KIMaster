import asyncio
import json
import threading

import websockets
from starlette.websockets import WebSocket
from Datatypes import RESPONSE


class GameClient:
    def __init__(self, host: str, port: int, key: str):
        self.host: str = host
        self.port: int = port
        self.websocket = None
        self.key: str = key
        self.pit = None

    async def connect(self):
        url = f"ws://{self.host}:{self.port}/ws"
        try:
            self.websocket = await websockets.connect(url, ping_interval=None)
        except ConnectionRefusedError as e:
            print(f"Can not connect to SocketServer with: {url}. Closing")
            return False

    async def receive_json(self):
        json_string = await self.websocket.recv()
        return json.loads(json_string)

    async def send_image(self, img_p1: bytes, img_p2: bytes):
        await self.send_cmd("client", "img")
        await self.websocket.send(img_p1)
        await self.websocket.send(img_p2)

    async def send_cmd(self, command: str, command_key: str, data: dict | None = None):
        cmd = {"command": command, "command_key": command_key}
        if data is not None:
            cmd.update(data)
        await self.websocket.send(cmd)

    async def send_response(self, response_code: RESPONSE, response_msg: str, data: dict | None = None):
        cmd = {"response_code": response_code.value, "response_msg": response_msg}
        if data is not None:
            cmd.update(data)
        await self.websocket.send(cmd)

    async def run(self):
        loop = await self.connect()
        while loop:
            command = await self.receive_json()
            if command["command"] == "play":
                match command["command_key"]:
                    case "create":
                        game_config = command["data"]["game_config"]
                        self.pit.init_game(game_config, num_games=1)
                    case "valid_moves":
                        pos = None
                        if "data" in command:
                            pos = command["data"]["pos"]
                        self.pit.arena.draw_valid_moves(pos)
                    case "make_move":
                        move = command["data"]["move"]
                        self.pit.Player.set_move(move)
                    case "undo_move":
                        num = command["data"]["num"]
                        self.pit.arena.undo_move(num)
                        self.pit.Player.stop_game()
                    case "give_up":
                        self.pit.arena.stop_game()
                        self.pit.Player.stop_game()
                        await self.send_response(RESPONSE.SUCCESS, "Successfully gave up")
                    case "quit":
                        # inject code to shut down docker container (and delete data)
                        await self.send_response(RESPONSE.SUCCESS, "Game quit")
                        break
                    case "new_game":
                        self.pit.init_game(self.pit.game_config, num_games=1)
                    case "show_blunder":
                        self.pit.arena.show_blunder()
                    case "timeline":
                        num = command["data"]["num"]
                        self.pit.arena.timeline(start_index=num)
                    case "step":
                        self.pit.arena.timeline(step=True)
                    case "unstep":
                        self.pit.arena.timeline(unstep=True)
                    case "evaluate":
                        game_config = command["data"]["game_config"]
                        num = command["data"]["num"]
                        self.pit.init_game(game_config, num_games=num)
                    case "stop_evaluate":
                        self.pit.arena.stop_game()
                        self.pit.Player.stop_game()
                        await self.send_response(RESPONSE.SUCCESS, "Evaluation stopped")

            """
            # Send a message
            message = input("Type your message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
                
            await self.send_response(RESPONSE.SUCCESS, message)
            response = await self.receive_json()
            """
        await self.websocket.close()
