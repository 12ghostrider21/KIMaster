import ast

import numpy as np
from websockets import ConnectionClosedError

from GameClient.connection_manager import WebSocketConnectionManager
from GameClient.pit import Pit
from Tools.Game_Config.game_config import GameConfig
from Tools.rcode import RCODE
from Tools.dynamic_imports import Importer, ExcludeModule


class GameClient(WebSocketConnectionManager):
    def __init__(self, host: str, port: int, key: str):
        super().__init__(host, port, key)
        self.importer: Importer = Importer("../Games", ExcludeModule.LAMBDA, ExcludeModule.NNET)
        self.pit: Pit = Pit(self)

    async def run(self):
        await self.connect()
        while True:
            try:
                read_object: dict = await self.receive_json()
            except ConnectionClosedError:
                await self.close()
                break
            p_pos: str = read_object.get("p_pos")
            command_key: str = read_object.get("command_key")

            match command_key:
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "create":
                    if self.is_arena_running():
                        await self.send_response(code=RCODE.P_STILLRUNNING, to=p_pos)
                        continue
                    game_config: GameConfig = GameConfig.dict_to_config(read_object, self.importer.get_games())
                    if not game_config.ready():
                        await self.send_response(code=RCODE.P_ARGS, to=p_pos, data=game_config.to_dict())
                        continue
                    self.pit.init_arena(game_config)
                    self.start_arena()
                    await self.send_response(code=RCODE.P_ARENAINIT, to=p_pos, data=game_config.to_dict())
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "surrender":
                    if not self.is_arena_running():
                        await self.send_response(RCODE.P_NOTRUNNING, p_pos)
                    else:
                        self.stop_arena()
                        winner = -1 if p_pos == "p1" else 1  # winner is the opposite player of the one who surrenders
                        await self.send_response(RCODE.P_SURRENDER, None, {"result": winner})
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "valid_moves":
                    pos = read_object.get("pos")
                    if pos:
                        try:
                            pos = int(pos)
                        except ValueError:
                            await self.send_response(RCODE.P_INVALIDPOS, p_pos, {"pos": pos})
                            continue
                        if pos < 0:
                            await self.send_response(RCODE.P_INVALIDPOS, p_pos)
                            continue
                    hist: tuple = self.pit.get_last_hist_entry()
                    await self.send_board(hist[0], hist[1], self.pit.arena.game_name, True)
                    await self.send_response(RCODE.P_MOVES, pos,
                                             {"moves": self.pit.arena.game.getValidMoves(hist[0], hist[1]).tolist()})
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "make_move":
                    if not self.is_arena_running():
                        await self.send_response(RCODE.P_NOTRUNNING, p_pos)
                        continue    # Ignore moves if game is not running
                    move = read_object.get("move")
                    if move is None:
                        await self.send_response(RCODE.P_NOMOVE, p_pos)
                        continue
                    move = self.parse_input(move)
                    if move is None:
                        await self.send_response(RCODE.P_INVALIDMOVE, p_pos)
                        continue
                    self.pit.set_move(move, p_pos)
                    await self.send_response(RCODE.P_VALIDMOVE, p_pos)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "undo_move":
                    if not self.is_arena_running():
                        await self.send_response(RCODE.P_NOTRUNNING, p_pos)
                        continue
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(RCODE.P_NOUNDO, p_pos)
                        continue
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(RCODE.P_INVALIDUNDO, p_pos, {"num": num})
                        continue
                    if num <= 0:
                        await self.send_response(RCODE.P_INVALIDUNDO, p_pos)
                        continue
                    state, player, iteration = self.pit.undo(num)
                    if state is None or player is None or iteration is None:
                        await self.send_response(RCODE.P_NOUNDO, p_pos)
                        continue
                    self.stop_arena()
                    await self.send_response(RCODE.P_VALIDUNDO, p_pos)
                    self.start_arena(state, player, iteration)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "new_game":
                    if self.is_arena_running():
                        await self.send_response(RCODE.P_STILLRUNNING, p_pos)
                        continue
                    if self.pit.arena.game is None:
                        await self.send_response(RCODE.P_NOGAMEINIT, p_pos)
                        continue
                    self.pit.arena.history.clear()
                    self.start_arena()
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "blunder":
                    pass
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "timeline":
                    if self.is_arena_running():
                        await self.send_response(RCODE.P_STILLRUNNING, p_pos)
                        continue
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(RCODE.P_NOTIMELINE, p_pos)
                        continue
                    try:
                        num = int(num)
                    except ValueError:
                        await self.send_response(RCODE.P_INVALIDTIMELINE, p_pos, {"num": num})
                        continue
                    if num < 0:
                        await self.send_response(RCODE.P_INVALIDTIMELINE, p_pos)
                        continue
                    state, player, iteration = self.pit.timeline(p_pos, True, num)
                    await self.send_board(state, 1 if p_pos else -1, self.pit.arena.game_name, False)
                    await self.send_response(RCODE.P_TIMELINE, p_pos, {"current_player": player, "iteration": iteration})
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "step":
                    if self.is_arena_running():
                        await self.send_response(RCODE.P_STILLRUNNING, p_pos)
                        continue
                    state, player, iteration = self.pit.timeline(p_pos, True, None)
                    await self.send_board(state, 1 if p_pos else -1, self.pit.arena.game_name, True)
                    await self.send_response(RCODE.P_STEP, p_pos, {"current_player": player, "iteration": iteration})
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "unstep":
                    if self.is_arena_running():
                        await self.send_response(RCODE.P_STILLRUNNING, p_pos)
                        continue
                    state, player, iteration = self.pit.timeline(p_pos, False, None)
                    await self.send_board(state, 1 if p_pos else -1, self.pit.arena.game_name, True)
                    await self.send_response(RCODE.P_UNSTEP, p_pos, {"current_player": player, "iteration": iteration})
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case _:
                    await self.send_response(code=RCODE.COMMANDNOTFOUND, to=p_pos, data={"command_key": command_key})

    def start_arena(self, board: np.array = None, cur_player: int = 1, it: int = 0):
        self.pit.start_battle(board=board, cur_player=cur_player, it=it)

    def stop_arena(self):
        self.pit.stop_battle()

    def is_arena_running(self) -> bool:
        return self.pit.arena.running

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
