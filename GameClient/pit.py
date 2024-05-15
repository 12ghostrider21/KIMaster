import time
from asyncio import create_task, Task
import asyncio
import os
import pathlib
import threading

from Tools.datatypes import GameConfig, EResponse
from Tools.utils import dotdict
from GameClient.arena import Arena
from Tools.mcts import MCTS
from GameClient.player import Player
from starlette.websockets import WebSocket
from Tools.datatypes import EDifficulty, Response


class Pit:
    def __init__(self, game_config: GameConfig, game_client):
        self.game_config: GameConfig | None = game_config
        self.game_client: WebSocket = game_client
        self.arena: Arena | None = None
        self.arena_task: Task | None = None  # not used for now

    def new_arena_task(self) -> None:
        # no task exist
        if self.arena_task is None:
            self.arena_task: Task = create_task(self.arena.playGame(verbose=True))
            print("Task created!")
            return

        # task stopped or done
        if self.arena_task.done() or self.arena_task.cancelled():
            self.arena_task: Task = create_task(self.arena.playGame(verbose=True))
            print("Task created!")
            return

        # task is running, stopping it!
        self.arena_task.cancel()
        print("Cancel")
        while True:
            print(self.arena_task.done(), self.arena_task.cancelled())
            time.sleep(1)


    def init_game(self, num_games: int, game_config: GameConfig | None) -> Response:
        if game_config is not None:  # if the arg is none, it's a re-init e.g. via "new_game"
            self.game_config = game_config

        # check if arena is already running

        game = self.game_config.game.value[0]()  # create new game instance of Game import of EGame
        game_name = self.game_config.game.name
        nnet = self.game_config.game.value[1]    # get the right NNet
        difficulty = self.game_config.difficulty
        player1 = None
        player2 = None

        match game_name:  # to be replaced with a query (DB)
            case "connect4":
                path = os.path.abspath("../resources/pretrained_models/connect4/best.h5")
                folder = os.path.dirname(path)
                file = os.path.basename(path)
            case _:  # dürfte überflüssig sein
                return Response(EResponse.ERROR, "File not found", {"game": game_name})

        mcts = self.init_nn(game, nnet, folder, file, difficulty)
        try:
            match self.game_config.mode.value:
                case "player_vs_player":
                    player1 = Player(game, self.game_client).play
                    player2 = Player(game, self.game_client).play
                case "player_vs_ai":
                    player1 = Player(game, self.game_client).play
                    player2 = lambda x: mcts.getActionProb(x, temp=0)
                case "playerai_vs_ai":
                    player1 = Player(game, self.game_client).play
                    player2 = lambda x: mcts.getActionProb(x, temp=0)
                case "playerai_vs_playerai":
                    player1 = Player(game, self.game_client).play
                    player2 = Player(game, self.game_client).play
        except AttributeError:  # dürfte überflüssig sein
            return Response(EResponse.ERROR, "Game mode does not exist!", {"mode": self.game_config.mode.name})

        player3 = lambda x: mcts.getActionProb(x, temp=1)
        self.arena = Arena(player1, player2, player3, game, self.game_client)

        # self.start_arena(num_games)
        if num_games == 1:
            # self.new_arena_task() method in testing phase
            asyncio.create_task(self.arena.playGame(verbose=True))
            return Response(EResponse.SUCCESS, "Game initialized")
        else:
            asyncio.create_task(self.arena.playGames(num_games, train=False))
            return Response(EResponse.SUCCESS, "Evaluation runs")

    def init_nn(self, game, nnet, folder: str, file: str, difficulty: EDifficulty = EDifficulty.hard.value):
        nn = nnet(game)
        nn.load_checkpoint(folder, file)
        args = dotdict({'numMCTSSims': difficulty.value, 'cpuct': 1.0})
        mcts = MCTS(game, nn, args)
        return mcts