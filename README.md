<!-- fullWidth: false tocVisible: false tableWrap: false -->

# Joueur de GO - Projet IA

Equipe : Eve Turchet et Matheline Chevalier

# Heuristique

Nous avons commencé par implémenter une heuristique simple qui retourne la différence entre le nombre de pions noirs et le nombre de pions blancs.

# Algorithme Alpha-Beta

Notre IA repose sur l'algorithme d'exploration Alpha-Beta.
Dans cet algorithme, nous simulons les futurs coups où le joueur Noir cherche à maximiser son score tandis que le joueur Blanc cherche à le minimiser.
Comme il est impossible de tout calculer, l'exploration s'arrête à une exploration donnée.
L'exploration est également optimisée grâce à l'élagage : une branche est coupée si le coup d'adversaire est jugée trop défavorable.

# Gestion du temps

Dans la fonction d'initialisation du joueur, on met son champ remaining_time à 2700 secondes (soit 45 minutes).\
Après chaque coup, on soustrait à ce champ le temps qu'a mis l'exécution de la fonction getPlayerMove.

Le temps consacré à un coup dépend du moment où on se place dans le jeu.\
Si le plateau a moins de dix pions, on a fixé le temps de choix du prochain coup à 1 seconde.

Ainsi, on peut réfléchir plus longtemps sur les coups décisifs.\
On calcule d'abord une estimation du nombre de coups qu'il reste à notre joueur (nombre de cases vides du plateau divisé par 2).\
On divise le temps restant au joueur par son nombre de coups restants estimé, ce qui nous donne le temps possible_time.

Pour que le joueur puisse réfléchir plus longtemps au milieu de la partie, là où ses coups sont plus décisifs, on multiplie ce temps par 1.5.\
S'il ne reste pas beaucoup de coups au joueur, il joue pendant possible_time secondes.

Avec cette stratégie, le joueur consomme très peu de temps au début de la partie, beaucoup plus au milieu et un peu moins à la fin.

# Utilisation du Iterative Deepening

Une fois que le joueur connait le temps qu'il peut utiliser pour son coup, il utilise l'Iterative Deepening sur cette période.\
Il commence avec une profondeur de 1, puis de 2, ...\
Si le temps est écoulé, les fonctions deroulementAlphaBeta et find_best_move soulèvent une TimeOutException et retournent None.\
Si c'est le cas, on utilise le coup proposé par la recherche avec la profondeur d'avant.

# Bibliothèque d'ouvertures

Pour améliorer notre joueur, nous utilisons également une bibliothèque d'ouvertures basée sur le fichier **_plays-8x8.json_**.\
Le fichier est chargé lors de l'initialisation du joueur.\
On crée ensuite un dictionnaire d'ouvertures qui ne contient que les suites de mouvements menant à une victoire :

- La clé correspond à l'historique exact de la partie à un instant t
- La valeur est le coup suivant joué par le gagnant de cette partie

A chaque fois qu'un joueur joue, on met à jour l'historique.\
Avant de commencer une itération avec Alpha-Beta, on interroge le dictionnaire avec notre historique actuel :

- Si on connaît le prochain coup gagnant, on le joue instantanément (O(1)).
- Si notre séquence est inconnue, on lance l'algorithme Alpha-Beta.

Cette approche permet d'économiser du temps au niveau du chronomètre en début de partie.
