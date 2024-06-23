import logging
import time

from coach import Coach

#from Games.connect4.Connect4Game import Connect4Game as Game
#from Games.connect4.pytorch.NNet import NNetWrapper as nn

from Games.tictactoe.TicTacToeGame import TicTacToeGame as Game
from Games.tictactoe.keras.NNet import NNetWrapper as nn

from Tools.utils import dotdict

log = logging.getLogger(__name__)


args = dotdict({
    'numIters': 1,
    'numEps': 1,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 20,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './temp/ttt_keras/',
    'load_model': False,
    'load_folder_file': ('./temp/connect4_pytorch/','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})


def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return int(hours), int(minutes), seconds

def main():
    start = time.time()
    log.info('Loading %s...', Game.__name__)
    g = Game(6)

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)

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
    end = time.time()
    hours, minutes, seconds = seconds_to_hms(end - start)
    print(f"Training Took: {hours}h {minutes}m {seconds:.2f}s")



if __name__ == "__main__":
    main()
