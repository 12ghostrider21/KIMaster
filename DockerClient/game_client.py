import asyncio
import json
import threading

import websockets
from starlette.websockets import WebSocket
from datatypes import RESPONSE, GameConfig, EGame, EGameMode, EDifficulty
from DockerClient.player import Player
import ast


class GameClient:
    def __init__(self, host: str, port: int, key: str):
        self.host: str = host
        self.port: int = port
        self.websocket = None
        self.key: str = key
        self.pit = None
        self.processed_lock = asyncio.Lock()
        self.processed = True
        self.player_pos: str = ""

    async def connect(self):
        url = f"ws://{self.host}:{self.port}/ws"
        try:
            self.websocket = await websockets.connect(url, ping_interval=None)
            await self.send_cmd("login", "", {"key": self.key})
            response = await self.receive_json()
            if response.get("response_code") == 200:
                return True
            return False
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
        cmd = json.dumps(cmd)
        await self.websocket.send(cmd)

    async def send_response(self, response_code: RESPONSE, response_msg: str | None = None,
                            data: dict | None = None):
        async with self.processed_lock:
            player_pos = self.player_pos
            self.processed = True
        cmd = {"response_code": response_code.value, "response_msg": response_msg, "player_pos": player_pos}
        if data is not None:
            cmd.update(data)
        cmd = json.dumps(cmd)
        await self.websocket.send(cmd)

    async def run(self):
        loop = await self.connect()
        while loop:
            command = await self.receive_json()
            player_pos = command.get("player_pos")
            async with self.processed_lock:
                self.processed = False
                self.player_pos = player_pos
            print(command)
            if command["command"] == "play":
                match command["command_key"]:
                    case "create":
                        from pit import Pit
                        game_config = self.extract_game_config(command)
                        self.pit = Pit(game_config, self)
                        await self.pit.init_game(num_games=1, game_config=game_config)
                    case "valid_moves":
                        pos = None
                        if "pos" in command:
                            pos = int(command["payload"]["pos"])
                        await self.pit.arena.draw_valid_moves(pos)
                    case "make_move":
                        move = self.parse_input(command["payload"]["move"])
                        await Player.set_move(move)
                    case "undo_move":
                        num = int(command["payload"]["num"])
                        await self.pit.arena.undo_move(num)
                        await Player.stop_game()
                    case "give_up":
                        await self.pit.arena.stop_game()
                        await Player.stop_game()
                        await self.send_response(RESPONSE.SUCCESS, "Successfully gave up")
                    case "quit":
                        # inject code to shut down docker container (and delete data)
                        await self.send_response(RESPONSE.SUCCESS, "Game quit")
                        break
                    case "new_game":
                        await self.pit.init_game(num_games=1, game_config=self.pit.game_config)
                    case "show_blunder":
                        await self.pit.arena.show_blunder()
                    case "timeline":
                        num = int(command["payload"]["num"])
                        await self.pit.arena.timeline(start_index=num)
                    case "step":
                        await self.pit.arena.timeline(step=True)
                    case "unstep":
                        await self.pit.arena.timeline(unstep=True)
                    case "evaluate":
                        game_config = self.extract_game_config(command)
                        num = int(command["payload"]["num"])
                        self.pit = Pit(game_config, self)
                        await self.pit.init_game(num_games=num, game_config=game_config)
                    case "stop_evaluate":
                        await self.pit.arena.stop_game()
                        await Player.stop_game()
                        await self.send_response(RESPONSE.SUCCESS, "Evaluation stopped")
            while True:
                async with self.processed_lock:
                    if self.processed:
                        break
                await asyncio.sleep(0.1)

            """
            # Send a message
            message = input("Type your message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
                
            await self.send_response(RESPONSE.SUCCESS, message)
            response = await self.receive_json()
            """
        await self.websocket.close()

    def extract_game_config(self, command):
        game = self.get_enum(EGame, command["payload"]["game"])
        mode = self.get_enum(EGameMode, command["payload"]["mode"])
        difficulty = self.get_enum(EDifficulty, command["payload"]["difficulty"])
        return GameConfig(game=game, mode=mode, difficulty=difficulty)

    def get_enum(self, enum_class, value):
        for enum_item in enum_class:
            if enum_item.value == value:
                return enum_item
        raise ValueError(f"No matching enum value found for {value}")

    def parse_input(self, input_str):
        if input_str.startswith("(") and input_str.endswith(")"):
            return ast.literal_eval(input_str)
        else:
            return int(input_str)
