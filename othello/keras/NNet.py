import argparse
import os
import shutil
import time
import random
import numpy as np
import math
import sys


sys.path.append('../..')
from utils import *
from NeuralNet import NeuralNet
import tensorflow as tf
from keras.callbacks import CSVLogger
import argparse

from .OthelloNNet import OthelloNNet as onnet

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 128,
    'num_channels': 128,
})

class NNetWrapper(NeuralNet):
    def __init__(self, game):
        self.nnet = onnet(game, args)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        with tf.device('GPU:0'):
            input_boards, target_pis, target_vs = list(zip(*examples))
            input_boards = np.asarray(input_boards)
            target_pis = np.asarray(target_pis)
            target_vs = np.asarray(target_vs)

            csv_logger = CSVLogger('log.csv', append=True, separator=';')
            self.nnet.model.fit(x = input_boards, y = [target_pis, target_vs], batch_size = args.batch_size, epochs = args.epochs,callbacks=[csv_logger])

    def predict(self, board):
        """
        board: np array with board
        """

        #print(get_available_devices())



        # timing
        start = time.time()

        # preparing input
        board = board[np.newaxis, :, :]

        # run
        pi, v = self.nnet.model.predict_on_batch(board)

        #print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return pi[0], v[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # change extension
        filename = filename.split(".")[0] + ".h5"

        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # change extension
        filename = filename.split(".")[0] + ".h5"

        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise("No model in path {}".format(filepath))

        self.nnet.model.load_weights(filepath)
