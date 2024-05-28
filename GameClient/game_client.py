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
from Tools.game_states import GAMESTATE
import pickle


class GameClient:
    @staticmethod
    def surface_to_png(img: surface) -> bytes:
        byte_io = io.BytesIO()
        image.save(img, byte_io, 'PNG')
        png_bytes = byte_io.getvalue()
        byte_io.close()
        return png_bytes

    def __init__(self, host: str, port: int, key: str):
        self.host: str = host
        self.port: int = port
        self.key: str = key
        self.pit: Pit | None = None
        self.websocket = None
        GameEnum.update(directory="Games")
        self.state: GAMESTATE = GAMESTATE.WAITING

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # network

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
        except ConnectionRefusedError:
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

    async def send_save(self, player_pos):
        save_file = pickle.dumps(self.pit.arena)
        await self.send_cmd("game_client", "save", {"player_pos": player_pos})
        await self.websocket.send(save_file)

    async def load_save(self):
        return pickle.loads(self.websocket.recv())

    async def send_cmd(self, command: str, command_key: str, data: dict | None = None):
        cmd = {"command": command, "command_key": command_key}
        if data is not None:
            cmd.update(data)
        cmd = json.dumps(cmd)
        await self.websocket.send(cmd)

    async def send_response(self, code: R_CODE, p_pos: str | None, data: dict = None):
        """
        :param code:
        :param p_pos: None is Broadcast on Socketserver
        :param data:
        :return:
        """
        cmd = {"response_code": code.value.code, "response_msg": code.value.msg, "player_pos": p_pos}
        if data is not None:
            cmd.update(data)
        cmd = json.dumps(cmd)
        await self.websocket.send(cmd)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # operation loop
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
            p_pos: str = read_object.get("player_pos")
            command_key: str = read_object.get("command_key")
            print(self.state, read_object)
            match self.state:
                case GAMESTATE.WAITING:
                    if command_key not in ["create", "evaluate", "quit", "games"]:
                        await self.send_response(R_CODE.P_NOINIT, p_pos)
                        continue
                    # create -> Running
                    # evaluate -> EVALUATE
                case GAMESTATE.RUNNING:
                    if command_key not in ["valid_moves", "make_move", "undo_move", "surrender", "blunder"]:
                        await self.send_response(R_CODE.P_STILLRUNNING, p_pos)
                        continue

                    # surrender -> FINISHED
                    # make_move (won or lost) -> FINISHED
                case GAMESTATE.FINISHED:
                    if command_key not in ["new_game", "timeline", "step", "unstep", "blunder", "quit", "create"]:
                        await self.send_response(R_CODE.P_GAMEOVER, p_pos)
                        continue
                    # new_game -> RUNNING

            match command_key:
                case "create":
                    if self.pit:
                        if self.pit.arena_task:
                            if not self.pit.arena_task.done():
                                await self.send_response(R_CODE.P_STILLRUNNING, p_pos)
                                continue
                    game_config: GameConfig = self.extract_game_config(read_object)
                    if not game_config():  # get new game_config and call check if correct
                        await self.send_response(R_CODE.P_ARGS, p_pos, {"game": read_object.get("game"),
                                                                        "mode": read_object.get("mode"),
                                                                        "difficulty": read_object.get("difficulty")})
                        continue
                    if not GameEnum.check_entry(game_config.game):
                        await self.send_response(R_CODE.P_GAMENOTAWAILABLE, p_pos,
                                                 {"game": game_config.game.game_name})
                        continue
                    self.pit = Pit(game_config, self)
                    response = await self.pit.init_game(num_games=1, game_config=game_config)
                    if response is None:
                        await self.send_response(R_CODE.INTERNALERROR, None)
                    await self.send_response(code=response.code, p_pos=None, data=response.data)
                    self.state = GAMESTATE.RUNNING
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "valid_moves":
                    pos = read_object.get("pos")
                    if pos:
                        try:
                            pos = int(pos)
                        except ValueError:
                            await self.send_response(R_CODE.P_INVALIDPOS, p_pos, {"pos": pos})
                            continue
                        if pos < 0:
                            await self.send_response(R_CODE.P_INVALIDPOS, p_pos)
                            continue
                    result = await self.pit.arena.draw_valid_moves(pos)
                    if result is None:
                        await self.send_response(R_CODE.P_INVALIDPOS, p_pos)
                        continue
                    img, representation = result
                    await self.send_response(R_CODE.P_MOVES, p_pos, {"moves": representation})
                    await self.send_image(img, p_pos)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "make_move":
                    move = read_object.get("move")
                    if move is None:
                        await self.send_response(R_CODE.P_NOMOVE, p_pos)
                        continue
                    move = self.parse_input(move)
                    if move is None:
                        await self.send_response(R_CODE.P_INVALIDMOVE, p_pos)
                        continue
                    print(f"Make move: {move=}")
                    await self.pit.set_move(move, p_pos)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "undo_move":
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(R_CODE.P_NOUNDO, p_pos)
                        continue
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(R_CODE.P_INVALIDUNDO, p_pos, {"num": num})
                        continue
                    if num <= 0:
                        await self.send_response(R_CODE.P_INVALIDUNDO, p_pos)
                        continue
                    if not self.pit.arena_task.done():
                        await self.pit.stop_play(p_pos)
                    response = await self.pit.arena.undo_move(num)
                    await self.send_response(response.code, p_pos)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "surrender":
                    await self.pit.stop_play(p_pos)
                    winner = -1 if p_pos == "p1" else 1  # winner is the opposite player of the one who surrenders
                    # p1 is 1 at arena, p2 is -1 at arena
                    await self.pit.arena_task
                    await self.send_response(R_CODE.P_SURRENDER, None, {"result": winner})
                    self.state = GAMESTATE.FINISHED
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "new_game":
                    if not self.pit.arena_task.done():
                        await self.send_response(R_CODE.P_STILLRUNNING, p_pos)
                        continue
                    response = await self.pit.init_game(num_games=1, game_config=self.pit.game_config)
                    if response is None:
                        await self.send_response(R_CODE.INTERNALERROR, None)
                    await self.send_response(code=response.code, p_pos=p_pos, data=response.data)
                    self.state = GAMESTATE.RUNNING
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "blunder":
                    blunder = await self.pit.arena.show_blunder(p_pos)
                    if len(blunder) == 0:
                        await self.send_response(R_CODE.P_BLUNDER, p_pos)
                    else:
                        await self.send_response(R_CODE.P_BLUNDERLIST, p_pos, {"blunder": blunder.__str__()})
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "timeline":
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(R_CODE.P_NOTIMELINE, p_pos)
                        continue
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(R_CODE.P_INVALIDTIMELINE, p_pos, {"num": num})
                        continue
                    if num < 0:
                        await self.send_response(R_CODE.P_INVALIDTIMELINE, p_pos)
                        continue
                    await self.handle_timeline(p_pos, "", num)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "step":
                    await self.handle_timeline(p_pos, "step")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "unstep":
                    await self.handle_timeline(p_pos, "unstep")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "games":
                    GameEnum.update(directory="Games")
                    data: dict = {e.game_name: GameEnum.check_entry(e) for e in GameEnum}
                    if data:
                        await self.send_response(R_CODE.P_GAMES, p_pos, data)
                    else:
                        await self.send_response(R_CODE.P_NOAVAILABLEGAMES, p_pos)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "evaluate":
                    if self.pit:
                        if self.pit.arena_task:
                            if not self.pit.arena_task.done():
                                await self.send_response(R_CODE.P_STILLRUNNING, p_pos)
                                continue
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(R_CODE.P_NOEVALUATION, p_pos)
                        continue
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(R_CODE.P_INVALIDEVALUATION, p_pos, {"num": num})
                        continue
                    if num == 1 or num > 100:
                        await self.send_response(R_CODE.P_INVALIDEVALUATION, p_pos)
                        continue
                    game_config: GameConfig = self.extract_game_config(read_object)
                    if not game_config():  # get new game_config and call check if correct
                        await self.send_response(R_CODE.P_ARGS, p_pos, {"game": read_object.get("game"),
                                                                        "mode": read_object.get("mode"),
                                                                        "difficulty": read_object.get("difficulty")})
                        continue

                    self.pit = Pit(game_config, self)
                    response = await self.pit.init_game(num_games=num, game_config=game_config)
                    if response is None:
                        await self.send_response(R_CODE.INTERNALERROR, None)
                    await self.send_response(code=response.code, p_pos=p_pos, data=response.data)
                    self.state = GAMESTATE.EVALUATE
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "stop_evaluate":
                    await self.pit.stop_play(p_pos)
                    await self.pit.arena_task
                    self.state = GAMESTATE.WAITING
                case _:
                    print(f"DEBUG: {command_key}")
            # update game_state value in lobby on every command
            print(self.state)
            await self.send_cmd("game_client", "state", {"state": self.state.name})
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
            await self.send_response(R_CODE.P_INVALIDTIMELINE, player_pos)
            return
        img, representation = result

        await self.send_response(R_CODE.P_TIMELINE, player_pos, {"representation": representation})
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
