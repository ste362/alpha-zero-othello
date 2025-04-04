import math

import numpy as np


class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanOthelloPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                print("[", int(i/self.game.n), int(i%self.game.n), end="] ")
        while True:
            input_move = input()
            input_a = input_move.split(" ")
            if len(input_a) == 2:
                try:
                    x,y = [int(i) for i in input_a]
                    if ((0 <= x) and (x < self.game.n) and (0 <= y) and (y < self.game.n)) or \
                            ((x == self.game.n) and (y == 0)):
                        a = self.game.n * x + y if x != -1 else self.game.n ** 2
                        if valid[a]:
                            break
                except ValueError:
                    # Input needs to be an integer
                    'Invalid integer'
            print('Invalid move')
        return a


class GreedyOthelloPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a]==1:
                nextBoard, _ = self.game.getNextState(board, 1, a)
                score = self.game.getScore(nextBoard, 1)
                candidates += [(-score, a)]
        candidates.sort()
        return candidates[0][1]





class MiniMaxPlayer:


    def __init__(self, game):
        self.game = game

    def __str__(self):
        return "MiniMax"


    def play(self, board):
        move=h_alphabeta_search_zero(self.game,board)[1]

        return move




def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda game, state, depth: depth > d

infinity = math.inf





def h_alphabeta_search_zero(game, state,cutoff=cutoff_depth(4),h=lambda g,s,p: g.getScore(s,p)):


    player = 1


    def max_value(state, player,alpha, beta, depth):
        if game.getGameEnded(state,player):
            return -game.getScore(state, player), None
        if cutoff(game, state, depth):
            #print(h(state, player))
            return -h(game,state, player), None
        v, move = -infinity, None
        val_moves=game.getValidMoves(state,player)
        for a in range(len(val_moves)):
            if val_moves[a]==1:
                v2, _ = min_value(game.getNextState(state,player, a)[0], -player, alpha, beta, depth+1)
                if v2 > v:
                    v, move = v2, a
                    alpha = max(alpha, v)
                if v >= beta:
                    return v, move
        return v, move


    def min_value(state, player,alpha, beta, depth):
        if game.getGameEnded(state,player):
            return game.getScore(state, player), None
        if cutoff(game, state, depth):
            return h(game,state, player), None
        v, move = +infinity, None
        val_moves=game.getValidMoves(state,player)
        for a in range(len(val_moves)):
            if val_moves[a]==1:
                v2, _ = max_value(game.getNextState(state,player, a)[0], -player, alpha, beta, depth + 1)
                if v2 < v:
                    v, move = v2, a
                    beta = min(beta, v)
                if v <= alpha:
                    return v, move
        return v, move

    return max_value(state, player,-infinity, +infinity, 0)