import importlib.util
import io
import os
import sys
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from os.path import splitext, basename

from Tools.Game_Config.difficulty import EDifficulty
from Tools.i_game import IGame
from Tools.mcts import MCTS
from Tools.utils import dotdict


class ExcludeModule(Enum):
    GAME_PY = auto()
    MCTS = auto()


@dataclass
class FilePaths:
    game_name: str | None = field(default=None)
    game_py: str | None = field(default=None)
    nnet_py: str | None = field(default=None)
    model_path: str | None = field(default=None)
    model_file: str | None = field(default=None)
    found: bool = field(default=False)

    def missing(self) -> list:
        return [k for k, v in self.__dict__.items() if v is None]


class Entry:

    def __init__(self, game_name: str):
        self.game_name: str = game_name
        self.keras: FilePaths = FilePaths(game_name=self.game_name)
        self.torch: FilePaths = FilePaths(game_name=self.game_name)
        self.x: int = 0

    def print(self):
        if self.x == 0:
            print(f"Game: {self.game_name} does not have a NeuralNet folder!")
        else:
            if self.keras.found:
                if len(self.keras.missing()) == 0:
                    print(f"\033[92mGame: {self.game_name} (Keras) available.\033[0m")
                else:
                    print(f"\033[93mGame: {self.game_name} (Keras)\033[0m")
                for att in self.keras.missing():
                    match att:
                        case "game_py":
                            print(f"\033[91m-- Game.py is missing!\033[0m")
                        case "nnet_py":
                            print(f"\033[91m-- NNet.py is missing!\033[0m")
                        case "model_path":
                            print(f"\033[91m-- Model is missing! (best.h5)\033[0m")
            if self.torch.found:
                if len(self.torch.missing()) == 0:
                    print(f"\033[92mGame: {self.game_name} (PyTorch) available.\033[0m")
                else:
                    print(f"\033[93mGame: {self.game_name} (PyTorch)\033[0m")
                    for att in self.torch.missing():
                        match att:
                            case "game_py":
                                print(f"\033[91m-- Game.py is missing!\033[0m")
                            case "nnet_py":
                                print(f"\033[91m-- NNet.py is missing!\033[0m")
                            case "model_path":
                                print(f"\033[91m-- Model is missing! (best.pth.tar)\033[0m")


class Importer:
    def __init__(self, directory: str, *exclude: ExcludeModule):
        start = time.perf_counter()
        print(f"\033[94m[{self.__class__.__name__}]", "Fetching files...")
        self.__path: dict[str, Entry] = self.__crawl_game_files(directory)
        self.__game_classes = {}
        self.__game_mcts = {}

        if ExcludeModule.GAME_PY not in exclude:  # get all game classes
            self.__game_classes = self.__import_game_classes()
        if ExcludeModule.MCTS not in exclude:  # create MCTS functions for each game and difficulty
            self.__game_funcs = self.__import_funcs()
        end = time.perf_counter()
        print(f"\033[94m[{self.__class__.__name__}]", f"Initialised fully in {end-start:.4}s.\033[0m")

    def get_games(self) -> dict[str, IGame]:
        return {k: game() for k, game in self.__game_classes.items()}

    def get_ai_func(self) -> dict:
        return self.__game_funcs

    @staticmethod
    def __crawl_game_files(directory: str) -> dict[str, Entry]:
        # Initialize return values
        result: dict[str, Entry] = {}
        for game_name in os.listdir(directory):
            if not os.path.isdir(os.path.join(directory, game_name)):
                continue
            entry = Entry(game_name=game_name)

            for root, dir_names, filenames in os.walk(os.path.join(directory, game_name)):
                root_l = os.path.basename(root).lower()

                # get game.py
                if root_l == game_name.lower():
                    for f in filenames:
                        if f.lower().endswith("game.py"):
                            entry.keras.game_py = os.path.join(root, f)
                            entry.torch.game_py = os.path.join(root, f)

                # check for pytorch files
                if root_l == "pytorch":
                    entry.torch.found = True
                    entry.x += 1
                    for f in filenames:
                        if f.lower().endswith("best.pth.tar"):
                            entry.torch.model_path = os.path.dirname(os.path.join(root, f))
                            entry.torch.model_file = os.path.basename(os.path.join(root, f))
                        if f.lower() == "nnet.py":
                            entry.torch.nnet_py = os.path.join(root, f)

                # check for keras files
                if root_l == "keras":
                    entry.keras.found = True
                    entry.x += 1
                    for f in filenames:
                        if f.lower().endswith("best.h5"):
                            entry.keras.model_path = os.path.dirname(os.path.join(root, f))
                            entry.keras.model_file = os.path.basename(os.path.join(root, f))
                        if f.lower() == "nnet.py":
                            entry.keras.nnet_py = os.path.join(root, f)

            if entry.keras.found or entry.torch.found:
                if len(entry.keras.missing()) == 0 or len(entry.torch.missing()) == 0:
                    result[game_name] = entry
            entry.print()
        return result

    @staticmethod
    def import_class_from_file(file_path, class_name=None):
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
        result = {}
        for entry in self.__path.values():
            if entry.x == 2 or len(entry.torch.missing()) == 0:
                result[entry.game_name] = Importer.import_class_from_file(entry.torch.game_py)
            else:
                result[entry.game_name] = Importer.import_class_from_file(entry.keras.game_py)
        return result

    def __import_funcs(self):
        result = {}
        for name, entry in self.__path.items():
            game: IGame = self.__game_classes[name]()
            nn = None
            if len(entry.torch.missing()) == 0:
                old_std = sys.stdout
                sys.stdout = io.StringIO()  # redirect stdout to nothing
                nn = Importer.import_class_from_file(entry.torch.nnet_py, "NNetWrapper")(game)
                nn.load_checkpoint(entry.torch.model_path, entry.torch.model_file)
                sys.stdout = old_std  # restore old stdout
            elif len(entry.keras.missing()) == 0:
                old_std = sys.stdout
                sys.stdout = io.StringIO()  # redirect stdout to nothing
                nn = Importer.import_class_from_file(entry.keras.nnet_py, "NNetWrapper")(game)
                nn.load_checkpoint(entry.keras.model_path, entry.keras.model_file)
                sys.stdout = old_std  # restore old stdout

            result[name] = {}
            for diff in EDifficulty:
                mcts = MCTS(game, nn, dotdict({'numMCTSSims': diff.value,
                                               'fpu': 0.,
                                               'universes': 1,
                                               'cpuct': 1,
                                               'prob_fullMCTS': 1.,
                                               'forced_playouts': False,
                                               'no_mem_optim': False, }))
                result[name].update({diff: mcts})
        return result


if __name__ == "__main__":
    # For testing purposes
    i = Importer("../Games")
    print(i.get_games())
    print(i.get_ai_func())
