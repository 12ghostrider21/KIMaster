import asyncio
import json
from enum import Enum

import websockets
from websockets import ConnectionClosedError

from GameClient.player import Player
from GameClient.pit import Pit
from starlette.websockets import WebSocketDisconnect
from Tools.datatypes import EResponse, GameConfig, EGame, EGameMode, EDifficulty
import ast

from Tools.i_game import IGame


class GameClient:
    def __init__(self, host: str, port: int, key: str):
        self.host: str = host
        self.port: int = port
        self.key: str = key
        self.websocket = None
        self.pit: Pit | None = None
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
            print("Login failed!", response)
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

    async def send_response(self, response_code: EResponse, p_pos: str, response_msg: str | None = None,
                            data: dict | None = None):
        #async with self.processed_lock:
        #    player_pos = self.player_pos
        #    self.processed = True
        cmd = {"response_code": response_code.value, "response_msg": response_msg, "player_pos": p_pos}
        if data is not None:
            cmd.update(data)
        cmd = json.dumps(cmd)
        await self.websocket.send(cmd)

    async def run(self):
        loop = await self.connect()
        while loop:
            try:
                readObject: dict = await self.receive_json()
            except json.decoder.JSONDecodeError:
                await self.send_response(EResponse.ERROR, "Received data is not a correct json!")
                continue
            except WebSocketDisconnect:
                break
            except ConnectionClosedError:
                print("Server closed!")
                break
            player_pos: str = readObject.get("player_pos")
            command: str | None = readObject.get("command")
            command_key: str | None = readObject.get("command_key")
            if self.pit is None and command_key != "create":
                await self.send_response(EResponse.ERROR, player_pos, "You need to create a Game first!")
                continue



        #while loop:
            #command = await self.receive_json()

            #async with self.processed_lock:
            #    self.processed = False
            #    self.player_pos = player_pos
            #print(command)

            match command_key:
                case "create":
                    game_config: GameConfig = self.extract_game_config(readObject)
                    if not game_config():  # get new game_config and call check if correct
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Arguments are missing!",
                                                 {"game": readObject.get("game"),
                                                  "mode": readObject.get("mode"),
                                                  "difficulty": readObject.get("difficulty")})
                        continue
                    self.pit = Pit(game_config, self)
                    response = self.pit.init_game(num_games=1, game_config=game_config)
                    await self.send_response(response_code=response.response_code,
                                             p_pos=player_pos,
                                             response_msg=response.response_msg,
                                             data=response.data)
                case "show_blunder":
                    blunder = await self.pit.arena.show_blunder()
                    if len(blunder) == 0:
                        await self.send_response(EResponse.ERROR, player_pos,"Blunder is empty!")
                    else:
                        await self.send_response(EResponse.SUCCESS, player_pos,
                                                 "Current blunder list.",
                                                 {"blunder": blunder.__str__()})
            continue


        """
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

            
            # Send a message
            message = input("Type your message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
                
            await self.send_response(RESPONSE.SUCCESS, message)
            response = await self.receive_json()
            
        await self.websocket.close()"""

    def extract_game_config(self, command: dict) -> GameConfig:
        c_game = self.get_enum(EGame, command.get("game"))
        c_mode = self.get_enum(EGameMode, command.get("mode"))
        c_difficulty = self.get_enum(EDifficulty, command.get("difficulty"))
        return GameConfig(game=c_game, mode=c_mode, difficulty=c_difficulty)

    def get_enum(self, enum_class, value: str) -> Enum | None:
        if value is None:
            return None
        for enum_item in enum_class:
            if enum_item.name.lower() == value.lower():
                return enum_item
        return None

    def parse_input(self, input_str):
        if input_str.startswith("(") and input_str.endswith(")"):
            return ast.literal_eval(input_str)
        else:
            return int(input_str)
