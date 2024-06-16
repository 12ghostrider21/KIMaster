import importlib
import io
import pygame
from logging import warn
from os import walk, environ, listdir
from os.path import join
import numpy as np
from fastapi import WebSocket, WebSocketDisconnect

from Tools.i_game import IGame
from Tools.language_handler import LanguageHandler
from Tools.mcts import MCTS
from Tools.rcode import RCODE
from Tools.utils import dotdict
from Tools.dynamic_imports import Importer
from connection_manager import AbstractConnectionManager
from lobby import Lobby
from lobby_manager import LobbyManager

environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # disable some logging features


class SocketServer(AbstractConnectionManager):
    def __init__(self, msg_builder: LanguageHandler):
        super().__init__(msg_builder)
        self.manager: LobbyManager = LobbyManager()
        # TODO import class instance
        self.importer: Importer = Importer()
        print(f"{self.importer=}")

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

    async def websocket_endpoint(self, websocket: WebSocket):
        await self.connect(websocket)
        game: IGame = None
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
                    case "ai_move":
                        array = read_object["board"]
                        dtype = read_object["dtype"]
                        shape = tuple(read_object["shape"])
                        cur_player = int(read_object.get("cur_player"))
                        game_name = command_key

                        board = np.array(array, dtype=dtype).reshape(shape)
                        # TODO game_classe instanc von game_name
                        # TODO lamda func of game with correct difficulty  lobby.difficulty
                        action = np.argmax(self.func(self.game.getCanonicalForm(board, cur_player)))
                        # todo np.argmax(lamda(game.conanboard( board, cur_player)))

                        await self.send_cmd(lobby.game_client, "play", "make_move",
                                            {"move": int(action), "p_pos": "p1" if cur_player == 1 else "p2"})
                    case "draw":
                        board: np.array = np.array(read_object.get("board"))
                        cur_player: int = read_object.get("cur_player")
                        valid: bool = bool(read_object.get("valid"))
                        game_name = command_key
                        #for game_name, v in self.imports.items():
                        #    if game_name.lower() == command_key.lower():
                        # TODO game_classe instanc von game_name
                        img_surface = self.game.draw(board, valid, cur_player=cur_player)
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
