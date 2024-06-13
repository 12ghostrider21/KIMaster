import base64
import importlib.util
import io
import json
import os
import struct
import sys

import numpy as np
import pygame
from fastapi import WebSocket, WebSocketDisconnect

from Games.connect4.Connect4Game import Connect4Game
from Games.connect4.keras.NNet import NNetWrapper
from Tools.Game_Config.difficulty import EDifficulty
from Tools.language_handler import LanguageHandler
from Tools.mcts import MCTS
from Tools.rcode import RCODE
from Tools.utils import dotdict
from connection_manager import AbstractConnectionManager
from lobby import Lobby
from lobby_manager import LobbyManager

def init_nn(game, nnet, folder: str, file: str):
    nn = nnet(game)
    nn.load_checkpoint(folder, file)
    args = dotdict({'numMCTSSims': 5, 'cpuct': 1.0})
    mcts = MCTS(game, nn, args)
    return mcts

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'    # disable some logging features


class SocketServer(AbstractConnectionManager):
    def __init__(self, msg_builder: LanguageHandler):
        super().__init__(msg_builder)
        self.manager: LobbyManager = LobbyManager()
        self.imports: dict = self.find_and_import_classes("/app/Games")
        self.lambdas: dict = self.create_lambda()
        for k, v in self.lambdas.items():
            for x, y in v.items():
                print(k, x, y)

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

    @staticmethod
    def import_class_from_file(filepath: str, class_name: str):
        spec = importlib.util.spec_from_file_location(class_name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Find the class with case-insensitive match
        for attr in dir(module):
            if attr.lower() == class_name.lower():
                return getattr(module, attr)

        raise AttributeError(f"Class {class_name} not found in {filepath}")

    def find_and_import_classes(self, games_folder: str):
        imports = {}

        for game_name in os.listdir(games_folder):
            game_path = os.path.join(games_folder, game_name)
            if os.path.isdir(game_path):
                imports[game_name] = {}

                # Import Game classes (files ending with Game.py)
                for file_name in os.listdir(game_path):
                    if file_name.endswith('Game.py'):
                        game_file = os.path.join(game_path, file_name)
                        if os.path.isfile(game_file):
                            try:
                                game_class = self.import_class_from_file(game_file, file_name.replace(".py", ""))
                                imports[game_name]['Game'] = game_class()
                            except (FileNotFoundError, AttributeError) as e:
                                print(f"Could not import Game class from {game_file}: {e}")

                # Import NNetWrapper class from keras/NNet.py
                keras_file = os.path.join(game_path, 'keras', 'NNet.py')
                if os.path.isfile(keras_file):
                    try:
                        keras_class = self.import_class_from_file(keras_file, 'NNetWrapper')
                        imports[game_name]['NNetWrapper'] = keras_class
                    except (FileNotFoundError, AttributeError) as e:
                        print(f"Could not import NNetWrapper class from {keras_file}: {e}")

                # import Keras folder and model
                keras_model = os.path.join(game_path, 'keras', 'best.h5')
                if os.path.isfile(keras_model):
                    file = os.path.basename(keras_model)
                    folder = os.path.dirname(os.path.abspath(keras_model))
                    imports[game_name]["folder"] = folder
                    imports[game_name]["file"] = file

                # Import NNetWrapper class from pytorch/NNet.py
                pytorch_file = os.path.join(game_path, 'pytorch', 'NNet.py')
                if os.path.isfile(pytorch_file):
                    try:
                        pytorch_class = self.import_class_from_file(pytorch_file, 'NNetWrapper')
                        imports[game_name]['NNetWrapper'] = pytorch_class
                    except (FileNotFoundError, AttributeError) as e:
                        print(f"Could not import NNetWrapper class from {pytorch_file}: {e}")

                # import pytorch folder and model
                torch_model = os.path.join(game_path, 'pytorch', 'best.h5')
                if os.path.isfile(torch_model):
                    file = os.path.basename(torch_model)
                    folder = os.path.dirname(os.path.abspath(torch_model))
                    imports[game_name]["folder"] = folder
                    imports[game_name]["file"] = file
        return imports

    def create_lambda(self):
        print("Loading Ai models...")
        results = {}
        ignored_games = []
        # save original stdout
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        try:
            # redirect stdout to silent mode
            sys.stdout = open(os.devnull, 'w')
            sys.stderr = open(os.devnull, 'w')
            for k, v in self.imports.items():
                game = self.imports[k].get("Game")
                network_class = self.imports[k].get("NNetWrapper")  # get the right NNet
                h5_folder = self.imports[k].get("folder")  # get the .h5 trained model path
                h5_file = self.imports[k].get("file")  # get the .h5 file
                if h5_folder and h5_file:
                    for difficulty in EDifficulty:
                        mcts = self.init_nn(game, network_class, h5_folder, h5_file, difficulty)
                        if k not in results:
                            results[k] = {}
                        results[k][difficulty] = lambda x: mcts.getActionProb(x, temp=0)
                else:
                    ignored_games.append(f"For '{game}' no best.h5 was found. Ignoring it.")
        finally:
            # set stdout back to original
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            print("Loading Ai models done.")
        return results

    def init_nn(self, game, nnet, folder: str, file: str, difficulty: EDifficulty) -> MCTS:
        nn = nnet(game)
        nn.load_checkpoint(folder, file)
        args = dotdict({'numMCTSSims': difficulty.value, 'cpuct': 1.0})
        mcts = MCTS(game, nn, args)
        return mcts

    async def websocket_endpoint(self, websocket: WebSocket):
        await self.connect(websocket)
        game = Connect4Game()
        folder = r"/app/Games/connect4/keras"
        file = "best.h5"
        mcts = init_nn(game, NNetWrapper, folder, file)
        func = lambda x: mcts.getActionProb(x, temp=0)
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
                        #game_instance = self.imports.get(game_name)["Game"]
                        #dict_functions = self.lambdas.get(game_name)
                        board = np.array(array, dtype=dtype).reshape(shape)
                        action = np.argmax(func(game.getCanonicalForm(board, cur_player)))
                        print(action)
                        #if dict_functions is None:
                        #    print(f"No lambda functions found for game: {game_name}")
                        #    continue

                        #func = dict_functions.get(lobby.difficulty)
                        #if func is None:
                        #    print(f"No lambda function found for difficulty: {lobby.difficulty}")
                        #    continue

                        #move = None
                        #valids = game_instance.getValidMoves(board, cur_player)
                        #print("AI SEARCHING")
                        #while True:
                        #    x = game_instance.getCanonicalForm(board, cur_player)
                        #    try:
                        #        move = np.argmax(func(x))
                        #        if move >= len(valids):
                        #            print("Invalid move, retrying")
                        #            continue
                        #    except Exception as e:
                        #        print(x.shape, x)
                        #        print(f"Error in lambda function: {e}")
                        #        break
                        #    break
                        #if move is not None:
                         #   print("AI move was:", move)
                        await self.send_cmd(lobby.game_client, "play", "make_move",
                                                {"move": int(action), "p_pos": "p1" if cur_player == 1 else "p2"})
                    case "draw":
                        board: np.array = np.array(read_object.get("board"))
                        cur_player: int = read_object.get("cur_player")
                        valid: bool = bool(read_object.get("valid"))
                        for game_name, v in self.imports.items():
                            if game_name.lower() == command_key.lower():
                                img_surface = v["Game"].draw(board, valid, cur_player=cur_player)
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
