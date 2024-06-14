import asyncio
import importlib.util
import inspect
import os
import time
from threading import Thread

import numpy as np

from GameClient.arena import Arena
from GameClient.player import Player
from Tools.Game_Config.game_config import GameConfig


class Pit:
    def __init__(self, game_client):
        self.game_config = GameConfig()
        self.arena = Arena(game_client)
        self.game_classes: dict = {}
        self.player1: Player = Player()
        self.player2: Player = Player()
        self.arena_task: Thread = None

    def stop_arena(self):
        if self.arena_task is None:
            return
        self.arena.stop = True
        print("ARENA STOPPING...")
        while self.arena_task is not None:
            time.sleep(0.1)
        self.arena.stop = False
        return

    def init_arena(self, game_config: GameConfig):
        play1, play2 = None, None
        match game_config.mode.value:
            case 0 | 3:
                play1 = self.player1.play
                play2 = self.player2.play
            case 1:
                play1 = self.player1.play
                play2 = self.player2.playAI
            case 2:
                play1 = self.player1.playAI
                play2 = self.player2.play
        game = self.game_classes.get(game_config.game.lower())()
        self.arena.set_arena(game, game_config.game, play1, play2)

    def start_game(self, board: np.array, cur_player: int, it: int):
        self.arena.stop = False
        self.arena.history.clear()
        self.arena_task = Thread(target=self.__run_async_method_in_thread, args=(board, cur_player, it), daemon=True)
        self.arena_task.start()

    def __run_async_method_in_thread(self, board, cur_player, it):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.arena.playGame(board, cur_player, it))
        loop.close()

    def set_move(self, move, pos):
        if pos == "p1":
            self.player1.move = move
        if pos == "p2":
            self.player2.move = move

    @staticmethod
    def import_game_classes(directory):
        pattern: str = "Game.py"
        imported_classes = {}

        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(pattern):
                    module_name = filename[:-3]
                    file_path = os.path.join(root, filename)

                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        name = name.replace("Game", "").lower()
                        if obj.__module__ == module_name:
                            imported_classes[name] = obj
                            print("Imported: ", name)
        return imported_classes
