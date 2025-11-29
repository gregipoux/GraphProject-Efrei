# graph.py
# Structure de données pour représenter un graphe orienté valué
# On stocke les distances dans L et les prédécesseurs dans P

from math import inf

class Graph:
    """
    Représentation d'un graphe orienté valué.
    Utilise une matrice de distances L et une matrice de prédécesseurs P.
    """

    def __init__(self, n):
        """
        n : nombre de sommets (0, 1, ..., n-1)
        """
        self.n = n

        # Matrice des distances : L[i][j] = coût du chemin i -> j
        # On initialise tout à inf (pas de chemin), sauf L[i][i] = 0
        self.L = [[inf] * n for _ in range(n)]
        for i in range(n):
            self.L[i][i] = 0

        # Matrice des prédécesseurs : P[i][j] = prédécesseur de j sur un plus court chemin depuis i
        # On initialise tout à None, sauf P[i][i] = i
        self.P = [[None] * n for _ in range(n)]
        for i in range(n):
            self.P[i][i] = i

    def add_arc(self, u, v, w):
        """
        Ajoute / met à jour l'arc u -> v de poids w.
        u, v : int (indices de sommets)
        w : int (poids, peut être négatif, nul ou positif)
        """
        self.L[u][v] = w
        # Le prédécesseur de v sur le chemin direct u->v est u
        self.P[u][v] = u
