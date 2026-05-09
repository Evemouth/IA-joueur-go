# Joueur de GO - Projet IA
Equipe : Eve Turchet et Matheline Chevalier

# Heuristique
Nous avons commencé par implémenter une heuristique simple qui retourne la différence entre le nombre de pions noirs et le nombre de pions blancs.

# Gestion du temps
Dans la fonction d'initialisation du joueur, on met son champ remaining_time à 2700 secondes (soit 45 minutes).
Après chaque coup, on soustrait à ce champ le temps qu'a mis l'exécution de la fonction getPlayerMove.

Le temps consacré à un coup dépend du moment où on se place dans le jeu.
Si le plateau a moins de dix pions, on a fixé le temps de choix du prochain coup à 1 seconde.

Ainsi, on peut réfléchir plus longtemps sur les coups décisifs.
On calcule d'abord une estimation du nombre de coups qu'il reste à notre joueur (nombre de cases vides du plateau divisé par 2).
On divise le temps restant au joueur par son nombre de coups restants estimé, ce qui nous donne le temps possible_time.

Pour que le joueur puisse réfléchir plus longtemps au milieu de la partie, là où ses coups sont plus décisifs, on multiplie ce temps par 1.5.
S'il ne reste pas beaucoup de coups au joueur, il joue pendant possible_time secondes.

Avec cette stratégie, le joueur consomme très peu de temps au début de la partie, beaucoup plus au milieu et un peu moins à la fin.

# Utilisation du Iterative Deepening
Une fois que le joueur connait le temps qu'il peut utiliser pour son coup, il utilise l'Iterative Deepening sur cette période.
Il commence avec une profondeur de 1, puis de 2, ...
Si le temps est écoulé, les fonctions deroulementAlphaBeta et find_best_move soulèvent une TimeOutException et retournent None.
Si c'est le cas, on utilise le coup proposé par la recherche avec la profondeur d'avant.