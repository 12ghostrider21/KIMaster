import importlib.util
import io
import os
import sys
from enum import Enum, auto
from os.path import splitext, basename

import numpy as np

from Tools.Game_Config.difficulty import EDifficulty
from Tools.i_game import IGame
from Tools.mcts import MCTS
from Tools.trained_folder_dataclass import TrainedFolder
from Tools.utils import dotdict

class ExcludeModule(Enum):
    GAME_PY = auto()
    NNET = auto()
    LAMBDA = auto()


class Importer:

    def __init__(self, directory: str, *exclude: ExcludeModule):
        self.__game_names, self.__game_pys, self.__game_nnets, self.__game_folder = self.__crawl_game_files(directory)
        # get all game classes
        if ExcludeModule.GAME_PY not in exclude:
            print(f"[{self.__class__.__name__}]", "Importing Game classes...")
            self.__game_classes = self.__import_game_classes()
        # import NNet.py of each game
        if ExcludeModule.NNET not in exclude:
            print(f"[{self.__class__.__name__}]", "Importing NNet classes...")
            self.__game_nnets = self.__import_nnet()
        # create lambda functions for each game and difficulty
        if ExcludeModule.LAMBDA not in exclude:
            print(f"[{self.__class__.__name__}]", "Creating AI lambdas functions...")
            self.__game_funcs = self.__create_lambdas()
        print(f"[{self.__class__.__name__}]", "Initialised fully.")

    def get_games(self) -> dict[str, IGame]:
        return {k: game() for k, game in self.__game_classes.items()}

    def get_ai_func(self) -> dict:
        return self.__game_funcs.copy()

    @staticmethod
    def __init_nn(game: IGame, nnet, trained_folder: TrainedFolder, difficulty: EDifficulty):
        nn = nnet(game)
        nn.load_checkpoint(trained_folder.folder, trained_folder.file)
        mcts = MCTS(game, nn, dotdict({'numMCTSSims': 250, 'cpuct': 3.0}))
        return mcts

    @staticmethod
    def __crawl_game_files(directory: str) -> tuple[set[str], dict[str, str], dict[str, str], dict[str, TrainedFolder]]:
        """
        return game_names, game_pys, game_nnets, game_folder: TrainedFolder
        """
        # Initialize return values
        game_names: set[str] = set(os.listdir(directory))
        game_pys: dict[str, str] = {}
        game_nnets: dict[str, str] = {}
        game_folder: dict[str, TrainedFolder] = {}
        results = (game_names, game_pys, game_nnets, game_folder)

        for root, _, filenames in os.walk(directory):
            for game in game_names:  # for all found games
                if game.lower() in root.lower():  # only directory with game_name
                    for f in filenames:
                        file_path = os.path.join(root, f)
                        lower_f = f.lower()
                        if lower_f.endswith("game.py") and game not in game_pys:
                            game_pys[game] = file_path
                        elif lower_f == "nnet.py" and game not in game_nnets:
                            game_nnets[game] = file_path
                        elif (lower_f.endswith(".tar") or lower_f.endswith(".h5")) and game not in game_folder:
                            base_name = os.path.basename(file_path)
                            base_directory = os.path.dirname(file_path)
                            game_folder[game] = TrainedFolder(base_directory, base_name)

        # Identify and remove games missing entries in any of the dictionaries
        incomplete_games = []
        for game in list(game_names):
            missing_parts = []
            if game not in game_pys:
                missing_parts.append("Game.py")
            if game not in game_nnets:
                missing_parts.append("NNet.py")
            if game not in game_folder:
                missing_parts.append("Model file (.tar or .h5)")
            if missing_parts:
                incomplete_games.append((game, missing_parts))
                game_names.discard(game)
                game_pys.pop(game, None)
                game_nnets.pop(game, None)
                game_folder.pop(game, None)

        if incomplete_games:
            print(f"[{__class__.__name__}]", "Warning: The following games were removed due to missing entries:")
            for game, missing_parts in incomplete_games:
                print(f"[{__class__.__name__}]", f"{game} is missing: {', '.join(missing_parts)}")

        return results

    @staticmethod
    def __import_class_from_file(file_path, class_name=None):
        module_name: str = splitext(basename(file_path))[0]
        # try to resolve automatically
        class_name = module_name if class_name is None else class_name
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Return the class from the module
        if hasattr(module, class_name):
            return getattr(module, class_name)
        else:
            raise ImportError(
                f"Class {class_name} not found in {file_path}. To make sure your Game can be found, name the class "
                f"the same as the Game.py file, (but with out the Game.py). The file for the neural net must be named "
                f"NNet.py")

    def __import_game_classes(self):
        return {game: Importer.__import_class_from_file(self.__game_pys[game]) for game in self.__game_names}

    def __import_nnet(self):
        return {game: Importer.__import_class_from_file(self.__game_nnets[game], 'NNetWrapper')
                for game in self.__game_names}

    def __create_lambdas(self):
        # CREATE LAMBDAS
        # 1) generate a list of games and difficulty pairs
        game_diff_pairs: list[tuple[str, EDifficulty]] = [(game, diff) for game in self.__game_names for diff in
                                                          EDifficulty]
        # 2) generate the monte carlo tree search for each game and each difficulty

        result = {}
        for game, diff in game_diff_pairs:
            old = sys.stdout
            sys.stdout = io.StringIO()
            mcts = Importer.__init_nn(self.__game_classes[game](), self.__game_nnets[game], self.__game_folder[game], diff)
            result.update({(game, diff): (lambda x: np.argmax(mcts.getActionProb(x, temp=0)), (game, diff))})
            sys.stdout = old
        return result


if __name__ == "__main__":
    # For testing purposes
    i = Importer("../Games")
    print(i.get_games())
    print(i.get_ai_func())

    x = lambda x: 1 + x
