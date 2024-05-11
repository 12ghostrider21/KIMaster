from DockerClient.i_game import IGame
from datatypes import GameConfig, RESPONSE
from resources.Path import Path
from game_client import GameClient
from arena import Arena
from utils import *
from DockerClient.mcts import MCTS
from DockerClient.player import Player
from Games.Connect4.keras.NNet import NNetWrapper as NNet


# import NNets from all Games


class Pit:
    def __init__(self, game_config: GameConfig, game_client: GameClient):
        self.game_config = game_config
        self.game_client = game_client
        self.arena: Arena | None = None

    async def init_game(self, num_games: int, game_config: GameConfig = None, player_pos=None):
        if game_config is not None:  # if the arg is none, it's a re-init e.g. via "new_game"
            self.game_config = game_config

        game = self.game_config.get("game")  # game name
        difficulty = self.game_config.get("difficulty")
        player1 = None
        player2 = None
        folder = None
        file = None

        match game:  # to be replaced with a query (DB)
            case "connect4":
                folder, file = Path.get_path(game)
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
        
        from e_game import EGame
        
        game = EGame.connect4
        
        mcts = self.init_nn(game, folder, file, difficulty)

        match game_config.get("mode"):
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

        self.arena = Arena(player1, player2, game, self.game_client)
        if num_games == 1:
            await self.game_client.send_response(response_code=RESPONSE.SUCCESS,
                                                 player_pos=player_pos,
                                                 response_msg="Game initialized")
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
