# interface.py

import os
import re
from output import print_path_and_distance

# ANSI color codes (minimal, with fallback for Windows)
try:
    # Try to enable ANSI colors on Windows 10+
    import sys
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
except:
    pass

# ANSI color codes (safe fallback to empty strings if not supported)
class Colors:
    HEADER = '\033[95m'  # Bright magenta
    TITLE = '\033[94m'   # Bright blue
    SUCCESS = '\033[92m' # Green
    WARNING = '\033[93m' # Yellow
    ERROR = '\033[91m'   # Red
    BOLD = '\033[1m'     # Bold
    RESET = '\033[0m'    # Reset
    SEPARATOR = '\033[90m'  # Dark gray

def print_separator(char="=", length=60, color=None):
    """Affiche une ligne de séparation."""
    sep = char * length
    if color:
        print(f"{color}{sep}{Colors.RESET}")
    else:
        print(sep)


def print_header():
    """Affiche l'en-tête du programme."""
    print_separator("=", 70, Colors.HEADER)
    print(f"{Colors.BOLD}{Colors.HEADER}  Projet SM501 - Théorie des graphes{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.HEADER}  Algorithme de Floyd-Warshall{Colors.RESET}")
    print_separator("=", 70, Colors.HEADER)
    print()


def extract_number(filename):
    """
    Extrait le premier nombre d'un nom de fichier pour un tri numérique.
    Exemple :
        g1.txt -> 1
        g10.txt -> 10
    """
    match = re.search(r"\d+", filename)
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


def display_graph_list(graphs_dir="graphs"):
    """
    Affiche une liste numérotée des graphes disponibles.
    Retourne la liste des fichiers.
    """
    files = list_graph_files(graphs_dir)

    if not files:
        print(f"{Colors.WARNING}Aucun fichier .txt trouvé dans le dossier '{graphs_dir}'.{Colors.RESET}")
        return []

    print(f"{Colors.TITLE}Graphes disponibles :{Colors.RESET}")
    print_separator("-", 50, Colors.SEPARATOR)
    
    for idx, fname in enumerate(files, start=1):
        print(f"  {Colors.BOLD}{idx:2d}.{Colors.RESET} {fname}")
    
    print_separator("-", 50, Colors.SEPARATOR)
    
    return files


def choose_graph_file(graphs_dir="graphs"):
    """
    Demande à l'utilisateur de choisir un fichier de graphe
    parmi ceux présents dans graphs_dir.
    Retourne le chemin complet du fichier choisi, ou None si annulation.
    """
    files = list_graph_files(graphs_dir)

    if not files:
        print(f"{Colors.ERROR}Aucun fichier .txt trouvé dans le dossier '{graphs_dir}'.{Colors.RESET}")
        return None

    display_graph_list(graphs_dir)

    while True:
        choix = input(f"\n{Colors.BOLD}Sélectionnez un graphe par son numéro (1-{len(files)}) ou 'q' pour annuler : {Colors.RESET}").strip()

        if choix.lower() == 'q':
            return None

        if not choix.isdigit():
            print(f"{Colors.ERROR}Veuillez entrer un numéro valide.{Colors.RESET}")
            continue

        idx = int(choix) - 1  # Convert to 0-based index

        if 0 <= idx < len(files):
            path = os.path.join(graphs_dir, files[idx])
            return path

        print(f"{Colors.ERROR}Numéro hors limites. Veuillez choisir entre 1 et {len(files)}.{Colors.RESET}")


def display_graph_summary(graph):
    """
    Affiche un résumé du graphe chargé.
    """
    print_separator("-", 60)
    print(f"{Colors.SUCCESS}✓ Graphe chargé avec succès{Colors.RESET}")
    print(f"  • Nombre de sommets : {Colors.BOLD}{graph.n}{Colors.RESET}")
    
    # Compter le nombre d'arcs (non-infini dans L)
    from math import inf
    arc_count = 0
    for i in range(graph.n):
        for j in range(graph.n):
            if i != j and graph.L[i][j] != inf:
                arc_count += 1
    
    print(f"  • Nombre d'arcs : {Colors.BOLD}{arc_count}{Colors.RESET}")
    print_separator("-", 60)


def ask_for_paths(L, P):
    """
    Boucle de demande de chemins à l'utilisateur suivant la séquence du sujet :
    "Chemin ? Si oui, alors Sommet de départ ? Sommet d'arrivée ? Affichage du chemin Recommencer?"
    """
    n = len(L)
    
    print(f"\n{Colors.TITLE}=== Analyse des plus courts chemins ==={Colors.RESET}")
    print(f"Le graphe contient {n} sommets (numérotés de 0 à {n-1}).")
    print()

    while True:
        # Question "Chemin ?"
        reponse = input(f"{Colors.BOLD}Chemin ? (o/n) : {Colors.RESET}").strip().lower()
        
        if reponse in ('n', 'non', 'q', 'quitter'):
            break
        
        if reponse not in ('o', 'oui', 'y', 'yes'):
            print(f"{Colors.ERROR}Veuillez répondre par 'o' (oui) ou 'n' (non).{Colors.RESET}")
            continue

        # Si oui, alors demander sommet de départ
        try:
            start = int(input(f"{Colors.BOLD}Sommet de départ ? (0-{n-1}) : {Colors.RESET}").strip())
        except ValueError:
            print(f"{Colors.ERROR}Veuillez entrer un entier valide.{Colors.RESET}")
            continue

        if not (0 <= start < n):
            print(f"{Colors.ERROR}Indice de sommet hors limites. Utilisez une valeur entre 0 et {n-1}.{Colors.RESET}")
            continue

        # Demander sommet d'arrivée
        try:
            end = int(input(f"{Colors.BOLD}Sommet d'arrivée ? (0-{n-1}) : {Colors.RESET}").strip())
        except ValueError:
            print(f"{Colors.ERROR}Veuillez entrer un entier valide.{Colors.RESET}")
            continue

        if not (0 <= end < n):
            print(f"{Colors.ERROR}Indice de sommet hors limites. Utilisez une valeur entre 0 et {n-1}.{Colors.RESET}")
            continue

        # Affichage du chemin
        print()
        print_path_and_distance(L, P, start, end)
        print()

        # Recommencer ?
        while True:
            recommencer = input(f"{Colors.BOLD}Recommencer ? (o/n) : {Colors.RESET}").strip().lower()
            if recommencer in ('n', 'non', 'q', 'quitter'):
                return  # Sortir de la fonction
            if recommencer in ('o', 'oui', 'y', 'yes'):
                break  # Continuer la boucle principale
            print(f"{Colors.ERROR}Veuillez répondre par 'o' (oui) ou 'n' (non).{Colors.RESET}")

    print(f"{Colors.SUCCESS}Retour au menu principal.{Colors.RESET}")


def run_automatic_tests(graphs_dir="graphs"):
    """
    Exécute Floyd-Warshall sur tous les graphes et affiche un résumé.
    """
    files = list_graph_files(graphs_dir)
    
    if not files:
        print(f"{Colors.ERROR}Aucun fichier .txt trouvé dans le dossier '{graphs_dir}'.{Colors.RESET}")
        return

    print(f"\n{Colors.TITLE}=== Mode test automatique ==={Colors.RESET}")
    print(f"Analyse de {len(files)} graphe(s)...\n")
    
    from loader import load_graph_from_file
    from floyd import floyd_warshall
    
    results = []
    
    for fname in files:
        path = os.path.join(graphs_dir, fname)
        try:
            g = load_graph_from_file(path)
            # Exécuter Floyd-Warshall sans affichage détaillé
            L, P, cycle_negatif = floyd_warshall(g.L, g.P, verbose=False, show_initial=False)
            
            results.append({
                'file': fname,
                'vertices': g.n,
                'has_cycle': cycle_negatif
            })
            
        except Exception as e:
            results.append({
                'file': fname,
                'vertices': None,
                'has_cycle': None,
                'error': str(e)
            })
    
    # Afficher le résumé
    print_separator("=", 70, Colors.SEPARATOR)
    print(f"{Colors.BOLD}{'Fichier':<20} {'Sommets':<10} {'Cycle négatif':<20}{Colors.RESET}")
    print_separator("-", 70, Colors.SEPARATOR)
    
    for r in results:
        file_str = r['file']
        if r['vertices'] is None:
            vertices_str = "ERREUR"
            cycle_str = f"{Colors.ERROR}{r.get('error', 'Inconnu')}{Colors.RESET}"
        else:
            vertices_str = str(r['vertices'])
            if r['has_cycle']:
                cycle_str = f"{Colors.ERROR}OUI{Colors.RESET}"
            else:
                cycle_str = f"{Colors.SUCCESS}NON{Colors.RESET}"
        
        print(f"{file_str:<20} {vertices_str:<10} {cycle_str}")
    
    print_separator("=", 70, Colors.SEPARATOR)
    print()
