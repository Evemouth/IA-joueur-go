# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban 
from random import choice
from playerInterface import *
import methods
import copy

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    def getPlayerName(self):
        return "Mathelin'eirb Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        
        start_time = time.time()
        time_limit = 5.0 # 5 secondes par coup : à revoir pour faire la strat du prof selon l'avancement du jeu
        
        legals = self._board.legal_moves()
        move = legals[0] # Si on a pas le temps de faire l'iterative deepening, on fait le 1er coup possible
        depth = 1

        while True:
            time_spent = time.time() - start_time
            if (time_spent > time_limit):
                break
            board_copy = copy.deepcopy(self._board)
            new_move = methods.find_best_move(board_copy, depth, start_time, time_limit)

            if new_move is None : # Si on a pas eu le temps de calculer jusqu'au bout
                break

            else : 
                move = new_move
                print("Fin calcul profondeur ", depth)
                depth += 1
        
        self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



