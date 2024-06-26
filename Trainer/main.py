import logging
import time
import os
import re
from Tools.dynamic_imports import Importer
from coach import Coach
from Tools.utils import dotdict
from dataclasses import dataclass, field

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
log.addHandler(console_handler)


@dataclass
class EntryGame:
    key: str = field(default="")
    game_path: str | None = field(default=None)
    nn: str | None = field(default=None)


@dataclass
class Entry:
    key: str | None = field(default=None)
    game_path: str | None = field(default=None)
    keras_nn: str | None = field(default=None)
    pytorch_nn: str | None = field(default=None)

    def check(self):
        result = []
        if self.game_path is not None and self.keras_nn is not None:
            result.append(EntryGame(f"{self.key}_keras", self.game_path, self.keras_nn))
        if self.game_path is not None and self.pytorch_nn is not None:
            result.append(EntryGame(f"{self.key}_pytorch", self.game_path, self.pytorch_nn))
        return result


class Trainer:
    def __init__(self, directory: str):
        self.directory = os.path.abspath(directory)
        self.saves = "./checkpoints/"
        self.available_games = self.find_games(self.directory)

    def find_highest_checkpoint_file(self, directory):
        if not os.path.isdir(directory):
            return None, None
        files = os.listdir(directory)

        # regex to extract the checkpoint index
        pattern = re.compile(r'checkpoint_(\d+)\.pth\.tar\.examples')

        highest_num = -1
        highest_file = None

        # go through all files
        for file in files:
            match = pattern.match(file)
            if match:
                # extract num from file name
                num = int(match.group(1))
                if num > highest_num:
                    highest_num = num
                    highest_file = file

        return highest_file, highest_num

    def find_games(self, directory: str):
        games = []
        for game in os.listdir(directory):
            e = Entry(key=game)
            a = os.path.join(directory, game)
            if not os.path.isdir(a):
                continue
            for folder in os.listdir(a):
                b = os.path.join(a, folder)
                if folder.lower().endswith("game.py"):
                    e.game_path = b
                if folder.lower().endswith("keras"):
                    for f in os.listdir(b):
                        if f.lower() == "nnet.py":
                            e.keras_nn = os.path.join(b, f)
                if folder.lower().endswith("pytorch"):
                    for f in os.listdir(b):
                        if f.lower() == "nnet.py":
                            e.pytorch_nn = os.path.join(b, f)
            for i in e.check():
                games.append(i)
        return games

    def run(self):
        entered: int = 0  # dummy for user input
        print("\033[95mTrainer started.\033[90m")
        if len(self.available_games) == 0:
            print(f"\033[91mNo available games in [\033[93m{self.directory}\033[91m]\033[90m")
            exit(0)
        # select game
        while True:
            for i, game_e in enumerate(self.available_games):
                print(f"\033[94m[\033[93m{i}\033[94m] \033[92m{game_e.key.upper()}\033[0m")
            try:
                entered = int(input(f"\033[95mSelect game to train [\033[93m-1\033[95m to exit]:"))
                if entered in range(0, len(self.available_games)):
                    break
                if entered == -1:
                    exit(0)
            except ValueError:
                pass

        # find checkpoint
        game_entry = self.available_games[entered]
        print(f"\033[95mSelected: [\033[92m{game_entry.key}\033[95m] importing Game.py and NNet.py ...\033[0m")
        try:
            game_class = Importer.import_class_from_file(game_entry.game_path)()
            nn_class = Importer.import_class_from_file(game_entry.nn, "NNetWrapper")(game_class)
        except Exception as e:
            print("\033[91mSomething went wrong with import selected game classes")
            print("\033[93m", e, "\033[0m")
            exit(1)
        # find last checkpoint
        path = f"{self.saves}/{game_entry.key}/"
        highest_checkpoint_file, highest_iteration = self.find_highest_checkpoint_file(path)
        if not highest_checkpoint_file or not (os.path.exists(path + "best.h5")
                                               or os.path.exists(path + "temp.h5")
                                               or os.path.exists(path + "best.pth.tar")
                                               or os.path.exists(path + "temp.pth.tar")):
            print('\033[91mNo checkpoint file or .h5 /.pth.tar file found!\033[0m')
            ld_model = False
            it = 0
        else:
            ld_model = True
            it = highest_iteration + 1

        while True:
            try:
                entered = int(
                    input(f"\033[95mNumIters? (\033[93mdefault=100\033[95m) [\033[93m-1\033[95m to exit]:\033[0m"))
                if entered == -1:
                    exit(0)
                break
            except ValueError:
                pass
        iter = entered
        while True:
            try:
                entered = int(
                    input(f"\033[95mNumEps? (\033[93mdefault=100\033[95m) [\033[93m-1\033[95m to exit]:\033[0m"))
                if entered == -1:
                    exit(0)
                break
            except ValueError:
                pass
        eps = entered
        while True:
            try:
                entered = int(
                    input(f"\033[95mArenaCompare? (\033[93mdefault=40\033[95m) [\033[93m-1\033[95m to exit]:\033[0m"))
                if entered == -1:
                    exit(0)
                if entered < 2:
                    print("\033[91mAt least 2 ArenaCompare!\033[0m")
                    continue
                break
            except ValueError:
                pass
        arena_compare = entered
        args = dotdict({
            'numIters': iter,
            'numEps': eps,  # Number of complete self-play games to simulate during a new iteration.
            'tempThreshold': 15,
            'updateThreshold': 0.6,
            # During arena playoff, new neural net will be accepted if threshold or more of games are won.
            'maxlenOfQueue': 200000,  # Number of game examples to train the neural networks.
            'numMCTSSims': 25,  # Number of games moves for MCTS to simulate.
            'arenaCompare': arena_compare,
            # Number of games to play during arena play to determine if new net will be accepted.
            'cpuct': 1,

            'checkpoint': path,
            'load_model': ld_model,
            # whether to load an existing model & checkpoint.examples (can be set at True always)
            'load_folder_file': (path, highest_checkpoint_file),
            'current_iteration': it,
            'numItersForTrainExamplesHistory': 20,
        })

        start_time = time.time()
        print('\033[95mLoading %s...\033[93m', game_class.__class__.__name__, "\033[0m")
        g = game_class

        print('\033[95mLoading %s...\033[93m', nn_class.__class__.__name__, "\033[0m")
        nnet = nn_class

        if args.load_model:
            log.info('Loading checkpoint "%s%s"...', args.load_folder_file[0], args.load_folder_file[1])
            path = self.saves + game_entry.key
            file = ""
            if "keras" in game_entry.nn:
                file = "best.h5"
            if "pytorch" in game_entry.nn:
                file = "best.pth.tar"
            if not os.path.exists(os.path.join(path, file)):
                if "keras" in game_entry.nn:
                    file = "temp.h5"
                if "pytorch" in game_entry.nn:
                    file = "temp.pth.tar"
            nnet.load_checkpoint(path, file)
        else:
            log.warning('Not loading a checkpoint!')

        log.info('Loading the Coach...')
        c = Coach(g, nnet, args)

        if args.load_model:
            log.info("Loading 'trainExamples' from file...")
            c.loadTrainExamples()

        log.info('Starting the learning process 🎉')
        c.learn()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time: {int(elapsed_time // 3600)}h"
              f" {int((elapsed_time % 3600) // 60)}m"
              f" {int((elapsed_time % 3600) % 60)}s")


if __name__ == "__main__":
    # if multiple games training at once -> threading
    t = Trainer("../Games")
    t.run()
