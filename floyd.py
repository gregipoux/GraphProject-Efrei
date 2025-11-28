# floyd.py

from math import inf
from output import print_matrices

def detect_cycle_negatif(L):
    """
    Renvoie True s'il existe un cycle absorbant (cycle de poids négatif).
    Critère : au moins un i tel que L[i][i] < 0 dans la matrice finale.
    """
    n = len(L)
    for i in range(n):
        if L[i][i] < 0:
            return True
    return False


def floyd_warshall(L, P, verbose=True, show_initial=True):
    """
    Implémente l'algorithme de Floyd-Warshall.

    Paramètres :
    - L : matrice des distances (modifiée en place)
    - P : matrice des prédécesseurs (modifiée en place)
    - verbose : si True, affiche les matrices à chaque étape
    - show_initial : si True, affiche l'état initial des matrices

    Retourne :
    - (L, P, cycle_negatif) :
        * L : matrice des plus courts chemins
        * P : matrice des prédécesseurs correspondants
        * cycle_negatif : booléen, True s'il existe un cycle absorbant
    """
    n = len(L)

    if verbose and show_initial:
        print_matrices(L, P, "Initialisation")

    for k in range(n):
        if verbose:
            print(f"=== Début de l'itération k = {k} ===")

        for i in range(n):
            for j in range(n):
                # si pas de chemin i->k ou k->j, on ne peut pas améliorer i->j
                if L[i][k] == inf or L[k][j] == inf:
                    continue

                nouvelle_distance = L[i][k] + L[k][j]

                if nouvelle_distance < L[i][j]:
                    L[i][j] = nouvelle_distance
                    # prédécesseur de j sur le plus court chemin i->j :
                    # on recopie le prédécesseur de j sur le chemin k->j
                    P[i][j] = P[k][j]

        if verbose:
            print_matrices(L, P, f"Après k = {k}")

    cycle_negatif = detect_cycle_negatif(L)

    if verbose:
        if cycle_negatif:
            print("!  Cycle absorbant détecté (cycle de poids négatif).")
        else:
            print("Aucun cycle absorbant détecté.")

    return L, P, cycle_negatif
