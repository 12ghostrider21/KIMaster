import importlib.util
import os
from os.path import splitext, basename, join, split
from os import walk
import sys
from enum import Enum, auto

from Tools.mcts import MCTS
from Tools.utils import dotdict
from Tools.i_game import IGame
from Tools.Game_Config.difficulty import EDifficulty


class exludable_modules(Enum):
    GAME_PY = auto()
    NNET = auto()
    LAMBDA = auto()


class Importer:
    #def __new__(cls, *args):
    #    if not hasattr(cls, 'instance'):
    #        cls.instance = super(Importer, cls).__new__(cls)
    #    return cls.instance

    @staticmethod
    def __init_nn(game, nnet, h5_path, difficulty: EDifficulty):
        h5_folder_file = split(h5_path)
        folder = h5_folder_file[0]
        file = h5_folder_file[1]
        nn = nnet(game)
        nn.load_checkpoint(folder, file)
        args = dotdict({'numMCTSSims': difficulty.value, 'cpuct': 1.0})
        mcts = MCTS(game, nn, args)
        return mcts

    def get_game_instances(self) -> dict[str, IGame]:
        return {game: self.game_classes[game]() for game in self.game_names}

    def get_game_funcs(self):
        return self.game_funcs

    @staticmethod
    def __crawler_helper(found_files: list[str], current_game: str, root: str, target_dict: dict[str, str],
                         ignored: list[str], pattern: str) -> bool:
        if len(found_files) == 1:  # add found file to target if it is unique
            target_dict.update({current_game: join(root, found_files[0])})
        elif len(found_files) > 1:  # ignore it if it is not unique
            ignored.append(current_game)
            print(
                f"could not identify unique {pattern} file for game: {current_game}."
                f" Make sure that there is only one file matching the name {pattern} in the {root} directory."
                f" To prevent unpredictable behaviour {current_game} will be ignored.")
            return False
        return True

    @staticmethod
    def __crawl_game_files() -> tuple[set[str], dict[str, str], dict[str, str], dict[str, str]]:
        """
    Crawl the game files and categorize them into different dictionaries based on their types.

    Returns:
        tuple: A tuple containing four elements:
            - games (list[str]): List of all game names found in the directory.
            - game_pys (dict[str, str]): Dictionary with game names as keys and paths to their Game.py files as values.
            - game_nnets (dict[str, str]): Dictionary with game names as keys and paths to their NNet.py files as values
            - game_h5s (dict[str, str]): Dictionary with game names as keys and paths to their .h5 files as values.

    Raises:
        Warning: If multiple directories with identical names are found in the GameDirectory.
    """
        # init return values
        games: set[str] = {game for game in os.listdir("../Games")}
        game_pys: dict[str, str] = {}
        game_nnets: dict[str, str] = {}
        game_h5s: dict[str, str] = {}

        excluded_from_result: list = []
        results = (games, game_pys, game_nnets, game_h5s)

        # init list for those games to exclude from result
        ignored: list[str] = []

        for root, dir_names, file_names in walk("../Games"):
            # get the current game
            current_game = [game for game in games if game.lower() in root.lower()]

            # only resolve Files if a unique game could be identified
            if len(current_game) == 1:
                current_game = current_game[0]

                # find *Game.py file of the current game
                game_py_file_pattern: str = "Game.py"
                found_game_pys = [f for f in file_names if f.lower().endswith(game_py_file_pattern.lower())]
                if not Importer.__crawler_helper(found_game_pys, current_game, root, game_pys, ignored,
                                                 "*" + game_py_file_pattern):
                    continue

                # find NNet.py files of the current game
                nnet_file_pattern = "NNet.py"
                found_nnets = [f for f in file_names if f.lower() == nnet_file_pattern.lower()]
                if not Importer.__crawler_helper(found_nnets, current_game, root, game_nnets, ignored,
                                                 nnet_file_pattern):
                    continue

                # find the .h5 of the current game
                h5_file_pattern = ".h5"
                found_h5s = [f for f in file_names if f.lower().endswith(h5_file_pattern.lower())]
                if not Importer.__crawler_helper(found_h5s, current_game, root, game_h5s, ignored,
                                                 "*" + h5_file_pattern):
                    continue

            elif len(current_game) > 1:
                print(f"WARNING: the game {current_game} seems to exist several times."
                      f" To prevent unpredictable behaviour {current_game} will be ignored. This Error is caused if "
                      f"there are multiple directories with identical names in your GameDirectory.")
                for game in current_game:
                    ignored.append(game)

        # ignore games where Game.py, NNet.py and.h5 files; could not be found
        for game in games:
            for element in [res for res in results if res is not games and res not in excluded_from_result]:
                if game not in element:
                    ignored.append(game)
                    print(
                        f"WARNING: A required File is missing for the game {game}. The path of this file is expected "
                        f"to be in this collection {element}. To prevent unstable behaviour the game {game} will be "
                        f"Ignored.")

        # remove ignored games
        for ignored_game in ignored:
            for r in results:
                if isinstance(r, dict):
                    r.pop(ignored_game, None)
                elif isinstance(r, set):
                    r.discard(ignored_game)
        return results

    @staticmethod
    def __import_class_from_file(file_path, class_name=None):
        # TODO try except ModuleNotFoundError -> Ignore missing modules and print them as missing!
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

    def __init__(self, *modules_to_exclude: exludable_modules):
        # get all relevant files related to games
        self.game_names, self.__game_pys, self.__game_nnet_files, self.__game_h5s = self.__crawl_game_files()

        # get all game classes
        if exludable_modules.GAME_PY not in modules_to_exclude:
            self.game_classes = self.__import_game_classes()
        # import NNet.py of each game
        if exludable_modules.NNET not in modules_to_exclude:
            self.game_nnets = self.__import_nnet()
        # create lambda functions for each game and difficulty
        if exludable_modules.LAMBDA not in modules_to_exclude:
            self.game_funcs = self.__create_lambdas()

    def __str__(self):
        return (f"{self.game_funcs=}\n"
                f"{self.game_nnets=}\n"
                f"{self.game_classes=}")

    def __import_game_classes(self):
        return {game: Importer.__import_class_from_file(self.__game_pys[game]) for game in self.game_names}

    def __import_nnet(self):
        return {game: Importer.__import_class_from_file(self.__game_nnet_files[game], 'NNetWrapper')
                           for game in self.game_names}

    def __create_lambdas(self):
        # CREATE LAMBDAS
        # 1) generate a list of games and difficulty pairs
        game_diff_pairs: list[tuple[str, EDifficulty]] = [(game, diff) for game in self.game_names for diff in
                                                          EDifficulty]

        # 2) generate the monte carlo tree search for each game and each difficulty
        wrapper_for_init_nn = lambda game, diff: Importer.__init_nn(self.game_classes[game](), self.game_nnets[game],
                                                                    self.__game_h5s[game], diff)
        game_mcts = {pair: wrapper_for_init_nn(pair[0], pair[1]) for pair in game_diff_pairs}

        # 3) generate functions for each game and difficulty
        return {pair: lambda x: game_mcts[pair].getActionProb(x, temp=0) for pair in game_diff_pairs}


if __name__ == "__main__":
    # For testing purposes
    i = Importer()
    print(i)
