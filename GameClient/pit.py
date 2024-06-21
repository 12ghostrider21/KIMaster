import asyncio

from GameClient.arena import Arena
from GameClient.player import Player
from Tools.Game_Config.game_config import GameConfig


class Pit:
    def __init__(self, game_client):
        self.game_client = game_client
        self.arena: Arena = Arena(game_client)
        self.player1: Player = Player()
        self.player2: Player = Player()

    def start_battle(self):
        asyncio.create_task(self.arena.play())

    def stop_battle(self):
        self.arena.stop()

    def set_move(self, move, pos):
        if pos == "p1":
            self.player1.move = move
        if pos == "p2":
            self.player2.move = move

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
        print("new game loaded:", game_config.game_name)
        self.arena.set_arena(game_config.game, game_config.game_name, play1, play2)

    def get_last_hist_entry(self) -> tuple[list, int, int]:
        if len(self.arena.history) > 0:
            return self.arena.history[-1]
