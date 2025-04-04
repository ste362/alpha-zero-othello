import Arena
from MCTS import MCTS
from othello import OthelloPlayers
from othello.OthelloGame import OthelloGame
from othello.OthelloPlayers import HumanOthelloPlayer, RandomPlayer, GreedyOthelloPlayer

from othello.keras.NNet import NNetWrapper as NNet
import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
with tf.device('CPU:0'):
    g = OthelloGame(6)


    # all players
    rp = RandomPlayer(g).play
    gp = GreedyOthelloPlayer(g).play
    hp = HumanOthelloPlayer(g).play
    minimax=OthelloPlayers.MiniMaxPlayer(g).play



    # nnet players

    n1 = NNet(g)
    n1.load_checkpoint('temp_6','best.h5')
    args1 = dotdict({'numMCTSSims':25, 'cpuct':1.0})
    mcts1 = MCTS(g, n1, args1)
    n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))




    n2 = NNet(g)
    #n2.load_checkpoint('temp', 'best.h5')
    args2 = dotdict({'numMCTSSims': 25, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp= 0))




    arena = Arena.Arena(n1p, minimax, g, display=OthelloGame.display)
    x,y,_=arena.playGames(10, verbose=False)
    print("neural",x, "minimax",y)
