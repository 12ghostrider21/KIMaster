import logging
import time
import os
import re

from coach import Coach

from Games.go.GoGame import GoGame as Game
from Games.go.pytorch.NNet import NNetWrapper as nn
from Tools.utils import dotdict

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
log.addHandler(console_handler)


directory = './temp/'


def find_highest_checkpoint_file(directory):
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


highest_checkpoint_file, highest_iteration = find_highest_checkpoint_file(directory)

if not highest_checkpoint_file or not (os.path.exists(directory + "best.h5") or os.path.exists(directory + "temp.h5")):
    log.error('No checkpoint file or .h5 file found!')
    ld_model = False
    it = 0
else:
    ld_model = True
    it = highest_iteration + 1

args = dotdict({
    'numIters': 100,
    'numEps': 100,  # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,  # Number of game examples to train the neural networks.
    'numMCTSSims': 25,  # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,  # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': directory,
    'load_model': ld_model,  # whether to load an existing model & checkpoint.examples (can be set at True always)
    'load_folder_file': (directory, highest_checkpoint_file),
    'current_iteration': it,
    'numItersForTrainExamplesHistory': 20,
})


def main():
    start_time = time.time()
    log.info('Loading %s...', Game.__name__)
    g = Game()

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)

    if args.load_model:
        log.info('Loading checkpoint "%s%s"...', args.load_folder_file[0], args.load_folder_file[1])
        path = "./temp/"
        file = "best.h5"
        if not os.path.exists(os.path.join(path, file)):
            file = "temp.h5"
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
    print(f"Time: {int(elapsed_time // 3600)}h {int((elapsed_time % 3600) // 60)}m {int((elapsed_time % 3600) % 60)}s")


if __name__ == "__main__":
    main()
