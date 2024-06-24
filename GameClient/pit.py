import asyncio

import numpy as np

from GameClient.arena import Arena
from GameClient.player import Player
from Tools.Game_Config.game_config import GameConfig
from Tools.rcode import RCODE
from Tools.response import Response


class Pit:
    def __init__(self, game_client):
        self.game_client = game_client
        self.arena: Arena = Arena(game_client)
        self.player1: Player = Player()
        self.player2: Player = Player()

    def start_battle(self, board: np.array, cur_player: int, it: int):
        asyncio.create_task(self.arena.play(board=board, cur_player=cur_player, it=it))

    def stop_battle(self) -> None:
        self.arena.stop()

    def set_move(self, move, pos) -> bool:
        if self.arena.cur_player == (1 if pos == "p1" else -1):
            if pos == "p1":
                self.player1.move = move
            if pos == "p2":
                self.player2.move = move
            return True  # is your Turn
        return False  # not your Turn

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

    def undo(self, steps):
        state, player, iteration = None, None, None
        steps = steps * 2 + 1  # *2 for enemy also undo and +1 for arena first append ignore
        if len(self.arena.history) == 1:
            return state, player, iteration  # return None to detect, no undo available

        if steps >= len(self.arena.history):
            steps = len(self.arena.history)
        for _ in range(steps):
            state, player, iteration = self.arena.history.pop()
        return state, player, iteration

    def timeline(self, p_pos: str, forward: bool = True, start_index: int | None = None):
        def update_index(current_index, start, direction, history_length):
            if start is not None:
                current_index = (start - 1) % history_length
            return (current_index + (1 if direction else -1)) % history_length

        if p_pos == "p1":
            self.arena.time_line_index_p1 = update_index(
                self.arena.time_line_index_p1, start_index, forward, len(self.arena.history)
            )
            state, player, iteration = self.arena.history[self.arena.time_line_index_p1]
        else:
            self.arena.time_line_index_p2 = update_index(
                self.arena.time_line_index_p2, start_index, forward, len(self.arena.history)
            )
            state, player, iteration = self.arena.history[self.arena.time_line_index_p2]

        return state, player, iteration
