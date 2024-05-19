import json
import ast
from enum import Enum
import websockets
from websockets import ConnectionClosedError
from starlette.websockets import WebSocketDisconnect

from player import Player
from pit import Pit
from game_config import GameConfig, EGame, EGameMode, EDifficulty
from e_response import EResponse
import asyncio

import os


class GameClient:
    def __init__(self, host: str, port: int, key: str):
        self.host: str = host
        self.port: int = port
        self.key: str = key
        self.websocket = None
        self.pit: Pit | None = None

    async def connect(self):
        url = f"ws://{self.host}:{self.port}/ws"
        print(f"Socket URL: {url}")
        try:
            self.websocket = await websockets.connect(url, ping_interval=None)
            await self.send_cmd("login", "", {"key": self.key})
            response = await self.receive_json()
            if response.get("response_code") == 200:
                print("Connected!")
                return True
            print("Login failed!", response)
            return False
        except ConnectionRefusedError as e:
            print(f"Can not connect to SocketServer with: {url}. Closing")
            return False

    async def receive_json(self):
        json_string = await self.websocket.recv()
        return json.loads(json_string)

    async def send_image(self, img: bytes, player_pos: str):
        await self.send_cmd("img", "", {"player_pos": player_pos})
        await self.websocket.send(img)

    async def broadcast_image(self, img1: bytes, img2: bytes):
        await self.send_cmd("img", "broadcast")
        await self.websocket.send(img1)
        await self.websocket.send(img2)

    async def send_cmd(self, command: str, command_key: str, data: dict | None = None):
        cmd = {"command": command, "command_key": command_key}
        if data is not None:
            cmd.update(data)
        cmd = json.dumps(cmd)
        await self.websocket.send(cmd)

    async def send_response(self, response_code: EResponse,
                            p_pos: str | None,
                            response_msg: str | None = None,
                            data: dict | None = None):
        cmd = {"response_code": response_code.value, "response_msg": response_msg, "player_pos": p_pos}
        if data is not None:
            cmd.update(data)
        cmd = json.dumps(cmd)
        await self.websocket.send(cmd)

    async def run(self):
        loop = await self.connect()
        while loop:
            try:
                read_object: dict = await self.receive_json()
            except json.decoder.JSONDecodeError:
                await self.send_response(EResponse.ERROR, "Received data is not a correct json!")
                continue
            except WebSocketDisconnect:
                break
            except ConnectionClosedError:
                print("Server closed!")
                break
            player_pos: str = read_object.get("player_pos")
            command_key: str | None = read_object.get("command_key")
            if self.pit is None and command_key not in ["create", "evaluate"]:
                await self.send_response(EResponse.ERROR, player_pos, "You need to create a game first!")
                continue
            match command_key:
                case "create":
                    if self.pit:
                        if self.pit.arena_task:
                            if not self.pit.arena_task.done():
                                await self.send_response(EResponse.ERROR, player_pos, "Game still running. "
                                                                                      "Please surrender first")
                                continue
                    game_config: GameConfig = self.extract_game_config(read_object)
                    if not game_config():  # get new game_config and call check if correct
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Arguments are missing or invalid!",
                                                 {"game": read_object.get("game"),
                                                  "mode": read_object.get("mode"),
                                                  "difficulty": read_object.get("difficulty")})
                        continue
                    self.pit = Pit(game_config, self)
                    response = await self.pit.init_game(num_games=1, game_config=game_config)
                    await self.send_response(response_code=response.response_code,
                                             p_pos=player_pos,
                                             response_msg=response.response_msg,
                                             data=response.data)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "valid_moves":
                    pos = read_object.get("pos")
                    if pos:
                        try:
                            pos = int(pos)
                        except ValueError:
                            await self.send_response(EResponse.ERROR, player_pos, f"Pos: '{pos}' is not a pos!",
                                                     {"pos": pos})
                            continue
                        if pos < 0:
                            await self.send_response(EResponse.ERROR, player_pos,
                                                     "Pos must be greater than or equal to 0!")
                            continue
                    result = await self.pit.arena.draw_valid_moves(pos)
                    if result is None:
                        await self.send_response(EResponse.ERROR, player_pos, "Invalid from_pos!")
                        continue
                    img, representation = result
                    await self.send_response(EResponse.SUCCESS, player_pos, "Valid moves:", {"moves": representation})
                    await self.send_image(img, player_pos)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "make_move":
                    move = read_object.get("move")
                    if move is None:
                        await self.send_response(EResponse.ERROR, player_pos, "'move' entry not set!")
                        continue
                    move = self.parse_input(move)
                    if move is None:
                        await self.send_response(EResponse.ERROR, player_pos, "Invalid move!")
                        continue
                    await self.pit.set_move(move, player_pos)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "undo_move":
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(EResponse.ERROR, player_pos, "Amount of undo not declared!")
                        continue
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(EResponse.ERROR, player_pos, f"num: '{num}' is not an int!",
                                                 {"num": num})
                        continue
                    if num <= 0:
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Amount of moves to be undone must be greater than 0!")
                        continue
                    await self.pit.stop_play(player_pos)
                    await self.pit.arena.undo_move(num)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "surrender":
                    await self.pit.stop_play(player_pos)
                    winner = -1 if player_pos == "p1" else 1  # winner is the opposite player of the one who surrenders
                    # p1 == 1 ; p2 == -1 at arena
                    await self.pit.arena_task
                    await self.send_response(EResponse.SUCCESS, None, "Game over: ",
                                             {"result": winner})
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "quit":
                    if not self.pit.arena_task.done():
                        await self.send_response(EResponse.ERROR, player_pos, "Game still running. "
                                                                              "Please surrender first")
                    await self.send_response(EResponse.SUCCESS, player_pos, "Game quit.")
                    # inject code to shut down docker container (and delete data)
                    break
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "new_game":
                    await self.pit.set_move(None, player_pos)  # if a move was set in Player after game over
                    # otherwise Player.play is called, move not None => automatically returned and executed
                    if not self.pit.arena_task.done():
                        await self.send_response(EResponse.ERROR, player_pos, "Game still running. "
                                                                              "Please surrender first")
                        continue
                    response = await self.pit.init_game(num_games=1, game_config=self.pit.game_config)
                    await self.send_response(response_code=response.response_code,
                                             p_pos=player_pos,
                                             response_msg=response.response_msg,
                                             data=response.data)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "blunder":
                    blunder = await self.pit.arena.show_blunder(player_pos)
                    if len(blunder) == 0:
                        await self.send_response(EResponse.SUCCESS, player_pos, "No obvious blunder.")
                    else:
                        await self.send_response(EResponse.SUCCESS, player_pos,
                                                 "Current blunder list:",
                                                 {"blunder": blunder.__str__()})
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "timeline":
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(EResponse.ERROR, player_pos, "Timeline start index not declared!")
                        continue
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(EResponse.ERROR, player_pos, f"num: '{num}' is not an int!",
                                                 {"num": num})
                        continue
                    if num < 0:
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Index must be greater than or equal to 0!")
                        continue
                    await self.handle_timeline(player_pos, "", num)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "step":
                    await self.handle_timeline(player_pos, "step")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "unstep":
                    await self.handle_timeline(player_pos, "unstep")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "evaluate":
                    if self.pit:
                        if self.pit.arena_task:
                            if not self.pit.arena_task.done():
                                await self.send_response(EResponse.ERROR, player_pos, "Game still running. "
                                                                                      "Please surrender first")
                                continue
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Num of games for evaluation not declared!")
                        continue
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(EResponse.ERROR, player_pos, f"num: '{num}' is not an int!",
                                                 {"num": num})
                        continue
                    if num == 1 or num > 100:
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Not 1 or more than 100 games supported at evaluation!")
                        continue
                    game_config: GameConfig = self.extract_game_config(read_object)
                    if not game_config():  # get new game_config and call check if correct
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Arguments are missing!",
                                                 {"game": read_object.get("game"),
                                                  "mode": read_object.get("mode"),
                                                  "difficulty": read_object.get("difficulty")})
                        continue

                    self.pit = Pit(game_config, self)
                    response = await self.pit.init_game(num_games=num, game_config=game_config)
                    await self.send_response(response_code=response.response_code,
                                             p_pos=player_pos,
                                             response_msg=response.response_msg,
                                             data=response.data)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "stop_evaluate":
                    await self.pit.stop_play(player_pos)
                    await self.pit.arena_task
        await self.websocket.close()

    async def handle_timeline(self, player_pos: str, step: str, *args: int):
        if args and isinstance(args[0], int):  # initial timeline start with timeline index
            result = await self.pit.arena.timeline(start_index=args[0])
        else:
            if step == "step":
                result = await self.pit.arena.timeline(step=True)
            elif step == "unstep":
                result = await self.pit.arena.timeline(unstep=True)
        if result is None:
            await self.send_response(EResponse.ERROR, player_pos, "Invalid timeline index!")
            return
        img, representation = result

        await self.send_response(EResponse.SUCCESS, player_pos, "", {"board": representation})
        await self.send_image(img, player_pos)

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

    def parse_input(self, input_str: str):
        if input_str is None:
            return None
        if isinstance(input_str, int):
            return input_str
        if input_str.startswith("(") and input_str.endswith(")"):
            try:
                result = ast.literal_eval(input_str)
                return result
            except ValueError:
                return None
        else:
            try:
                return int(input_str)
            except ValueError:
                return None
