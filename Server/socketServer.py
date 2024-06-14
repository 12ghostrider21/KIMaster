import importlib
import io
import os

import numpy as np
import pygame
from fastapi import WebSocket, WebSocketDisconnect

from Tools.i_game import IGame
from Tools.language_handler import LanguageHandler
from Tools.mcts import MCTS
from Tools.rcode import RCODE
from Tools.utils import dotdict
from connection_manager import AbstractConnectionManager
from lobby import Lobby
from lobby_manager import LobbyManager

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # disable some logging features


class SocketServer(AbstractConnectionManager):
    def __init__(self, msg_builder: LanguageHandler):
        super().__init__(msg_builder)
        self.manager: LobbyManager = LobbyManager()
        self.game_name, self.game_instances, self.game_nnet = self.crawl_game_files()

        self.game: IGame = self.dynamic_import("Games.connect4.Connect4Game", "Connect4Game")()
        nnet = self.dynamic_import('Games.connect4.keras.NNet', 'NNetWrapper')
        mcts = self.init_nn(self.game, nnet, r"/app/Games/connect4/keras", "best.h5")
        self.func = lambda x: mcts.getActionProb(x, temp=0)
        #self.imports: dict = self.find_and_import_classes("/app/Games")
        #self.lambdas: dict = self.create_lambda()

    def dynamic_import(self, module_name, class_name):
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        return class_

    def init_nn(self, game, nnet, folder: str, file: str):
        nn = nnet(game)
        nn.load_checkpoint(folder, file)
        args = dotdict({'numMCTSSims': 5, 'cpuct': 1.0})
        mcts = MCTS(game, nn, args)
        return mcts

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

    def crawl_game_files(self):
        game_pys: dict[str, str] = {}
        game_nnets: dict[str, str] = {}
        games: list[str] = [game for game in os.listdir("/app/Games")]
        ignored: list[str] = []

        for root, dir_names, file_names in os.walk("/app/Games"):
            # make all lower case, to remove case sensitivity

            # get the current game
            current_game = [game for game in games if game.lower() in root.lower()]

            # only resolve Files if a unique game could be identified
            if len(current_game) == 1:
                current_game = current_game[0]

                # find *Game.py file of the current game
                game_py_files = [f for f in file_names if f.lower().endswith("Game.py".lower())]
                if len(game_py_files) == 1:
                    game_pys.update({current_game: os.path.join(root, game_py_files[0])})
                elif len(game_py_files) > 1:
                    ignored.append(current_game)
                    print(
                        f"could not identify unique *Game.py file for game: {current_game}. Make sure that there is only one file matching the name *Game.py in the {root} directory. To prevent unpredictable behaviour {current_game} will be ignored.")
                    continue

                # find the NNet.py of the current game
                nnet_files = [f for f in file_names if f.lower() == "NNet.py".lower()]
                if len(nnet_files) == 1:
                    game_nnets.update({current_game: os.path.join(root, nnet_files[0])})
                elif len(nnet_files) > 1:
                    ignored.append(current_game)
                    print(
                        f"could not identify unique NNet.py file for game: {current_game}. Make sure that there is only one file matching the name NNet.py in the {root} directory. To prevent unpredictable behaviour {current_game} will be ignored.")
                    continue

            elif len(current_game) > 1:
                print(
                    f"the game {current_game} seems to exist several times. To prevent unpredictable behaviour {current_game} will be ignored. This Error is caused if there are multiple directories with identical names in your GameDirectory.")
                for game in current_game:
                    ignored.append(current_game)

        # remove ignored games
        for game in ignored:
            try:
                games.remove(game)
            except ValueError:
                pass
            try:
                game_pys.pop(game)
            except KeyError:
                pass
            try:
                game_nnets.pop(game)
            except KeyError:
                pass
        return games, game_pys, game_nnets

    async def websocket_endpoint(self, websocket: WebSocket):
        await self.connect(websocket)
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
                        action = np.argmax(self.func(self.game.getCanonicalForm(board, cur_player)))
                        # todo np.argmax(lamda(game.conanboard( board, cur_player)))

                        await self.send_cmd(lobby.game_client, "play", "make_move",
                                            {"move": int(action), "p_pos": "p1" if cur_player == 1 else "p2"})
                    case "draw":
                        board: np.array = np.array(read_object.get("board"))
                        cur_player: int = read_object.get("cur_player")
                        valid: bool = bool(read_object.get("valid"))
                        #for game_name, v in self.imports.items():
                        #    if game_name.lower() == command_key.lower():
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
