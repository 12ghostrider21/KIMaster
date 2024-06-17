import ast

from websockets.exceptions import ConnectionClosedError

from GameClient.connection_manager import AbstractConnectionManager
from GameClient.pit import Pit
from Tools.Game_Config.game_config import GameConfig
from Tools.rcode import RCODE
from Tools.dynamic_imports import Importer, ExcludeModule


class GameClient(AbstractConnectionManager):
    def __init__(self, host: str, port: int, key: str):
        super().__init__(host, port, key)
        self.pit: Pit = Pit(self)

    async def run(self):
        await self.connect()
        self.pit.game_classes = Importer("/app/Games", ExcludeModule.NNET, ExcludeModule.LAMBDA).get_games()
        while True:
            try:
                read_object: dict = await self.receive_json()
            except ConnectionClosedError:
                await self.close()
                break
            p_pos: str = read_object.get("p_pos")
            command_key: str = read_object.get("command_key")

            match command_key:
                case "create":
                    if self.pit.arena_task is not None:
                        await self.send_response(code=RCODE.P_STILLRUNNING, to=p_pos)
                        continue
                    game_config: GameConfig = GameConfig.dict_to_config(read_object)
                    if not game_config.ready():
                        await self.send_response(code=RCODE.P_ARGS, to=p_pos, data=game_config.to_dict())
                        continue
                    if game_config.game.lower() not in self.pit.game_classes.keys():
                        await self.send_response(code=RCODE.P_GAMENOTAVAILABLE, to=p_pos, data=game_config.to_dict())
                        continue
                    self.pit.init_arena(game_config)
                    await self.send_response(code=RCODE.P_ARENAINIT, to=p_pos, data=game_config.to_dict())
                    self.pit.start_game(None, 1, 0)
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
                    hist: list = self.pit.arena.get_last_board()
                    await self.send_board(hist[0], hist[1], self.pit.arena.game_name, True)
                    await self.send_response(RCODE.P_MOVES, pos)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                case "make_move":
                    if self.pit.arena_task is None:
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
                case "surrender":
                    self.pit.stop_arena()
                    winner = -1 if p_pos == "p1" else 1  # winner is the opposite player of the one who surrenders
                    await self.send_response(RCODE.P_SURRENDER, None, {"result": winner})
                case "undo_move":
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
                    self.pit.stop_arena()
                    board, cur_player, it = self.pit.arena.undo_move(num)
                    self.pit.start_game(board, cur_player, it)
                    await self.send_response(RCODE.P_VALIDUNDO, p_pos)
                case _:
                    await self.send_response(code=RCODE.COMMANDNOTFOUND, to=p_pos, data={"command_key": command_key})

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
