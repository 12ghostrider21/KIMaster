import asyncio
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
        self.arena_task: Thread | None = None

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
        game = self.game_classes.get(game_config.game.replace("Game", "").lower())
        self.arena.set_arena(game, game_config.game.replace("Game", ""), play1, play2)

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
