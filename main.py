import logging
import coloredlogs

""" Othello
from Coach import Coach
from othello.OthelloGame import OthelloGame as Game
from othello.pytorch.NNet import NNetWrapper as nn
from utils import *
"""

from Coach import Coach
from connect4.Connect4Game import Connect4Game as Game
from connect4.keras.NNet import NNetWrapper as nn
from utils import *

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.

args = dotdict({
    'numIters': 5,           # 5 times numEps (currently 15) = 75 games played
    'numEps': 15,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        # after 15 states/ nodes evaluated, switching from exploration to exploitation
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won (currently at least 60% must be won).
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate. (25-times search() called => 25 states/ nodes evaluated)
    'arenaCompare': 20,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,   # numItersForTrainExamplesHistory = maximum number of 'iterations' that
                                   # game episodes are kept in queue. After that last is popped and new one is added.

})


def main():
    log.info('Loading %s...', Game.__name__)
    # g = Game(6) Othello
    g = Game()

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)  # nn alias for NNetWrapper

    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file[0], args.load_folder_file[1])
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()


if __name__ == "__main__":
    main()