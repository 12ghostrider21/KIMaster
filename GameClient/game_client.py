import ast
import numpy as np
from websockets import ConnectionClosedError

from GameClient.connection_manager import WebSocketConnectionManager
from GameClient.pit import Pit
from Tools.Game_Config.game_config import GameConfig
from Tools.rcode import RCODE
from Tools.dynamic_imports import Importer, ExcludeModule

# Constant to define the maximum number of evaluations
MAX_EVAL_NUM = 100


class GameClient(WebSocketConnectionManager):
    def __init__(self, host: str, port: int, key: str):
        """
        Initialize the GameClient with host, port, and key. It also initializes the Importer and Pit.
        """
        super().__init__(host, port, key)
        self.importer: Importer = Importer("../Games", ExcludeModule.MCTS)  # Importer for games excluding MCTS
        self.pit: Pit = Pit(self)  # Initialize the Pit object

    async def run(self):
        """
        Main loop to run the game client, handling incoming commands through a WebSocket connection.
        """
        await self.connect()  # Connect to the WebSocket server
        while True:
            try:
                read_object: dict = await self.receive_json()  # Await and receive a JSON object from the WebSocket
            except ConnectionClosedError:
                await self.close()  # Close the connection if there's an error
                break
            p_pos: str = read_object.get("p_pos")  # Get player position from the received JSON
            command_key: str = read_object.get("command_key")  # Get the command key from the received JSON

            match command_key:
                # Handling 'create' command
                case "create":
                    if self.is_arena_running():
                        await self.send_response(code=RCODE.P_STILLRUNNING, to=p_pos)
                        continue
                    game_config: GameConfig = GameConfig.dict_to_config(read_object, self.importer.get_games())
                    if not game_config.ready():
                        await self.send_response(code=RCODE.P_ARGS, to=p_pos, data=game_config.to_dict())
                        continue
                    self.pit.init_arena(game_config)  # Initialize arena with game configuration
                    self.pit.clear_arena()
                    self.start_arena()  # Start the arena
                    await self.send_response(code=RCODE.P_ARENAINIT, to=None, data=game_config.to_dict())
                    await self.update()  # Update the state

                # Handling 'surrender' command
                case "surrender":
                    if not self.is_arena_running():
                        await self.send_response(RCODE.P_NOTRUNNING, p_pos)
                    else:
                        self.stop_arena()  # Stop the arena
                        winner = -1 if p_pos == "p1" else 1  # Determine the winner based on who surrendered
                        last_it = self.pit.get_last_hist_entry()[2]
                        await self.send_response(RCODE.P_SURRENDER, None, {"result": winner,
                                                                           "turn": last_it})
                    await self.update()

                # Handling 'valid_moves' command
                case "valid_moves":
                    if not self.is_arena_running():
                        await self.send_response(RCODE.P_NOTRUNNING, p_pos)
                        continue
                    if self.pit.get_cur_player() != (1 if p_pos == "p1" else -1):
                        await self.send_response(RCODE.P_NOTYOURTURN, p_pos)
                        continue
                    hist: tuple = self.pit.get_last_hist_entry()  # Get the last history entry from the Pit
                    from_pos = read_object.get("fromPos")
                    if read_object.get("isFrontend") and p_pos == "p2":
                        from_pos = self.pit.arena.game.rotateMove(from_pos)
                    await self.send_board(hist[0], hist[1], self.pit.arena.game_name, True, from_pos)
                    moves = [self.pit.arena.game.translate(hist[0], hist[1], i)
                             for i, m in enumerate(self.pit.arena.game.getValidMoves(hist[0], hist[1])) if m == 1]
                    if read_object.get("isFrontend") and p_pos == "p2":
                        moves = str([self.pit.arena.game.rotateMove(move) for move in moves])
                    await self.send_response(RCODE.P_MOVES, p_pos, {"moves": moves})

                # Handling 'make_move' command
                case "make_move":
                    if not self.is_arena_running():
                        await self.send_response(RCODE.P_NOTRUNNING, p_pos)
                        continue  # Ignore moves if the game is not running
                    move = read_object.get("move")
                    if move is None:
                        await self.send_response(RCODE.P_NOMOVE, p_pos)
                        continue
                    if type(move) is list:
                        move = (move[0], move[1])
                    if type(move) is str:
                        move = self.parse_input(move)  # Parse the move input
                    if move is None:
                        await self.send_response(RCODE.P_INVALIDMOVE, p_pos)
                        continue
                    if read_object.get("isFrontend") and p_pos == "p2":
                        move = self.pit.arena.game.rotateMove(move)
                    if not self.pit.set_move(move, p_pos):
                        await self.send_response(RCODE.P_NOTYOURTURN, p_pos)

                # Handling 'undo_move' command
                case "undo_move":
                    if not self.is_arena_running():
                        await self.send_response(RCODE.P_NOTRUNNING, p_pos)
                        continue
                    if self.pit.get_cur_player() != (1 if p_pos == "p1" else -1):
                        await self.send_response(RCODE.P_NOTYOURTURN, p_pos)
                        continue
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(RCODE.P_NOUNDO, p_pos)
                        continue
                    try:
                        num = int(num)  # Validate the number of moves to undo
                    except ValueError:
                        await self.send_response(RCODE.P_INVALIDUNDO, p_pos, {"num": num})
                        continue
                    if num <= 0:
                        await self.send_response(RCODE.P_INVALIDUNDO, p_pos, {"num": num})
                        continue
                    if len(self.pit.arena.history) < 3:
                        await self.send_response(RCODE.P_NOUNDO, p_pos)
                        continue
                    while self.pit.arena.running:
                        self.stop_arena()
                    await self.send_response(RCODE.P_VALIDUNDO, p_pos)
                    state, player, it = self.pit.undo(num)  # Perform the undo operation
                    self.start_arena(state, player, it)

                # Handling 'new_game' command
                case "new_game":
                    if self.is_arena_running():
                        await self.send_response(RCODE.P_STILLRUNNING, p_pos)
                        continue
                    if self.pit.arena.game is None:
                        await self.send_response(RCODE.P_NOGAMEINIT, p_pos)
                        continue
                    self.pit.clear_arena()
                    self.start_arena()
                    await self.send_response(code=RCODE.P_ARENAINIT, to=None)
                    await self.update()  # Update the state

                # Handling 'blunder' command (currently not implemented)
                case "blunder":
                    # if arena is running -> break
                    if self.is_arena_running():
                        await self.send_response(RCODE.P_STILLRUNNING, p_pos)
                        continue
                    # if no action was played
                    if len(self.pit.arena.blunder_history) == 0:
                        await self.send_response(RCODE.P_NOBLUNDER, p_pos)
                        continue
                    # check if blunder gets updated from server
                    blunder = read_object.get("blunder")
                    if blunder is not None:
                        self.pit.set_blunder(blunder)
                        self.pit.arena.blunder_calculation = False  # blunder received deactivate function
                        # successfully requested blunder
                        await self.send_response(code=RCODE.P_BLUNDERLIST, to=p_pos, data=self.pit.get_blunder(p_pos))
                        continue
                    # only one create request of blunder possible
                    if self.pit.arena.blunder_calculation:
                        await self.send_response(code=RCODE.P_BLUNDER, to=p_pos)
                        continue
                    # request blunder create on first request
                    if len(self.pit.arena.blunder) == 0:
                        if read_object.get("isFrontend") and p_pos == "p2":
                            self.pit.arena.rotate = True
                        self.pit.arena.blunder_calculation = True
                        await self.send_response(code=RCODE.P_CREATEBLUNDER, to=p_pos)
                        await self.send_cmd(command="blunder", command_key=self.pit.arena.game_name,
                                            p_pos=p_pos, data=self.pit.get_blunder_payload())
                        continue
                    if read_object.get("isFrontend") and p_pos == "p2":
                        self.pit.arena.rotate = True
                    # successfully requested blunder
                    await self.send_response(code=RCODE.P_BLUNDERLIST, to=p_pos, data=self.pit.get_blunder(p_pos))

                # Handling 'timeline' command
                case "timeline":
                    if self.is_arena_running():
                        await self.send_response(RCODE.P_STILLRUNNING, p_pos)
                        continue
                    num = read_object.get("num")
                    if num is None:
                        await self.send_response(RCODE.P_NOTIMELINE, p_pos)
                        continue
                    try:
                        num = int(num)  # Validate the timeline input
                    except ValueError:
                        await self.send_response(RCODE.P_INVALIDTIMELINE, p_pos, {"num": num})
                        continue
                    if num < 0:
                        await self.send_response(RCODE.P_INVALIDTIMELINE, p_pos)
                        continue
                    state, player, it = self.pit.timeline(p_pos, True, num)
                    await self.send_board(state, 1 if p_pos == "p1" else -1, self.pit.arena.game_name,
                                          False, None)
                    await self.send_response(RCODE.P_TIMELINE, p_pos, {"current_player": player, "it": it})

                # Handling 'step' command
                case "step":
                    if self.is_arena_running():
                        await self.send_response(RCODE.P_STILLRUNNING, p_pos)
                        continue
                    state, player, it = self.pit.timeline(p_pos, True, None)
                    await self.send_board(state, 1 if p_pos == "p1" else -1, self.pit.arena.game_name,
                                          False, None)
                    data = {"current_player": player, "it": it, "last_it": len(self.pit.arena.history) - 1}
                    await self.send_response(RCODE.P_STEP, p_pos, data)

                # Handling 'unstep' command
                case "unstep":
                    if self.is_arena_running():
                        await self.send_response(RCODE.P_STILLRUNNING, p_pos)
                        continue
                    state, player, it = self.pit.timeline(p_pos, False, None)
                    await self.send_board(state, 1 if p_pos == "p1" else -1, self.pit.arena.game_name,
                                          False, None)
                    data = {"current_player": player, "it": it, "last_it": len(self.pit.arena.history) - 1}
                    await self.send_response(RCODE.P_UNSTEP, p_pos, data)

                # Handling extern request of current game image
                case "image":
                    if self.pit.arena.running:
                        if self.pit.arena.board is not None:
                            await self.broadcast_board(board=self.pit.arena.board,
                                                       cur_player=self.pit.arena.cur_player,
                                                       game_name=self.pit.arena.game_name,
                                                       valid=False)

                # Handling unknown commands
                case _:
                    await self.send_response(code=RCODE.COMMANDNOTFOUND, to=p_pos, data={"command_key": command_key})
            await self.update()

    def start_arena(self, board: np.array = None, cur_player: int = 1, it: int = 0):
        """
        Start the game arena with optional initial board state, current player, and iteration.
        """
        self.pit.start_battle(board=board, cur_player=cur_player, it=it)

    def stop_arena(self):
        """
        Stop the game arena.
        """
        self.pit.stop_battle()

    def is_arena_running(self) -> bool:
        """
        Check if the arena is currently running.
        """
        return self.pit.arena.running

    async def update(self):
        """
        Send an update command to the WebSocket server with the current game state.
        """
        await self.send_cmd("update", "", None,
                            {"key": self.key,
                             "game_running": self.is_arena_running()})

    @staticmethod
    def parse_input(input_str: str):
        """
        Parse the input string to convert it into an appropriate format (integer or tuple).
        """
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
