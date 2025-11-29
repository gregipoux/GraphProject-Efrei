"""Exemple d'application réelle de l'algorithme de Floyd-Warshall.

Ce script met en scène un réseau logistique multi-entrepôts et illustre
l'utilisation du calcul de plus courts chemins pour identifier les itinéraires
les plus rapides entre chaque plateforme régionale.
"""

from pathlib import Path
from loader import load_graph_from_file
from floyd import floyd_warshall
from output import reconstruct_path

# Fichier de données utilisé pour l'exemple
GRAPH_FILE = Path("graphs/g14_application.txt")

# Association sommet -> description lisible
CITY_LABELS = {
    0: "Lille (Haut-de-France)",
    1: "Paris (Île-de-France)",
    2: "Nantes (Pays de la Loire)",
    3: "Lyon (Auvergne-Rhône-Alpes)",
    4: "Marseille (Provence-Alpes-Côte d'Azur)",
    5: "Toulouse (Occitanie)",
    6: "Bordeaux (Nouvelle-Aquitaine)",
    7: "Strasbourg (Grand Est)",
    8: "Rennes (Bretagne)",
    9: "Nice (Provence-Alpes-Côte d'Azur)",
    10: "Clermont-Ferrand (Auvergne-Rhône-Alpes)",
    11: "Montpellier (Occitanie)",
}


# Quelques paires emblématiques à commenter dans le rapport
OD_QUERIES = [
    (0, 9),   # Lille -> Nice
    (5, 9),   # Toulouse -> Nice
    (8, 4),   # Rennes -> Marseille
    (7, 11),  # Strasbourg -> Montpellier
]


def describe_network(n_vertices: int, n_edges: int) -> None:
    """Affiche un résumé synthétique du réseau étudié."""
    print("\n=== RÉSUMÉ DU RÉSEAU LOGISTIQUE ===")
    print(f"Nombre de plateformes : {n_vertices}")
    print(f"Nombre d'itinéraires directs modélisés : {n_edges}")
    print("Les sommets représentent des hubs régionaux interconnectés par des liaisons routières.")

    print("\nCorrespondance des sommets :")
    for idx in range(n_vertices):
        print(f"  {idx:>2} → {CITY_LABELS.get(idx, 'Hub inconnu')}")


def print_sample_paths(L, P) -> None:
    """Affiche quelques plus courts chemins commentés."""
    print("\n=== ITINÉRAIRES OPTIMAUX COMMENTÉS ===")
    for start, end in OD_QUERIES:
        path = reconstruct_path(P, start, end)
        readable_path = " -> ".join(CITY_LABELS.get(p, str(p)) for p in path)
        print(f"{CITY_LABELS[start]} → {CITY_LABELS[end]} : {readable_path} (temps cumulé = {L[start][end]} h)")

        # Ajoute une brève interprétation métier
        if (start, end) == (0, 9):
            print("  • Le corridor Paris–Lyon structure l'itinéraire nord-est vers Nice.")
        elif (start, end) == (5, 9):
            print("  • Les plateformes méditerranéennes (Montpellier puis Marseille) évitent un détour par le nord.")
        elif (start, end) == (8, 4):
            print("  • La traversée ouest-est s'appuie sur le hub bordelais avant de rejoindre le sud-est.")
        elif (start, end) == (7, 11):
            print("  • La diagonale est-sud privilégie la liaison Clermont-Ferrand puis Montpellier.")


def main() -> None:
    if not GRAPH_FILE.exists():
        raise FileNotFoundError(
            f"Fichier de graphe introuvable : {GRAPH_FILE}. Exécutez ce script depuis la racine du projet."
        )

    graph = load_graph_from_file(str(GRAPH_FILE))
    # Compte des arcs avant modification des matrices par l'algorithme
    edge_count = sum(
        1
        for i in range(graph.n)
        for j in range(graph.n)
        if i != j and graph.L[i][j] != float("inf")
    )

    L, P, has_negative_cycle = floyd_warshall(graph.L, graph.P, verbose=False)

    describe_network(graph.n, edge_count)

    print("\n=== DIAGNOSTIC DE CONSISTANCE ===")
    if has_negative_cycle:
        print("Un cycle absorbant a été détecté : le réseau doit être corrigé avant exploitation.")
        return

    print("Aucun cycle absorbant : les temps de trajet minimaux sont bien définis.")
    print_sample_paths(L, P)


if __name__ == "__main__":
    main()
