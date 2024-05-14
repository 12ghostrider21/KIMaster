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

    async def connect(self):
        url = f"ws://{self.host}:{self.port}/ws"
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
            if self.pit is None and command_key != "create":
                await self.send_response(EResponse.ERROR, player_pos, "You need to create a game first!")
                continue
            match command_key:
                case "create":
                    game_config: GameConfig = self.extract_game_config(read_object)
                    if not game_config():  # get new game_config and call check if correct
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Arguments are missing!",
                                                 {"game": read_object.get("game"),
                                                  "mode": read_object.get("mode"),
                                                  "difficulty": read_object.get("difficulty")})
                        continue
                    self.pit = Pit(game_config, self)
                    response = self.pit.init_game(num_games=1, game_config=game_config)
                    await self.send_response(response_code=response.response_code,
                                             p_pos=player_pos,
                                             response_msg=response.response_msg,
                                             data=response.data)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "valid_moves":
                    pos = read_object.get("pos")
                    if pos is None:
                        await self.send_response(EResponse.ERROR, player_pos, "'pos' entry not set!")
                        continue
                    try:
                        pos = int(pos)
                    except ValueError:
                        await self.send_response(EResponse.ERROR, player_pos, f"Pos: '{pos}' is not a pos!", {"pos": pos})
                        continue
                    if pos < 0:
                        await self.send_response(EResponse.ERROR, player_pos, "Pos must be greater than or equal to 0")
                        continue
                    representation = await self.pit.arena.draw_valid_moves(pos)
                    await self.send_response(EResponse.SUCCESS, player_pos, "Valid moves.", {"moves": representation})
                    continue
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "show_blunder":
                    blunder = await self.pit.arena.show_blunder()
                    if len(blunder) == 0:
                        await self.send_response(EResponse.SUCCESS, player_pos, "No obvious blunder!")
                    else:
                        await self.send_response(EResponse.SUCCESS, player_pos,
                                                 "Current blunder list.",
                                                 {"blunder": blunder.__str__()})
                    continue
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "make_move":
                    move = read_object.get("move")
                    if move is None:
                        await self.send_response(EResponse.ERROR, player_pos, "'move' entry not set!")
                        continue
                    move = self.parse_input(move)
                    await Player.set_move(move)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "undo_move":
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(EResponse.ERROR, player_pos, "Amount of undo not declared!")
                        continue
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(EResponse.ERROR, player_pos, f"num: '{num}' is not a int!", {"num": num})
                        continue
                    if num <= 0:
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Amount of moves to be undone must be greater than 0")
                        continue
                    await self.pit.arena.undo_move(num)
                    await Player.stop_game()
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "give_up":
                    await self.pit.arena.stop_game()
                    await Player.stop_game()
                    await self.send_response(EResponse.SUCCESS, player_pos, "Successfully gave up")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "quit":
                    await self.send_response(EResponse.SUCCESS, player_pos, "Game quit")
                    # inject code to shut down docker container (and delete data)
                    break
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "new_game":
                    response = self.pit.init_game(num_games=1, game_config=self.pit.game_config)
                    await self.send_response(response_code=response.response_code,
                                             p_pos=player_pos,
                                             response_msg=response.response_msg,
                                             data=response.data)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "show_blunder":
                    blunder = await self.pit.arena.show_blunder()
                    if len(blunder) == 0:
                        await self.send_response(EResponse.SUCCESS, player_pos, "No obvious blunder")
                    else:
                        await self.send_response(EResponse.SUCCESS, player_pos,
                                                 "Current blunder list",
                                                 {"blunder": blunder.__str__()})
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "timeline":
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(EResponse.ERROR, player_pos, "Start index not declared")
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(EResponse.ERROR, player_pos, f"num: '{num}' is not a int!", {"num": num})
                        continue
                    if num < 0:
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Index must be greater than or equal to 0")
                        continue
                    await self.pit.arena.timeline(start_index=num)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "step":
                    await self.pit.arena.timeline(step=True)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "unstep":
                    await self.pit.arena.timeline(unstep=True)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "evaluate":
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Num of games for evaluation not declared")
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(EResponse.ERROR, player_pos, f"num: '{num}' is not a int!", {"num": num})
                        continue
                    if num > 100:
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Not more than 100 games supported at evaluation")
                    game_config: GameConfig = self.extract_game_config(read_object)
                    if not game_config():  # get new game_config and call check if correct
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Arguments are missing!",
                                                 {"game": read_object.get("game"),
                                                  "mode": read_object.get("mode"),
                                                  "difficulty": read_object.get("difficulty")})
                        continue
                    mode = game_config.mode
                    if mode != "playerai_vs_ai":
                        await self.send_response(EResponse.ERROR, player_pos,
                                                 "Only mode 'playerai_vs_ai' supported")

                    self.pit = Pit(game_config, self)
                    response = self.pit.init_game(num_games=1, game_config=game_config)
                    await self.send_response(response_code=response.response_code,
                                             p_pos=player_pos,
                                             response_msg=response.response_msg,
                                             data=response.data)
                case "stop_evaluate":
                    await self.pit.arena.stop_game()
                    await Player.stop_game()
                    await self.send_response(EResponse.SUCCESS, player_pos, "Evaluation stopped")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        await self.websocket.close()

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
        # @ make it save
        if input_str is None:
            return None
        if isinstance(input_str, int):
            return input_str
        if input_str.startswith("(") and input_str.endswith(")"):
            return ast.literal_eval(input_str)
        else:
            return int(input_str)
