# main.py

from interface import choose_graph_file, ask_for_paths
from loader import load_graph_from_file
from floyd import floyd_warshall

def main():
    print("=== Projet SM501 : Algorithme de Floyd-Warshall ===")

    while True:
        path = choose_graph_file("graphs")
        if path is None:
            print("Arrêt du programme.")
            break

        print(f"\nChargement du graphe depuis : {path}")
        try:
            g = load_graph_from_file(path)
        except Exception as e:
            print(f"Erreur lors du chargement du graphe : {e}")
            continue

        print(f"Graphe chargé avec {g.n} sommets.")
        print("Affichage de la matrice initiale et exécution de Floyd-Warshall...\n")

        # exécution de Floyd-Warshall (avec affichage des matrices intermédiaires)
        L, P, cycle_negatif = floyd_warshall(g.L, g.P, verbose=True)

        if cycle_negatif:
            print("\nLe graphe contient au moins un circuit absorbant.")
            print("Les plus courts chemins ne sont pas définis (cycle de poids négatif).")
        else:
            print("\nAucun circuit absorbant détecté.")
            ask_for_paths(L, P)

        # Recommencer avec un autre graphe ?
        rep = input("\nVoulez-vous analyser un autre graphe ? (o/n) ").strip().lower()
        if rep not in ("o", "oui"):
            print("Fin du programme.")
            break


if __name__ == "__main__":
    main()
