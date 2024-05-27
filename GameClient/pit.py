from asyncio import create_task, Task
import numpy as np
from starlette.websockets import WebSocket
from Tools.Game_Config import GameConfig, EDifficulty
from Tools.Response import R_CODE, Response
from Tools.utils import dotdict
from Tools.mcts import MCTS
from arena import Arena
from player import Player


class Pit:
    def __init__(self, game_config: GameConfig, game_client):
        self.game_config: GameConfig | None = game_config
        self.game_client: WebSocket = game_client
        self.arena: Arena | None = None
        self.arena_task: Task | None = None
        self.player1: Player | None = None
        self.player2: Player | None = None

    async def start_game(self, num_games: int, verbose: bool, board: np.array, cur_player: int, it: int) -> (Response |
                                                                                                             None):
        # check if game is set
        if self.game_config is None:
            return
        if self.arena_task is not None and not self.arena_task.done():
            await self.arena_task
        # no task exist                        or done
        if self.arena_task is None or self.arena_task.done():
            if num_games == 1:
                self.arena_task = create_task(self.arena.playGame(verbose=verbose,
                                                                  board=board,
                                                                  cur_player=cur_player,
                                                                  it=it))
                return Response(R_CODE.P_INIT)
            else:
                self.arena_task = create_task(self.arena.playGames(num_games, train=False))
                return Response(R_CODE.P_EVAL)

    async def init_game(self, num_games: int, game_config: GameConfig | None) -> Response | None:
        if self.game_config is None and game_config is None:
            return
        if game_config is not None:  # if the arg is none, it's a re-init e.g. via "new_game"
            if not game_config():
                return
            self.game_config = game_config

        # get all values for init or set default values
        game = self.game_config.game.game_class()  # get the game_class
        network_class = self.game_config.game.nnet_class  # get the right NNet
        h5_folder = self.game_config.game.h5_folder  # get the .h5 trained model path
        h5_file = self.game_config.game.h5_file_name  # get the .h5 file
        difficulty = self.game_config.difficulty  # get the play difficulty
        mode = self.game_config.mode  # get the play mode

        self.player1 = Player(game, self.game_client, True if num_games > 1 else False)
        self.player2 = Player(game, self.game_client, True if num_games > 1 else False)

        try:
            mcts = self.init_nn(game, network_class, h5_folder, h5_file, difficulty)
            match mode.value:
                case "player_vs_player":
                    play1 = self.player1.play
                    play2 = self.player2.play
                case "player_vs_ai":
                    play1 = self.player1.play
                    play2 = lambda x: mcts.getActionProb(x, temp=0)
                case "playerai_vs_ai":
                    play1 = self.player1.play
                    play2 = lambda x: mcts.getActionProb(x, temp=0)
                case "playerai_vs_playerai":
                    play1 = self.player1.play
                    play2 = self.player2.play
                case _: # Game mode does not exist!
                    return
        except AttributeError:  # Game mode does not exist!
            return

        evaluator = lambda x: mcts.getActionProb(x, temp=1)
        self.arena = Arena(play1, play2, evaluator, game, self.game_client)
        # start with default values
        return await self.start_game(num_games, verbose=True, board=None, cur_player=1, it=0)

    async def set_move(self, move, player_pos: str):
        if player_pos == "p1":
            await self.player1.set_move(move, player_pos)
        if player_pos == "p2":
            await self.player2.set_move(move, player_pos)

    async def stop_play(self, player_pos: str):
        if player_pos == "p1":
            await self.player1.stop_play()
        if player_pos == "p2":
            await self.player2.stop_play()

    def init_nn(self, game, nnet, folder: str, file: str, difficulty: EDifficulty = EDifficulty.hard.value):
        nn = nnet(game)
        nn.load_checkpoint(folder, file)
        args = dotdict({'numMCTSSims': difficulty.value, 'cpuct': 1.0})
        mcts = MCTS(game, nn, args)
        return mcts
