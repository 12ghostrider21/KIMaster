import asyncio
import os
import pathlib
import threading

from Tools.datatypes import GameConfig, EResponse
from Tools.utils import dotdict
from GameClient.arena import Arena
from GameClient.mcts import MCTS
from GameClient.player import Player
from starlette.websockets import WebSocket
from Tools.datatypes import EDifficulty, Response

class Pit:
    def __init__(self, game_config: GameConfig, game_client):
        self.game_config: GameConfig | None = game_config
        self.game_client: WebSocket = game_client
        self.arena: Arena | None = None

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
        folder = None
        file = None

        match game_name:  # to be replaced with a query (DB)
            case "connect4":
                path = os.path.abspath("../resources/pretrained_models/connect4/best.h5")
                folder = os.path.dirname(path)
                file = os.path.basename(path)
            case _:
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
        except AttributeError:
            return Response(EResponse.ERROR, "Game mode does not exist!")

        self.arena = Arena(player1, player2, game, self.game_client)
        self.start_arena(num_games)
        if num_games == 1:
            return Response(EResponse.SUCCESS, "Game initialized")
        else:
            return Response(EResponse.SUCCESS, "Evaluation runs")

    def init_nn(self, game, nnet, folder: str, file: str, difficulty: EDifficulty = EDifficulty.hard.value):
        nn = nnet(game)
        nn.load_checkpoint(folder, file)
        args = dotdict({'numMCTSSims': difficulty.value, 'cpuct': 1.0})
        mcts = MCTS(game, nn, args)
        return mcts

    def run_async_function_in_thread(self, num_games: int):
        # Neuen Event-Loop für den Thread erstellen
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if num_games == 1:
            # Async-Funktion im Event-Loop des Threads ausführen
            loop.run_until_complete(self.arena.playGame(verbose=True))
        else:
            loop.run_until_complete(self.arena.playGames(num_games))  # return values gone ?
        loop.close()

    def start_arena(self, num_games: int):
        thread = threading.Thread(target=self.run_async_function_in_thread, args=[num_games], daemon=True)
        thread.start()
        # new thread ?
        # await self.arena.playGame(verbose=True)
        # wins_player1, wins_player2, draws = await self.arena.playGames(num_games)

        #await self.game_client.send_cmd("broadcast", "arena",
        #                                {"response_code": EResponse.SUCCESS.value,
        #                                 "response_msg": "Game evaluated",
        #                                 "wins_player1": wins_player1,
        #                                 "wins_player2": wins_player2,
        #                                 "draws": draws})
