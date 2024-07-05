import asyncio
import io
import numpy as np
import pygame
from concurrent.futures import ThreadPoolExecutor
from os import environ
from fastapi import WebSocket, WebSocketDisconnect

from Tools.dynamic_imports import Importer
from Tools.i_game import IGame
from Tools.language_handler import LanguageHandler
from Tools.rcode import RCODE
from connection_manager import AbstractConnectionManager
from lobby import Lobby
from lobby_manager import LobbyManager

environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # disable some logging features


class SocketServer(AbstractConnectionManager):
    def __init__(self, msg_builder: LanguageHandler):
        super().__init__(msg_builder)
        self.manager: LobbyManager = LobbyManager()
        self.executor = ThreadPoolExecutor()  # Global Thread Executor without any Thread limits
        self.importer: Importer = Importer("/app/Games")

    async def connect(self, websocket: WebSocket):
        query_params = websocket.query_params
        login = query_params.get("login", "")
        if login not in self.manager.lobbies.keys():
            return await websocket.close(code=1008, reason="Unauthorized")
        self.manager.lobbies.get(login).game_client = websocket
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket):
        self.active_connections.remove(websocket)
        self.manager.disconnect_game_client(websocket)

    def submit_task(self, loop, coro, *args):
        """
        Run async methods in an own thread to reduce response times
        Args:
            loop: event loop
            coro: coroutine to run
            *args: parameters of coroutine

        Returns: None
        """
        loop.run_in_executor(self.executor, lambda: asyncio.run(coro(*args)))

    @staticmethod
    def player_to_pos(cur_player: int) -> str:
        return "p1" if cur_player == 1 else "p2"

    @staticmethod
    def surface_to_png(img: pygame.surface) -> bytes:
        byte_io = io.BytesIO()
        pygame.image.save(img, byte_io, 'PNG')
        png_bytes = byte_io.getvalue()
        byte_io.close()
        return png_bytes

    async def websocket_endpoint(self, websocket: WebSocket):
        await self.connect(websocket)
        loop = asyncio.get_event_loop()
        game_instances: dict[str, IGame] = self.importer.get_games()
        ai_funcs = self.importer.get_ai_func()
        try:
            while True:
                read_object: dict = await websocket.receive_json()

                lobby: Lobby = self.manager.get_lobby(read_object.get("key"))
                if lobby is None:
                    continue
                p_pos: str | None = read_object.get("to")  # None is Broadcast

                response = read_object.get("response")
                if response:
                    read_object.pop("response")  # remove internal entry
                    read_object.pop("to")  # remove internal entry
                    if read_object.get("key"):
                        read_object.pop("key")

                    client = lobby.get(p_pos)
                    if p_pos is None:
                        await self.broadcast_response(client, RCODE.get(response), read_object)
                    else:
                        await self.send_response(client, RCODE.get(response), read_object)
                    continue

                command: str = read_object.get("command")
                command_key: str = read_object.get("command_key")
                match command:
                    case "update":  # update lobby_states
                        game_running: bool = bool(read_object.get("game_running"))
                        lobby.game_running = game_running
                    case "ai_move":
                        game = game_instances[command_key]
                        default = game.getInitBoard()
                        it = int(read_object["it"])
                        cur_player = int(read_object.get("cur_player"))
                        board = np.array(read_object["board"], dtype=default.dtype).reshape(default.shape)
                        mcts = ai_funcs.get(lobby.game).get(lobby.difficulty)
                        self.submit_task(loop, self.ai_Action, game, board, it, mcts, cur_player, lobby.game_client)
                    case "blunder":
                        game = game_instances[command_key]
                        default = game.getInitBoard()
                        mcts = ai_funcs.get(lobby.game).get(lobby.difficulty)
                        actions = []  # reconstruct blunder_history from payload
                        for k, v in read_object.items():
                            if k not in ["command", "command_key", "to", "key"]:
                                payload = (k, np.array(v[0], dtype=default.dtype).reshape(default.shape), v[1], v[2])
                                actions.append(payload)
                        self.submit_task(loop, self.blunder, game, mcts, actions, lobby.game_client, p_pos)
                    case "draw":
                        await self.draw(read_object, game_instances[command_key], lobby, p_pos)

        except WebSocketDisconnect as e:
            code = {1000: "Normal dissconnect", 1001: "Browser reload/tab close",
                    1006: "GameClient was stopped connection break!"}
            print(websocket.client, f"WebSocket dissconnected with code: {e.code}, {code.get(e.code)}")
        finally:
            await self.disconnect(websocket)

    async def ai_Action(self, game: IGame, board: np.array, it: int, mcts, cur_player, game_client: WebSocket):
        func = lambda x, y, n: np.argmax(mcts.get_action_prob(x, y, temp=(0.5 if n <= 6 else 0.)))
        action_index = func(board, cur_player, it)
        move = game.translate(board, cur_player, action_index)
        await self.send_cmd(game_client, "play", "make_move",
                            {"move": move, "p_pos": self.player_to_pos(cur_player)})

    async def draw(self, read_object: dict, game: IGame, lobby: Lobby, p_pos: str):
        array: np.array = np.array(read_object.get("board"))
        valid: bool = bool(read_object.get("valid"))
        from_pos: int = read_object.get("from_pos")
        default = game.getInitBoard()
        board = np.array(array, dtype=default.dtype).reshape(default.shape)
        img_surface1 = game.draw(board, valid, 1, from_pos)
        img_surface2 = game.draw(board, valid, -1, from_pos)
        img1 = self.surface_to_png(img_surface1)
        img2 = self.surface_to_png(img_surface2)
        if p_pos is None:
            # broadcast
            clients = lobby.get(p_pos)
            spec = clients[:-2]
            for c in spec:
                await self.send_bytes(c, img1)  # spectators
            await self.send_bytes(clients[-2], img1)  # p1
            await self.send_bytes(clients[-1], img2)  # p2
        else:
            # to p_pos
            img = img1 if p_pos == "p1" else img2
            await self.send_bytes(lobby.get(p_pos), img)

    async def blunder(self, game: IGame, mcts, actions: any, game_client: WebSocket, p_pos: str):
        func = lambda x, y: mcts.get_action_prob(x, y, temp=1)
        blunder_list = []
        for index, board, player, action in actions:

            # probability vector
            action_probs = np.array(func(board, player))

            # using mean as reference whether a move is good or not so
            mean = 1.0 / np.count_nonzero(action_probs)
            good_actions_indices = np.where(action_probs >= mean)[0]
            good_actions = [game.translate(board, player, a) for a in good_actions_indices]
            if action not in good_actions:  # is blunder
                blunder_list.append((action, index, player))
        await self.send_cmd(game_client=game_client,
                            command="blunder",
                            command_key="blunder",
                            data={"blunder": blunder_list, "p_pos": p_pos})