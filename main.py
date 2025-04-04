import logging

import os
os.environ['NUMEXPR_MAX_THREADS'] = '6'
import coloredlogs
import tensorflow as tf
from Coach import Coach
from othello.OthelloGame import  OthelloGame as Game
from othello.keras.NNet import NNetWrapper as nn
from utils import *

log = logging.getLogger(__name__)

coloredlogs.install(level='debug')  # Change this to DEBUG to see more info.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

args = dotdict({
    'numIters': 100,
    'numEps': 60,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 10,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 100000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'arenaCompareToMiniMax':20,
    'cpuct': 1,
    'startIter':0,
    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('temp','temp'),
    'numItersForTrainExamplesHistory': 15,

})


def main():
    with tf.device('CPU:0'):
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


if __name__ == "__main__":
    main()