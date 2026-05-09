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
import json

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self._remaining_time = 2700

        # Charge la bibliothèque d'ouvertures
        self._opening_book = {}
        try:
            with open("plays-8x8.json", "r") as file:
                games = json.load(file)
                for game in games:
                    moves = game["moves"]
                    winner = game["winner"] # BLACK ou WHITE
                    if winner == "BLACK":
                        win_color = Goban.Board._BLACK
                    else:
                        win_color = Goban.Board._WHITE

                    # Sauvegarde les 10 premiers coups
                    for i in range(min(10, len(moves))):
                        history = tuple(moves[:i]) # tuple immuable une fois créé → peut être utilisé comme clé de dictionnaire
                        next_move = moves[i]
                        
                        if history not in self._opening_book:
                            self._opening_book[history] = []
                        
                        if i % 2 == 0:
                            turn_color = Goban.Board._BLACK 
                        else:
                            turn_color = Goban.Board._WHITE
                        if turn_color == win_color: # si le coup mène à une victoire pour le joueur de ce tour, on le garde
                            self._opening_book[history].append(next_move) 
        
        except Exception as e:
            print("Erreur de chargement des ouvertures:", e)

    def getPlayerName(self):
        return "Mathelin'eirb Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        
        # Essaie de lire le coup depuis la bibliothèque
        current_history = tuple(self._history)
        if current_history in self._opening_book and len(self._opening_book[current_history]) > 0:
            best_move_str = choice(self._opening_book[current_history])
            print("Ouverture trouvée ! Je joue :", best_move_str)
            self._history.append(best_move_str)
            move_flat = Goban.Board.name_to_flat(best_move_str)
            self._board.push(move_flat)
            return best_move_str

        # Si pas d'ouverture trouvée, on utilise alpha-beta
        start_time = time.time()

        nb_stones = 0
        for line in range(self._board._BOARDSIZE):
            for case in range(self._board._BOARDSIZE):
                p = self._board[self._board.flatten((case, self._board._BOARDSIZE - line - 1))]
                if p == self._board._BLACK or p == self._board._WHITE:
                    nb_stones += 1

        nb_moves_estimation = max(1, (64 - nb_stones) // 2) # Max (1, x) pour être sur de pas diviser par 0 
        possible_time = self._remaining_time / nb_moves_estimation

        if nb_stones < 10:
            time_limit = 1.0 # On réfléchit 1 sec pour les premiers coups
        elif nb_stones < 45:
            time_limit = possible_time * 1.5
        else:
            time_limit = possible_time

        # On évite de réfléchir - de 1 sec et + de 1 min
        time_limit = max(1.0, min(time_limit, 60.0))
        
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

        time_spent = time.time() - start_time
        self._remaining_time -= time_spent
        
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
        self._history.append(move) # ajout le coup de l'adversaire à l'historique
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)
        self._remaining_time = 2700
        self._history = [] # historique des coups pioches

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



