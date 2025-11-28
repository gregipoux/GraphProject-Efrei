# interface.py

import os
import re
from loader import load_graph_from_file
from floyd import floyd_warshall
from output import print_path_and_distance

def extract_number(filename):
    """
    Extrait le premier nombre d'un nom de fichier pour un tri numérique.
    Exemple :
        g1.txt -> 1
        g10.txt -> 10
    """
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0


def list_graph_files(graphs_dir="graphs"):
    """
    Retourne la liste triée NUMERIQUEMENT des fichiers .txt dans graphs_dir.
    """
    if not os.path.isdir(graphs_dir):
        return []

    files = [
        f for f in os.listdir(graphs_dir)
        if f.lower().endswith(".txt")
    ]

    files = sorted(files, key=extract_number)

    return files


def choose_graph_file(graphs_dir="graphs"):
    """
    Demande à l'utilisateur de choisir un fichier de graphe
    parmi ceux présents dans graphs_dir.
    Retourne le chemin complet du fichier choisi, ou None si annulation.
    """

    files = list_graph_files(graphs_dir)

    if not files:
        print(f"Aucun fichier .txt trouvé dans le dossier '{graphs_dir}'.")
        return None

    print("\nGraphes disponibles :")
    for idx, fname in enumerate(files):
        print(f"  {idx}: {fname}")
    print("  q: quitter")

    while True:
        choix = input("Sélectionnez un graphe par son numéro (ou 'q' pour quitter) : ").strip()

        if choix.lower() == 'q':
            return None

        if not choix.isdigit():
            print("Veuillez entrer un numéro valide.")
            continue

        idx = int(choix)

        if 0 <= idx < len(files):
            path = os.path.join(graphs_dir, files[idx])
            return path

        print("Indice hors limites.")


def ask_for_paths(L, P):
    """
    Boucle de demande de chemins à l'utilisateur :
    - demande si l'utilisateur veut afficher un chemin
    - si oui : demande start et end, affiche le chemin et sa valeur
    - répète jusqu'à ce que l'utilisateur dise non
    """

    n = len(L)

    while True:
        rep = input("\nVoulez-vous afficher un chemin ? (o/n) ").strip().lower()

        if rep not in ("o", "oui", "n", "non"):
            print("Réponse non reconnue. Répondez par 'o' ou 'n'.")
            continue

        if rep in ("n", "non"):
            break

        try:
            start = int(input(f"Sommet de départ (entre 0 et {n-1}) : ").strip())
            end = int(input(f"Sommet d'arrivée (entre 0 et {n-1}) : ").strip())
        except ValueError:
            print("Veuillez entrer des entiers valides.")
            continue

        if not (0 <= start < n and 0 <= end < n):
            print("Indices de sommets hors limites.")
            continue

        print_path_and_distance(L, P, start, end)

    print("Fin de l'affichage des chemins pour ce graphe.")