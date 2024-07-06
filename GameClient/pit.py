import asyncio
import numpy as np
from GameClient.arena import Arena
from GameClient.player import Player
from Tools.Game_Config.game_config import GameConfig


# The Pit class manages the game interactions and states
class Pit:
    def __init__(self, game_client):
        # Initialize the Pit with the game client
        self.game_client = game_client
        # Create an arena instance using the game client
        self.arena: Arena = Arena(game_client)
        # Initialize two players
        self.player1: Player = Player()
        self.player2: Player = Player()

    def clear_arena(self):
        self.arena.history.clear()  # reset history on new game configuration
        self.arena.blunder.clear()  # reset blunder on new game configuration
        self.arena.blunder_history.clear()  # reset
        self.arena.blender_calculation = False  # reset to default

    # Start the battle in the arena
    def start_battle(self, board: np.array, cur_player: int, it: int):
        # Set the arena's running status to True
        self.arena.running = True
        self.arena.board = board
        # Create and start an asynchronous task to play the game in the arena
        asyncio.create_task(self.arena.play(cur_player=cur_player, it=it))

    # Stop the battle in the arena
    def stop_battle(self) -> None:
        # Call the arena's stop method to halt the game
        self.arena.stop()

    # Set the move for a player
    def set_move(self, move, pos) -> bool:
        # Check if it's the correct player's turn based on their position
        if self.get_cur_player() == (1 if pos == "p1" else -1):
            # Set the move for player 1
            if pos == "p1":
                self.player1.move = move
            # Set the move for player 2
            elif pos == "p2":
                self.player2.move = move
            return True  # It is the player's turn
        return False  # Not the player's turn

    def get_cur_player(self) -> int:
        return self.arena.cur_player

    # Initialize the arena with the game configuration
    def init_arena(self, game_config: GameConfig):
        play1, play2 = None, None
        # Match the game mode to set up the appropriate player functions
        match game_config.mode.value:
            case 0 | 3:  # player_vs_player or playerai_vs_playerai
                play1 = self.player1.play
                play2 = self.player2.play
            case 1 | 4:  # player_vs_kim or playerai_vs_kim
                play1 = self.player1.play
                play2 = self.player2.playAI
            case 2 | 5:  # kim_vs_player or kim_vs_playerai
                play1 = self.player1.playAI
                play2 = self.player2.play
        # Print the new game configuration
        print("New game loaded:", game_config)
        # Set the arena with the game and player configurations
        self.arena.set_arena(game_config.game, game_config.game_name, play1, play2)

    # Retrieve the last entry from the arena's history
    def get_last_hist_entry(self) -> tuple[list | None, int | None, int | None]:
        if len(self.arena.history) > 0:
            return self.arena.history[-1]
        return None, None, None

    # Undo a certain number of steps in the game
    def undo(self, steps: int):
        state, player, it = None, None, None
        if len(self.arena.history) >= 3:
            for _ in range(steps * 2 + 1):  # steps * 2 (own and enemy) + 1 for arena initial append
                if len(self.arena.history) != 0:
                    state, player, it = self.arena.history.pop()
                    for i, h in enumerate(self.arena.blunder_history):
                        x = h[0] == state
                        if np.all(x):
                            self.arena.blunder_history.pop(i)
                            break
        return state, player, it

    # Navigate through the game timeline
    def timeline(self, p_pos: str, forward: bool = True, start_index: int | None = None):
        # Helper function to update the index for timeline navigation
        def update_index(current_index, start, direction, history_length):
            if start is not None:
                current_index = (start - 1) % history_length
            return (current_index + (1 if direction else -1)) % history_length

        if p_pos == "p1":
            self.arena.time_index_p1 = update_index(
                self.arena.time_index_p1, start_index, forward, len(self.arena.history)
            )
            state, player, iteration = self.arena.history[self.arena.time_index_p1]
        else:
            self.arena.time_index_p2 = update_index(
                self.arena.time_index_p2, start_index, forward, len(self.arena.history)
            )
            state, player, iteration = self.arena.history[self.arena.time_index_p2]

        return state, player, iteration

    def set_blunder(self, blunder: list):
        for b in blunder:
            self.arena.blunder.append(b)

    def get_blunder_payload(self) -> dict:
        data = {}
        for bh in self.arena.blunder_history:
            array, player, index, move = bh
            data[index] = (array.tolist(), player, move)
        return data

    def get_blunder(self, rotate: bool) -> dict:
        data = {"blunder": []}
        for b in self.arena.blunder:
            x = {"action": b[0] if not rotate else self.arena.game.rotateMove(b[0]),
                 "it": b[1],
                 "player": b[2]}
            data["blunder"].append(x)
        return data
