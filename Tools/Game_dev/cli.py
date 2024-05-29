import json
import websockets
import asyncio
from enum import Enum


class Play:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.websocket = None
        self.game_config: dict = {}

    async def main(self):
        connected = await self.connect()
        if not connected:
            return
        await self.run()
        await self.websocket.close()
        print("\nConnection to server closed.\n")
        print("Thank you for using our service!\n")
        return

    async def run(self):
        while True:
            success = await self.init_game()
            if success:
                while True:
                    await self.play()
                    await self.handle_blunder()
                    await self.handle_timeline()
                    user_input = input("\nDo you want to play another game? (y/<some_other_key>)\n").lower()
                    if user_input == "y":
                        user_input = input("\nSame configuration? (y/<some_other_key>)\n"
                                           "If you want to play another game, mode, difficulty, "
                                           "press '<some_other_key>'\n").lower()
                        if user_input == "y":
                            continue
                        else:
                            break
                    else:
                        return
            else:
                return

    async def init_game(self):
        while True:
            is_joining = input("\nWould you like to join a lobby? (y/n):\n"
                               "(press 'q' to quit)\n").lower()
            if is_joining == "y":
                while True:
                    lobby_key = input("\nPlease insert your lobby key:\n"
                                      "(return to base selection by typing 'r')\n")
                    if lobby_key == "r":
                        break
                    join_cmd = Command.join.value
                    join_cmd.update({"key": lobby_key})
                    pos = input(
                        "\nPlease choose your position (p1/p2/sp):\n"
                        "[p1 = player1, p2 = player2, sp = spectator]\n"
                        "(return to base selection by typing 'r')\n")
                    if lobby_key == "r":
                        break
                    join_cmd.update({"pos": pos})
                    await self.send_cmd(join_cmd)
                    response = await self.get_response_timeout(101)  # "lobby joined"
                    if response:
                        print('\n' + str(response) + '\n')
                        response = await self.get_response(
                            200)  # "game initialized"; waiting for the host to hit "play"
                        if response:
                            print('\n' + str(response) + '\n')
                        return True
            elif is_joining == "n":
                while True:
                    is_eval = input("\nWould you like to evaluate your own AI / regular algorithm? (y/n):\n"
                                    "(return to base selection by typing 'r')\n").lower()
                    match is_eval:
                        case "y":
                            await self.init_lobby()
                            await asyncio.sleep(1)
                            config = await self.select_config(is_eval=True)
                            if config is None:  # means user_input was 'r'
                                await self.send_cmd(Command.leave.value)
                                continue
                            config.update({"mode": "playerai_vs_ai"})
                            while True:
                                user_input = input("\nHow many games shall your AI / algorithm play?\n"
                                                   "(return to intermediate selection by typing 'r')\n").lower()
                                if user_input == "r":
                                    break
                                elif isinstance(user_input, int):
                                    num_games = int(user_input)
                                    config.update({"num": num_games})
                                    self.game_config = config
                                    await asyncio.sleep(1)
                                    print("Spectators can join subsequently.\n")

                                    eval_cmd = Command.evaluate.value
                                    eval_cmd.update(self.game_config)

                                    await self.send_cmd(eval_cmd)
                                    response = await self.get_response_timeout(201)  # "evaluation runs"
                                    print('\n' + str(response) + '\n')
                                    return True
                                else:
                                    continue
                        case "n":  # initializing standard non evaluation game
                            await self.init_lobby()
                            await asyncio.sleep(1)
                            config = await self.select_config(is_eval=False)
                            if config is None:  # means user_input was 'r'
                                await self.send_cmd(Command.leave.value)
                                continue
                            self.game_config = config
                            while True:
                                user_input = input("\nEveryone joined the lobby? (press 'y' if so):\n"
                                                   "(Spectators can join subsequently.)\n"
                                                   "(return to intermediate selection by typing 'r')\n").lower()
                                match user_input:
                                    case "y":
                                        create_game_cmd = Command.create_game.value
                                        create_game_cmd.update(self.game_config)
                                        await self.send_cmd(create_game_cmd)
                                        response = await self.get_response_timeout(200)
                                        print('\n' + str(response) + '\n')  # "game initialized"
                                        return True
                                    case "r":
                                        await self.send_cmd(Command.leave.value)
                                        break
                                    case _:
                                        continue
                        case "r":
                            break
                        case _:
                            continue

            elif is_joining == "q":
                return False
            else:
                continue

    async def init_lobby(self):
        await self.send_cmd(Command.create_lobby.value)
        response = await self.receive_json()  # lobby created
        if response:
            print('\n' + str(response) + '\n')
            print("Others can join.\n")

    async def select_config(self, is_eval: bool) -> dict | None:
        config = {}
        options = ["game", "difficulty"]
        if not is_eval:
            options.insert(1, "mode")

        for i in options:
            while True:
                user_input = input(f"Which {i} do you want to play?:\n"
                                   "(return to intermediate selection by typing 'r')\n").lower()
                if user_input == "r":
                    return None
                elif user_input not in getattr(Config, i):  # invalid input
                    print("\nPlease choose from the following:\n")
                    print(str(getattr(Config, i)) + '\n')
                else:
                    break
            config.update({i: user_input})
        return config

    async def play(self):
        match self.game_config.get("mode"):
            case "player_vs_player":
                await self.handle_player_vs_player()
            case "player_vs_ai":
                await self.handle_player_vs_ai()
            case "playerai_vs_ai":
                await self.handle_playerai_vs_ai()
            case "playerai_vs_playerai":
                await self.handle_playerai_vs_playerai()

    async def handle_player_vs_player(self):
        await self.game_loop("\nIf you want to surrender at some point, press 'q'\n",
                             ai_player=False,
                             ai_enemy=False,
                             display=True)

    async def handle_player_vs_ai(self):
        await self.game_loop("\nIf you want to surrender at some point, press 'q'\n",
                             ai_player=False,
                             ai_enemy=True,
                             display=True)

    async def handle_playerai_vs_ai(self):
        # from <own_ai_make_move_directory> import MakeMoveClass
        if self.game_config.get("num"):  # case evaluation
            await self.game_loop("\nTo stop evaluation earlier and display intermediate results, press 'q'\n",
                                 ai_player=True,
                                 ai_enemy=True,
                                 display=False)
        else:  # case regular game
            await self.game_loop("\nIf you want to surrender at some point, press 'q'\n",
                                 ai_player=True,
                                 ai_enemy=True,
                                 display=True)

    async def handle_playerai_vs_playerai(self):
        await self.game_loop("\nIf you want to surrender at some point, press 'q'\n",
                             ai_player=True,
                             ai_enemy=True,
                             display=True)

    async def game_loop(self, message: str, ai_player: bool, ai_enemy: bool, display: bool, ):
        user_input = asyncio.create_task(self.console_input(message))
        while True:
            response = await self.receive_json()
            if user_input.done():
                user_input = user_input.result().lower()
                if user_input == "q":
                    if display:
                        await self.send_cmd(Command.surrender.value)
                        response = await self.get_response_timeout(210)  # surrender
                    else:
                        await self.send_cmd(Command.stop_evaluate.value)
                        response = await self.get_response_timeout(203)  # evaluation finished
                    if response:
                        print('\n' + str(response) + '\n')
                    return
                else:
                    if display:
                        user_input = asyncio.create_task(self.console_input(""))
                    else:
                        user_input = asyncio.create_task(self.console_input("\nTo stop evaluation earlier and display "
                                                                            "intermediate results, press 'q'\n"))
            if int(response.get("response_code")) == 205:  # board
                board = response.get("board")
                if ai_player:
                    move = "0"  # dummy
                    # move = <own_make_move_method(board)>  # replace with AI / algorithm that calculates move
                    success = await self.exec_move(move)
                    if not success:
                        print(f"\nError: Invalid move!\nMove: {move}\nGame is shutting down.\n")
                        if display:
                            await self.send_cmd(Command.surrender.value)
                        else:
                            await self.send_cmd(Command.stop_evaluate.value)

                        return
                else:  # human player
                    while True:
                        message = "\nPlease insert your move:\n" \
                                  "(show valid moves by typing 'v')\n"
                        if ai_enemy:
                            message += "(undo move by typing 'u')\n"
                        move = input(message).lower()
                        match move:
                            case "v":
                                await self.send_cmd(Command.valid_moves.value)
                                response = await self.get_response_timeout(208)  # valid moves
                                if response:
                                    print('\n' + str(response) + '\n')
                            case "u":
                                if ai_enemy:
                                    cmd_undo = Command.undo_move.value
                                    cmd_undo.update({"num": "1"})
                                    await self.send_cmd(Command.undo_move.value)
                                    break
                            case "q":
                                break
                            case _:
                                success = await self.exec_move(move)
                                if not success:
                                    print(f"\nError: Invalid move!\nMove: {move}\n")
                                    await asyncio.sleep(0.5)
                                else:
                                    break
            elif int(response.get("response_code")) in [202, 203]:  # game over / evaluation finished
                print("\n" + str(response) + "\n")
                if not ai_player and ai_enemy:
                    undo = input("\nDo you want to undo the last move? (y/n)\n").lower()
                    if undo == "y":
                        cmd_undo = Command.undo_move.value
                        cmd_undo.update({"num": "1"})
                        await self.send_cmd(Command.undo_move.value)
                        continue
                return
            else:
                print('\n' + str(response) + '\n')

    async def exec_move(self, move: str):
        cmd_move = Command.make_move.value
        cmd_move.update({"move": move})
        await self.send_cmd(cmd_move)
        response = await self.receive_json()
        if response.get("response_code") == 207:  # valid move
            return True
        elif response.get("response_code") in [255, 256]:  # no move / invalid move
            return False

    async def handle_blunder(self):
        if self.game_config.get("num"):  # case evaluation
            user_input = input("\nDo you want to show blunders of one of the matches? (y/n):\n").lower()
        else:  # case regular game
            user_input = input("\nDo you want to show blunders? (y/n):\n").lower()

        if user_input == "y":
            await self.send_cmd(Command.blunder.value)
            response = await self.get_response_timeout(212)  # blunder
            if response:
                print("\nIf blunder:\nfirst arg = move index; second arg = move\n")
                print('\n' + str(response) + '\n')

    async def handle_timeline(self):
        if self.game_config.get("num"):  # case evaluation
            user_input = input(
                "\nDo you want to review chosen states of one of the matches (timeline)? (y/n):\n").lower()
        else:  # case regular game
            user_input = input("\nDo you want to review chosen states of the match (timeline)? (y/n):\n").lower()
        if user_input == "y":
            timeline = False
            while True:
                user_input = input("\nWhich game state do you want to review (index starting by 0)?\n"
                                   "(Press 'q' to skip review)\n").lower()
                if isinstance(user_input, int):
                    cmd_timeline = Command.timeline.value
                    cmd_timeline.update({"num": str(user_input)})
                    await self.send_cmd(cmd_timeline)
                    response = await self.receive_json()
                    if response.get("response_code") in [260, 261]:  # no timeline index / invalid timeline index
                        print('\n' + str(response) + '\n')
                        await asyncio.sleep(0.5)
                        continue
                    if response.get("response_code") == 214:  # valid timeline index
                        print('\n' + str(response) + '\n')
                        timeline = True
                        break
                elif user_input == "q":
                    break
                else:
                    continue
            if timeline:
                while True:
                    user_input = input("\nStep through timeline: (l/r)\n"
                                       "['l' = previous state; 'r' = next state]\n"
                                       "(Press 'q' to quit timeline)\n").lower()
                    match user_input:
                        case "l":
                            await self.send_cmd(Command.step.value)
                            response = await self.receive_json()
                            print('\n' + str(response) + '\n')
                        case "r":
                            await self.send_cmd(Command.unstep.value)
                            response = await self.receive_json()
                            print('\n' + str(response) + '\n')
                        case "q":
                            break
                        case _:
                            continue

    async def console_input(self, message: str) -> str:
        return input(message).lower()

    async def send_cmd(self, cmd: dict):
        cmd = json.dumps(cmd)
        await self.websocket.send(cmd)

    async def get_response_timeout(self, response_code: int) -> dict | None:
        try:
            response = await asyncio.wait_for(self.get_response(response_code), timeout=2)
        except asyncio.TimeoutError:
            print("Try operation again.")
            return None
        return response

    async def get_response(self, response_code: int) -> dict:
        while True:
            response = await self.receive_json()
            code = response.get("response_code")
            if code:
                if int(code) == response_code:
                    return response

    async def receive_json(self) -> dict:
        json_string = await self.websocket.recv()
        return json.loads(json_string)

    async def connect(self):
        url = f"ws://{self.host}:{self.port}/ws"
        try:
            self.websocket = await websockets.connect(url, ping_interval=None)
            print("\nSuccessfully connected.\n")
            return True
        except ConnectionRefusedError as e:
            print(f"Can not connect to server with: {url}")
            return False


class Command(Enum):
    create_lobby = {"command": "lobby", "command_key": "create"}
    join = {"command": "lobby", "command_key": "join"}
    swap = {"command": "lobby", "command_key": "swap"}
    leave = {"command": "lobby", "command_key": "leave"}
    create_game = {"command": "play", "command_key": "create"}
    new_game = {"command": "play", "command_key": "new_game"}
    make_move = {"command": "play", "command_key": "make_move"}
    valid_moves = {"command": "play", "command_key": "valid_moves"}
    undo_move = {"command": "play", "command_key": "undo_move"}
    surrender = {"command": "play", "command_key": "surrender"}
    quit = {"command": "quit", "command_key": "quit"}
    blunder = {"command": "play", "command_key": "blunder"}
    timeline = {"command": "play", "command_key": "timeline"}
    step = {"command": "play", "command_key": "step"}
    unstep = {"command": "play", "command_key": "unstep"}
    evaluate = {"command": "play", "command_key": "evaluate"}
    stop_evaluate = {"command": "play", "command_key": "stop_evaluate"}


class Config:
    game = ["connect4", "othello", "tictactoe", "nim", "checkers", "go", "waldmeister"]
    mode = ["player_vs_player", "player_vs_ai", "playerai_vs_ai", "playerai_vs_playerai"]
    difficulty = ["easy", "medium", "hard"]


if __name__ == "__main__":
    play = Play(host="localhost", port=12345)
    asyncio.run(play.main())