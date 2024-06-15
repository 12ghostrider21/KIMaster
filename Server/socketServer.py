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
from connection_manager import AbstractConnectionManager
from lobby import Lobby
from lobby_manager import LobbyManager

environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # disable some logging features


class SocketServer(AbstractConnectionManager):
    def __init__(self, msg_builder: LanguageHandler):
        super().__init__(msg_builder)
        self.manager: LobbyManager = LobbyManager()
        self.game_name, self.game_instances, self.game_nnet, self.game_h5 = self.crawl_game_files()

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
    
    def __crawler_helper(found_files: list[str], current_game: str, root:str, target_dict: dict[str, str], ignored: list[str], pattern:str) -> bool :
        """
    Helper function to update the target dictionary with the found files if they are unique. 

    Args:
        found_files (list[str]): List of files found matching the pattern.
        current_game (str): The current game being processed.
        root (str): The root directory where the files are being searched.
        target_dict (dict[str, str]): The dictionary to update with the found file path.
        ignored (list[str]): List of games to be ignored due to issues.
        pattern (str): The pattern used for matching the files.

    Returns:
        bool: True if the file is unique and added to the target_dict, False otherwise.
    
    Raises:
        Warning: If multiple Files with identical pattern are found in the GameDirectory
    
    Notes:
        The intention behind this function is to reduce repetitive code in the `crawl_game_files()` function
    
    See Also:
        `crawl_game_files()`
    
    """
        if len(found_files) == 1: # add found file to target if it is unique
            target_dict.update({current_game:join(root,found_files[0])})
        elif len(found_files) > 1: # ignore it if it is not unique
            ignored.append(current_game)
            warn(f"could not identify unique {pattern} file for game: {current_game}. Make sure that there is only one file matching the name NNet.py in the {root} directory. To prevent unpredictable behaviour {current_game} will be ignored.")
            return False
        return True

    def crawl_game_files(self) -> tuple[list[str], dict[str:str], dict[str:str], dict[str:str]]:
        """
    Crawl the game files and categorize them into different dictionaries based on their types.

    Returns:
        tuple: A tuple containing four elements:
            - games (list[str]): List of all game names found in the directory.
            - game_pys (dict[str, str]): Dictionary with game names as keys and paths to their Game.py files as values.
            - game_nnets (dict[str, str]): Dictionary with game names as keys and paths to their NNet.py files as values.
            - game_h5s (dict[str, str]): Dictionary with game names as keys and paths to their .h5 files as values.

    Raises:
        Warning: If multiple directories with identical names are found in the GameDirectory.
    """
        # init return values
        game_pys: dict[str, str] = {}
        game_nnets: dict[str,str] = {}
        game_h5s: dict[str, str] = {}
        games:list[str] = [game for game in listdir("/app/Games")]
        results = (games, game_pys, game_nnets, game_h5s)  
        
        # init list for those games to exclude from result
        ignored: list[str] = []
        
        for root, dir_names, file_names in walk("Games"):
            # make all lower case, to remove case sensitivity
            
            # get the current game
            current_game = [game for game in games if game.lower() in root.lower()]
            
            # only resolve Files if a unique game could be identified
            if len(current_game) == 1:
                current_game = current_game[0]
                
                # find *Game.py file of the current game
                game_py_file_pattern: str = "Game.py"
                found_game_pys = [f for f in file_names if f.lower().endswith(game_py_file_pattern.lower())]
                if not self.__crawler_helper(found_game_pys, current_game, root, game_pys, ignored, "*"+game_py_file_pattern):
                    continue
                
                # find NNet.py files of the current game
                nnet_file_pattern = "NNet.py"
                found_nnets = [f for f in file_names if f.lower() == nnet_file_pattern.lower()]
                if not self.__crawler_helper(found_nnets, current_game, root, game_nnets, ignored, nnet_file_pattern):
                    continue
                
                # find the .h5 of the current game
                h5_file_pattern = ".h5"
                found_h5s = [f for f in file_names if f.lower().endswith(h5_file_pattern.lower())]
                if not self.__crawler_helper(found_h5s, current_game, root, game_h5s, ignored, "*"+h5_file_pattern):
                    continue
                
            elif len(current_game) > 1:
                warn(f"the game {current_game} seems to exist several times. To prevent unpredictable behaviour {current_game} will be ignored. This Error is caused if there are multiple directories with identical names in your GameDirectory.")
                for game in current_game:
                    ignored.append(game)
        
        # remove ignored games
        for ignored_game in ignored:
            for r in results:
                try:
                    if isinstance(r, dict):
                        r.pop(ignored_game)
                    elif isinstance(r, list):
                        r.remove(ignored_game)
                except (ValueError, KeyError):
                    pass
        return results

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
