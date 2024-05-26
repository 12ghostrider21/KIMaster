import io
import json
import ast
from enum import Enum

from pygame import surface, image
import websockets
from websockets import ConnectionClosedError
from starlette.websockets import WebSocketDisconnect
from pit import Pit

from Tools.Game_Config import GameConfig, EGameMode, EDifficulty, GameEnum
from Tools.Response import R_CODE


class GameClient:
    def __init__(self, host: str, port: int, key: str):
        self.host: str = host
        self.port: int = port
        self.key: str = key
        self.pit: Pit | None = None
        self.websocket = None
        GameEnum.update(directory="Games")

    @staticmethod
    def surface_to_png(img: surface) -> bytes:
        byte_io = io.BytesIO()
        image.save(img, byte_io, 'PNG')
        png_bytes = byte_io.getvalue()
        byte_io.close()
        return png_bytes

    async def connect(self):
        url = f"ws://{self.host}:{self.port}/ws"
        print(f"Socket URL: {url}")
        try:
            self.websocket = await websockets.connect(url, ping_interval=None)
            await self.send_cmd("login", "", {"key": self.key})
            response = await self.receive_json()
            if response.get("response_code") == 101:
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

    async def send_image(self, img: surface, player_pos: str):
        await self.send_cmd("img", "", {"player_pos": player_pos})
        await self.websocket.send(self.surface_to_png(img))

    async def broadcast_image(self, img1: surface, img2: surface):
        await self.send_cmd("img", "broadcast")
        await self.websocket.send(self.surface_to_png(img1))
        await self.websocket.send(self.surface_to_png(img2))

    async def send_cmd(self, command: str, command_key: str, data: dict | None = None):
        cmd = {"command": command, "command_key": command_key}
        if data is not None:
            cmd.update(data)
        cmd = json.dumps(cmd)
        await self.websocket.send(cmd)

    async def send_response(self, response_code: R_CODE,
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
                await self.send_response(R_CODE.NONVALIDJSON, "Received data is not correct json!")
                continue
            except WebSocketDisconnect:
                break
            except ConnectionClosedError:
                print("Server closed!")
                break
            player_pos: str = read_object.get("player_pos")
            command_key: str | None = read_object.get("command_key")
            if self.pit is None and command_key not in ["create", "evaluate", "quit"]:
                await self.send_response(R_CODE.P_NOINIT, player_pos, "You need to create a game first!")
                continue
            if self.pit:
                if self.pit.arena_task:
                    if self.pit.arena_task.done() and command_key in ["valid_moves", "make_move", "surrender"]:
                        await self.send_response(R_CODE.P_NOINIT, player_pos, "You need to create a game first!")
                        continue

            match command_key:
                case "create":
                    if self.pit:
                        if self.pit.arena_task:
                            if not self.pit.arena_task.done():
                                await self.send_response(R_CODE.P_STILLRUNNING, player_pos,
                                                         "Game still running. Please surrender first!")
                                continue
                    game_config: GameConfig = self.extract_game_config(read_object)
                    if not game_config():  # get new game_config and call check if correct
                        await self.send_response(R_CODE.P_ARGS, player_pos,
                                                 "Arguments are missing or invalid!",
                                                 {"game": read_object.get("game"),
                                                  "mode": read_object.get("mode"),
                                                  "difficulty": read_object.get("difficulty")})
                        continue
                    self.pit = Pit(game_config, self)
                    response = await self.pit.init_game(num_games=1, game_config=game_config)
                    if response is None:
                        await self.send_response(R_CODE.INTERNALERROR, None, "Internal error occurred")
                    await self.send_response(response_code=response.response_code,
                                             p_pos=None,
                                             response_msg=response.response_msg,
                                             data=response.data)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "valid_moves":
                    pos = read_object.get("pos")
                    if pos:
                        try:
                            pos = int(pos)
                        except ValueError:
                            await self.send_response(R_CODE.P_INVALIDPOS, player_pos,
                                                     f"Pos: '{pos}' is not a pos!",
                                                     {"pos": pos})
                            continue
                        if pos < 0:
                            await self.send_response(R_CODE.P_INVALIDPOS, player_pos,
                                                     "Pos must be greater than or equal to 0!")
                            continue
                    result = await self.pit.arena.draw_valid_moves(pos)
                    if result is None:
                        await self.send_response(R_CODE.P_INVALIDPOS, player_pos, "Invalid from_pos!")
                        continue
                    img, representation = result
                    await self.send_response(R_CODE.P_MOVES, player_pos, "Valid moves:",
                                             {"moves": representation})
                    await self.send_image(img, player_pos)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "make_move":
                    move = read_object.get("move")
                    if move is None:
                        await self.send_response(R_CODE.P_NOMOVE, player_pos, "'move' entry not set!")
                        continue
                    move = self.parse_input(move)
                    if move is None:
                        await self.send_response(R_CODE.P_INVALIDMOVE, player_pos, "Invalid move!")
                        continue
                    print(move)
                    await self.pit.set_move(move, player_pos)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "undo_move":
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(R_CODE.P_NOUNDO, player_pos,
                                                 "Amount of moves to be undone not declared!")
                        continue
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(R_CODE.P_INVALIDUNDO, player_pos,
                                                 f"Num: '{num}' is not an int!",
                                                 {"num": num})
                        continue
                    if num <= 0:
                        await self.send_response(R_CODE.P_INVALIDUNDO, player_pos,
                                                 "Amount of moves to be undone must be greater than 0!")
                        continue
                    if not self.pit.arena_task.done():
                        await self.pit.stop_play(player_pos)
                    response = await self.pit.arena.undo_move(num)
                    await self.send_response(response.response_code, player_pos, response.response_msg)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "surrender":
                    await self.pit.stop_play(player_pos)
                    winner = -1 if player_pos == "p1" else 1  # winner is the opposite player of the one who surrenders
                    # p1 is 1 at arena, p2 is -1 at arena
                    await self.pit.arena_task
                    await self.send_response(R_CODE.P_SURRENDER, None, "Game over:",
                                             {"result": winner})
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "quit":
                    if not self.pit.arena_task.done():
                        await self.send_response(R_CODE.P_STILLRUNNING, player_pos,
                                                 "Game still running. Please surrender first!")
                        continue
                    await self.send_response(R_CODE.P_QUIT, player_pos, "Game quit.")
                    break
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "new_game":
                    if not self.pit.arena_task.done():
                        await self.send_response(R_CODE.P_STILLRUNNING, player_pos,
                                                 "Game still running. Please surrender first!")
                        continue
                    response = await self.pit.init_game(num_games=1, game_config=self.pit.game_config)
                    if response is None:
                        await self.send_response(R_CODE.INTERNALERROR, None, "Internal error occurred")
                    await self.send_response(response_code=response.response_code,
                                             p_pos=player_pos,
                                             response_msg=response.response_msg,
                                             data=response.data)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "blunder":
                    blunder = await self.pit.arena.show_blunder(player_pos)
                    if len(blunder) == 0:
                        await self.send_response(R_CODE.P_BLUNDER, player_pos, "No obvious blunder.")
                    else:
                        await self.send_response(R_CODE.P_BLUNDERLIST, player_pos,
                                                 "Blunder list (index, move):",
                                                 {"blunder": blunder.__str__()})
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "timeline":
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(R_CODE.P_NOTIMELINE, player_pos,
                                                 "Timeline start index not declared!")
                        continue
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(R_CODE.P_INVALIDTIMELINE, player_pos,
                                                 f"Index: '{num}' is not an int!",
                                                 {"num": num})
                        continue
                    if num < 0:
                        await self.send_response(R_CODE.P_INVALIDTIMELINE, player_pos,
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
                                await self.send_response(R_CODE.P_STILLRUNNING, player_pos,
                                                         "Game still running. Please surrender first!")
                                continue
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(R_CODE.P_NOEVALUATION, player_pos,
                                                 "Num of games at evaluation not declared!")
                        continue
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(R_CODE.P_INVALIDEVALUATION, player_pos,
                                                 f"Num: '{num}' is not an int!",
                                                 {"num": num})
                        continue
                    if num == 1 or num > 100:
                        await self.send_response(R_CODE.P_INVALIDEVALUATION, player_pos,
                                                 "1 or more than 100 games not supported at evaluation!")
                        continue
                    game_config: GameConfig = self.extract_game_config(read_object)
                    if not game_config():  # get new game_config and call check if correct
                        await self.send_response(R_CODE.P_ARGS, player_pos,
                                                 "Arguments are missing!",
                                                 {"game": read_object.get("game"),
                                                  "mode": read_object.get("mode"),
                                                  "difficulty": read_object.get("difficulty")})
                        continue

                    self.pit = Pit(game_config, self)
                    response = await self.pit.init_game(num_games=num, game_config=game_config)
                    if response is None:
                        await self.send_response(R_CODE.INTERNALERROR, None, "Internal error occurred")
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
        result = None
        if args and isinstance(args[0], int):  # initial timeline start with timeline index
            result = await self.pit.arena.timeline(start_index=args[0])
        else:
            if step == "step":
                result = await self.pit.arena.timeline(step=True)
            elif step == "unstep":
                result = await self.pit.arena.timeline(unstep=True)
        if result is None:
            await self.send_response(R_CODE.P_INVALIDTIMELINE, player_pos, "Invalid timeline index!")
            return
        img, representation = result

        await self.send_response(R_CODE.P_TIMELINE, player_pos, "", {"representation": representation})
        await self.send_image(img, player_pos)

    def extract_game_config(self, command: dict) -> GameConfig:
        c_game = GameEnum.get(command.get("game"))
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
