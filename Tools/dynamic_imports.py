import importlib.util
import os
from os.path import splitext, basename, join, split
from os import walk
import sys

from Tools.mcts import MCTS
from Tools.utils import dotdict
from Tools.i_game import IGame
from Tools.Game_Config.difficulty import EDifficulty

class Importer:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Importer, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def init_nn(game, nnet, h5_path, difficulty: EDifficulty):
        h5_folder_file = split(h5_path)
        folder = h5_folder_file[0]
        file = h5_folder_file[1]
        nn = nnet(game)
        nn.load_checkpoint(folder, file)
        args = dotdict({'numMCTSSims': difficulty.value, 'cpuct': 1.0})
        mcts = MCTS(game, nn, args)
        return mcts
        

    def __init__(self):
        pass
        # get all relevant files related to games
        self.games, game_pys, game_nnet_files, game_h5s = Importer.crawl_game_files()
        print(f"{self.games=}")
        print(f"{game_pys=}")
        print(f"{game_nnet_files=}")
        print(f"{game_h5s=}")
        # get all game classes
        self.game_classes = {game: Importer.import_class_from_file(game_pys[game]) for game in self.games}

        # import NNet.py of each game
        game_nnets = {game: Importer.import_class_from_file(game_nnet_files[game], 'NNetWrapper') for game in
                      self.games}

        # CREATE LAMBDAS
        # 1) generate a list of games and difficulty pairs
        game_diff_pairs:list[tuple[str, EDifficulty]] = [(game, diff) for game in self.games for diff in EDifficulty]
        
        # 2) generate the monte carlo tree search for each game and each difficulty
        wrapper_for_init_nn = lambda game, diff : Importer.init_nn(self.game_classes[game](), game_nnets[game], game_h5s[game], diff)
        game_mcts = {pair:wrapper_for_init_nn(pair[0], pair[1]) for pair in game_diff_pairs}
        
        # 3) generate functions for each game and difficulty
        self.__game_funcs = {pair: lambda x: game_mcts[pair].getActionProb(x, temp=0) for pair in game_diff_pairs}

    def game_client_games(self) -> dict[str, IGame]:
        return {game:self.game_classes[game]() for game in self.games}

    def server_call(self):
        pass
    
    def get_game_func(self, game_name:str, difficulty:EDifficulty):
        return self.__game_funcs(game_name, difficulty)

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
    def crawl_game_files() -> tuple[list[str], dict[str:str], dict[str:str], dict[str:str]]:
        """
    Crawl the game files and categorize them into different dictionaries based on their types.

    Returns:
        tuple: A tuple containing four elements:
            - games (list[str]): List of all game names found in the directory.
            - game_pys (dict[str, str]): Dictionary with game names as keys and paths to their Game.py files as values.
            - game_nnets (dict[str, str]): Dictionary with game names as keys and paths to their NNet.py files as values.
            - game_h5s (dict[str, str]): Dictionary with game names as keys and paths to their .h5 files as values.

    Raises:
        Warning: If multiple directories with identical names are found in the GameDirectory.
    """
        # init return values
        games: set[str] = {game for game in os.listdir("/app/Games")}
        game_pys: dict[str, str] = {}
        game_nnets: dict[str, str] = {}
        game_h5s: dict[str, str] = {}
        results = (games, game_pys, game_nnets, game_h5s)

        # init list for those games to exclude from result
        ignored: list[str] = []

        for root, dir_names, file_names in walk("/app/Games"):
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
                print(
                    f"WARNING: the game {current_game} seems to exist several times. To prevent unpredictable behaviour {current_game} will be ignored. This Error is caused if there are multiple directories with identical names in your GameDirectory.")
                for game in current_game:
                    ignored.append(game)
                    
        
        # ignore games where Game.py, NNet.py and.h5 files; could not be found
        for game in games:
            for element in [res for res in results if res is not games]:
                if game not in element:
                    ignored.append(game)
                    print(f"WARNING: A required File is missing for the game {game}. The path of this file is expected to be in this collection {element}. To prevent unstable behaviour the game {game} will be Ignored.")
                
        # remove ignored games
        for ignored_game in ignored:
            for r in results:
                
                if isinstance(r, dict):
                    r.pop(ignored_game, None)
                elif isinstance(r, set):
                    r.discard(ignored_game)
                
        return results

    @staticmethod
    def import_class_from_file(file_path, class_name = None):
        module_name: str = splitext(basename(file_path))[0]
        # try to resolve automaticly 
        class_name = module_name if class_name == None else class_name
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Return the class from the module
        if hasattr(module, class_name):
            return getattr(module, class_name)
        else:
            raise ImportError(f"Class {class_name} not found in {file_path}. To make sure your Game can be found, name the class the same as the Game.py file, (but with out the Game.py). The file for the neural net must be named NNet.py")

    @staticmethod
    def test(*args, **kwargs):
        print(args, kwargs)

    '''
    # USE THIS IF ABOVE DOES NOT WORK !!!!!!
    
    @staticmethod
    def import_class_from_file(filepath: str, class_name: str):
        spec = importlib.util.spec_from_file_location(class_name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Find the class with case-insensitive match
        for attr in dir(module):
            if attr.lower() == class_name.lower():
                return getattr(module, attr)

        raise AttributeError(f"Class {class_name} not found in {filepath}")
    
    @staticmethod
    def import_class_from_file(filepath: str):
        class_name = splitext(basename(filepath))[0]
        Importer.import_class_from_file(filepath, class_name)'''

    # DONE import all games from /Games folder and create a instance of it
    # DONE import all NNet.py of each game
    # DONE: find directory path of .h5 files of each game
    # DONE: find name of .h5 file of each game
    # DONE: create all lambda functions for ai operation for each difficulty (EDifficulty)
    # define game_client specific method for imports if necessary
    # loading as fast as possible login of game_client can be delayed
    # define server specific method for imports if necessary

    """
    import os
    import sys
    import glob
    import importlib.util
    
    # Der Pfad zu deinem Ordner
    ordner_pfad = os.path.join(os.getcwd(), 'mein_ordner')
    
    # Finde alle Python-Dateien im Ordner
    python_dateien = glob.glob(os.path.join(ordner_pfad, '*.py'))
    
    # Gehe durch alle gefundenen Python-Dateien
    for datei in python_dateien:
        # Lade die Modul-Spezifikation aus der Datei
        modul_name = os.path.basename(datei)[:-3]
        spezifikation = importlib.util.spec_from_file_location(modul_name, datei)
        modul = importlib.util.module_from_spec(spezifikation)
        spezifikation.loader.exec_module(modul)
    
        # Prüfe, ob die Klasse in dem Modul existiert
        if hasattr(modul, 'MeineKlasse'):
            MeineKlasse = getattr(modul, 'MeineKlasse')
            break
    else:
        raise ImportError("MeineKlasse wurde nicht gefunden.")
    
    # Erstelle eine Instanz der Klasse
    objekt = MeineKlasse("Max")
    
    # Rufe die Methode auf und drucke das Ergebnis
    print(objekt.begruessen())

    
    """

    """
    @staticmethod
    def import_class_from_file(filepath: str, class_name: str):
        spec = importlib.util.spec_from_file_location(class_name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Find the class with case-insensitive match
        for attr in dir(module):
            if attr.lower() == class_name.lower():
                return getattr(module, attr)

        raise AttributeError(f"Class {class_name} not found in {filepath}")

    def find_and_import_classes(self, games_folder: str):
        imports = {}

        for game_name in os.listdir(games_folder):
            game_path = os.path.join(games_folder, game_name)
            if os.path.isdir(game_path):
                imports[game_name] = {}

                # Import Game classes (files ending with Game.py)
                for file_name in os.listdir(game_path):
                    if file_name.endswith('Game.py'):
                        game_file = os.path.join(game_path, file_name)
                        if os.path.isfile(game_file):
                            try:
                                game_class = self.import_class_from_file(game_file, file_name.replace(".py", ""))
                                imports[game_name]['Game'] = game_class()
                            except (FileNotFoundError, AttributeError) as e:
                                print(f"Could not import Game class from {game_file}: {e}")

                # Import NNetWrapper class from keras/NNet.py
                keras_file = os.path.join(game_path, 'keras', 'NNet.py')
                if os.path.isfile(keras_file):
                    try:
                        keras_class = self.import_class_from_file(keras_file, 'NNetWrapper')
                        imports[game_name]['NNetWrapper'] = keras_class
                    except (FileNotFoundError, AttributeError) as e:
                        print(f"Could not import NNetWrapper class from {keras_file}: {e}")

                # import Keras folder and model
                keras_model = os.path.join(game_path, 'keras', 'best.h5')
                if os.path.isfile(keras_model):
                    file = os.path.basename(keras_model)
                    folder = os.path.dirname(os.path.abspath(keras_model))
                    imports[game_name]["folder"] = folder
                    imports[game_name]["file"] = file

                # Import NNetWrapper class from pytorch/NNet.py
                pytorch_file = os.path.join(game_path, 'pytorch', 'NNet.py')
                if os.path.isfile(pytorch_file):
                    try:
                        pytorch_class = self.import_class_from_file(pytorch_file, 'NNetWrapper')
                        imports[game_name]['NNetWrapper'] = pytorch_class
                    except (FileNotFoundError, AttributeError) as e:
                        print(f"Could not import NNetWrapper class from {pytorch_file}: {e}")

                # import pytorch folder and model
                torch_model = os.path.join(game_path, 'pytorch', 'best.h5')
                if os.path.isfile(torch_model):
                    file = os.path.basename(torch_model)
                    folder = os.path.dirname(os.path.abspath(torch_model))
                    imports[game_name]["folder"] = folder
                    imports[game_name]["file"] = file
        return imports

    def create_lambda(self):
        print("Loading Ai models...")
        results = {}
        ignored_games = []
        # save original stdout
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        try:
            # redirect stdout to silent mode
            sys.stdout = open(os.devnull, 'w')
            sys.stderr = open(os.devnull, 'w')
            for k, v in self.imports.items():
                game = self.imports[k].get("Game")
                network_class = self.imports[k].get("NNetWrapper")  # get the right NNet
                h5_folder = self.imports[k].get("folder")  # get the .h5 trained model path
                h5_file = self.imports[k].get("file")  # get the .h5 file
                if h5_folder and h5_file:
                    for difficulty in EDifficulty:
                        mcts = self.init_nn(game, network_class, h5_folder, h5_file, difficulty)
                        if k not in results:
                            results[k] = {}
                        results[k][difficulty] = lambda x: mcts.getActionProb(x, temp=0)
                else:
                    ignored_games.append(f"For '{game}' no best.h5 was found. Ignoring it.")
        finally:
            # set stdout back to original
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            print("Loading Ai models done.")
        return results
    
    """

    """
    loading and creation of MCTS function
    
    
    def init_nn(game, nnet, folder: str, file: str, difficutly: EDifficulty):
        nn = nnet(game)
        nn.load_checkpoint(folder, file)
        args = dotdict({'numMCTSSims': difficutly.value, 'cpuct': 1.0})
        mcts = MCTS(game, nn, args)
        return mcts
    
    """

    """
     copy of game_ client opperation
     
     
    @staticmethod
    def import_game_classes(directory):
        pattern: str = "Game.py"
        imported_classes = {}

        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(pattern):
                    module_name = filename[:-3]
                    file_path = os.path.join(root, filename)

                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        name = name.replace("Game", "").lower()
                        if obj.__module__ == module_name:
                            imported_classes[name] = obj
                            print("Imported: ", name)
        return imported_classes
    """