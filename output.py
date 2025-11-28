# output.py

from math import inf

def print_matrix(M, name="M"):
    """
    Affiche une matrice M avec un nom.
    """
    n = len(M)
    print(f"\n{name} =")
    # en-tête colonnes
    print("      ", end="")
    for j in range(n):
        print(f"{j:>6}", end="")
    print()
    print("     " + "-" * (6 * n))

    for i in range(n):
        print(f"{i:>3} |", end=" ")
        for j in range(n):
            val = M[i][j]
            if val is None:
                s = "None"
            elif val == inf:
                s = "∞"
            else:
                s = str(val)
            print(f"{s:>6}", end="")
        print()


def print_matrices(L, P, step_desc=""):
    """
    Affiche les matrices L (distances) et P (prédécesseurs) pour une étape donnée.
    """
    print("\n" + "=" * 50)
    if step_desc:
        print(f"Étape : {step_desc}")
    print_matrix(L, "L (distances)")
    print_matrix(P, "P (prédécesseurs)")
    print("=" * 50 + "\n")


def reconstruct_path(P, start, end):
    """
    Reconstruit un plus court chemin de start à end à partir de la matrice P.
    Retourne une liste de sommets [start, ..., end] ou None si pas de chemin.
    """
    if P[start][end] is None:
        return None

    chemin = [end]
    j = end
    while j != start:
        j = P[start][j]
        if j is None:
            # cas si on n'arrive pas à remonter
            return None
        chemin.append(j)

    chemin.reverse()
    return chemin


def print_path_and_distance(L, P, start, end):
    """
    Affiche un chemin et sa distance totale.
    """
    path = reconstruct_path(P, start, end)
    if path is None:
        print(f"Aucun chemin de {start} à {end}.")
    else:
        distance = L[start][end]
        path_str = " -> ".join(str(v) for v in path)
        print(f"Chemin de {start} à {end} : {path_str} (valeur = {distance})")
