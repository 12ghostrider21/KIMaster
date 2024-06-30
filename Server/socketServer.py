import asyncio
import io
from os import environ

import numpy as np
import pygame
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

    @staticmethod
    def surface_to_png(img: pygame.surface) -> bytes:
        byte_io = io.BytesIO()
        pygame.image.save(img, byte_io, 'PNG')
        png_bytes = byte_io.getvalue()
        byte_io.close()
        return png_bytes

    async def ai_Action(self, game: IGame, board: np.array, it: int, mcts, cur_player, game_client: WebSocket):
        func = lambda x, n: np.argmax(mcts.get_action_prob(x, temp=(0.5 if n <= 6 else 0.)))
        action = func(game.getCanonicalForm(board, cur_player), it)
        await self.send_cmd(game_client, "play", "make_move",
                            {"move": int(action), "p_pos": "p1" if cur_player == 1 else "p2"})

    async def blunder(self, game: IGame, mcts, actions: any, game_client: WebSocket, p_pos: str):
        func = lambda x: mcts.get_action_prob(x, temp=1)
        blunder_list = []
        for index, board, player, action in actions:

            # probability vector
            action_probs = np.array(func(game.getCanonicalForm(board, player)))

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

    async def websocket_endpoint(self, websocket: WebSocket):
        await self.connect(websocket)
        game_instances: dict[str, IGame] = self.importer.get_games()
        ai_funcs = self.importer.get_ai_func()
        try:
            while True:
                read_object: dict = await websocket.receive_json()
                lobby: Lobby = self.manager.get_lobby(read_object.get("key"))
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
                        array = read_object["board"]
                        it = int(read_object["it"])
                        cur_player = int(read_object.get("cur_player"))
                        board = np.array(array, dtype=default.dtype).reshape(default.shape)
                        mcts = ai_funcs.get(lobby.game).get(lobby.difficulty)
                        await asyncio.create_task(self.ai_Action(game, board, it, mcts, cur_player, lobby.game_client))
                    case "blunder":
                        game = game_instances[command_key]
                        default = game.getInitBoard()
                        mcts = ai_funcs.get(lobby.game).get(lobby.difficulty)
                        actions = []  # reconstruct blunder_history from payload
                        for k, v in read_object.items():
                            if k not in ["command", "command_key", "to", "key"]:
                                payload = (k, np.array(v[0], dtype=default.dtype).reshape(default.shape), v[1], v[2])
                                actions.append(payload)
                        await asyncio.create_task(self.blunder(game, mcts, actions, lobby.game_client, p_pos))
                    case "draw":
                        array: np.array = np.array(read_object.get("board"))
                        cur_player: int = read_object.get("cur_player")
                        valid: bool = bool(read_object.get("valid"))
                        game_name = command_key
                        game = game_instances[game_name]
                        default = game.getInitBoard()
                        board = np.array(array, dtype=default.dtype).reshape(default.shape)
                        img_surface = game.draw(board, valid, cur_player=cur_player)
                        img = self.surface_to_png(img_surface)
                        if p_pos is None:
                            # broadcast
                            for c in lobby.get(p_pos):
                                await self.send_bytes(c, img)
                        else:
                            # to p_pos
                            await self.send_bytes(lobby.get(p_pos), img)

        except RuntimeError:
            pass
        except WebSocketDisconnect:
            pass
        await self.disconnect(websocket)
