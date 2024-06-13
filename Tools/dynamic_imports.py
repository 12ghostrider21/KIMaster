class Importer:
    def __init__(self):
        pass

        self.lambdas: dict = {}

    def game_clinet_games(self):
        return {}

    # import all games from /Games folder and create a instance of it
    # import all NNet.py of each game
    # find directory path of .h5 files of each game
    # find name of .h5 file of each game
    # create all lambda functions for ai operation for each difficulty (EDifficulty)
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
