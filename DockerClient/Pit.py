from Datatypes import GameConfig, RESPONSE
from resources.Path import Path
import IGame
import GameClient
import Arena
from utils import *
from DockerClient.MCTS import MCTS
from DockerClient.Player import Player
from Games.Connect4.keras.NNet import NNetWrapper as NNet


# import NNets from all Games


class Pit:
    def __init__(self, game_config: GameConfig, game_client: GameClient):
        self.game_config = game_config
        self.game_client = game_client
        self.arena: Arena = None

    async def init_game(self, num_games: int, game_config: GameConfig = None):
        if game_config is not None:  # if the arg is none, it's a re-init e.g. via "new_game"
            self.game_config = game_config

        game = self.game_config.game.value
        difficulty = self.game_config.difficulty.value

        player1 = None
        player2 = None
        folder = None
        file = None

        match self.game_config.game:  # to be replaced with a query (DB)
            case "connect4":
                folder, file = Path.get_path("connect4")
        """ 
            case "ttt":
                folder, file = Path.get_path("ttt")
            case "othello":
                folder, file = Path.get_path("othello")
            case "nim"
                folder, file = Path.get_path("nim")
            case "checkers"
                folder, file =  Path.get_path("checkers")
            case "go"
                folder, file = Path.get_path("go")
            case "waldmeister"
                folder, file =  Path.get_path("waldmeister")
        """

        mcts = self.init_nn(game, folder, file, difficulty)

        match game_config.mode:
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

        self.arena = Arena.Arena(player1, player2, game, self.game_client)
        if num_games == 1:
            await self.game_client.send_response(RESPONSE.SUCCESS, "Game initialized")
            await self.arena.playGame(verbose=True)
        else:
            await self.game_client.send_response(RESPONSE.SUCCESS, "Evaluation runs")
            wins_player1, wins_player2, draws = self.arena.playGames(num_games)
            await self.game_client.send_response(RESPONSE.SUCCESS, "Game evaluated",
                                                 {"wins_player1": wins_player1,
                                                  "wins_player2": wins_player2,
                                                  "draws": draws})

    def init_nn(self, game: IGame, folder: str, file: str, difficulty: int = 50):
        nn = NNet(game)
        nn.load_checkpoint(folder, file)
        args = dotdict({'numMCTSSims': difficulty, 'cpuct': 1.0})
        mcts = MCTS(game, nn, args)
        return mcts
