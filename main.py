# main.py
# Point d'entrée principal du programme
# On orchestre le menu et le flux d'exécution : choix de graphe, Floyd-Warshall, chemins

from interface import (
    print_header, display_graph_list, choose_graph_file,
    display_graph_summary, ask_for_paths, run_automatic_tests,
    Colors, print_separator
)
from loader import load_graph_from_file
from floyd import floyd_warshall
from output import print_matrix
from visualizer import visualize_graph, open_in_browser, PYVIS_AVAILABLE


def show_main_menu():
    """Affiche le menu principal et retourne le choix de l'utilisateur."""
    print()
    print_separator("=", 60, Colors.TITLE)
    print(f"{Colors.BOLD}{Colors.TITLE}MENU PRINCIPAL{Colors.RESET}")
    print_separator("=", 60, Colors.TITLE)
    print(f"  {Colors.BOLD}1.{Colors.RESET} Lister les graphes disponibles")
    print(f"  {Colors.BOLD}2.{Colors.RESET} Analyser un graphe")
    print(f"  {Colors.BOLD}3.{Colors.RESET} Exécuter les tests automatiques")
    print(f"  {Colors.BOLD}4.{Colors.RESET} Visualiser un graphe (pyvis)")
    print(f"  {Colors.BOLD}5.{Colors.RESET} Quitter")
    print_separator("=", 60, Colors.TITLE)
    
    while True:
        choix = input(f"{Colors.BOLD}Votre choix (1-5) : {Colors.RESET}").strip()
        
        if choix in ('1', '2', '3', '4', '5'):
            return choix
        
        print(f"{Colors.ERROR}Choix invalide. Veuillez entrer un nombre entre 1 et 5.{Colors.RESET}")


def analyze_graph(graphs_dir="graphs"):
    """
    Gère l'analyse d'un graphe : sélection, chargement, Floyd-Warshall, chemins.
    """
    path = choose_graph_file(graphs_dir)
    
    if path is None:
        print(f"{Colors.WARNING}Analyse annulée.{Colors.RESET}")
        return False
    
    print(f"\n{Colors.TITLE}Chargement du graphe : {path}{Colors.RESET}")
    
    try:
        g = load_graph_from_file(path)
    except Exception as e:
        print(f"{Colors.ERROR}Erreur lors du chargement du graphe : {e}{Colors.RESET}")
        input(f"\n{Colors.WARNING}Appuyez sur Entrée pour continuer...{Colors.RESET}")
        return True  # Continue the loop
    
    display_graph_summary(g)
    
    print(f"\n{Colors.TITLE}=== Matrice initiale ==={Colors.RESET}")
    print_matrix(g.L, "L (distances initiales)")
    
    print(f"\n{Colors.TITLE}=== Exécution de Floyd-Warshall ==={Colors.RESET}")
    print("Affichage des matrices intermédiaires à chaque étape k...\n")
    
    # Exécution de Floyd-Warshall (avec affichage des matrices intermédiaires)
    L, P, cycle_negatif = floyd_warshall(g.L, g.P, verbose=True, show_initial=False)
    
    print_separator("=", 70, Colors.SEPARATOR)
    
    # Gestion des cycles absorbants
    if cycle_negatif:
        # Si cycle détecté, on n'affiche pas les chemins (non définis)
        print(f"\n{Colors.ERROR}{Colors.BOLD}⚠ ATTENTION : Cycle absorbant détecté !{Colors.RESET}")
        print(f"{Colors.WARNING}Le graphe contient au moins un circuit de poids négatif.{Colors.RESET}")
        print(f"{Colors.WARNING}Les plus courts chemins ne sont pas définis.{Colors.RESET}")
    else:
        # Sinon, on peut proposer l'analyse des chemins
        print(f"\n{Colors.SUCCESS}{Colors.BOLD}✓ Aucun cycle absorbant détecté{Colors.RESET}")
        print(f"{Colors.SUCCESS}Les plus courts chemins sont bien définis.{Colors.RESET}\n")
        
        # Proposer l'analyse des chemins
        ask_for_paths(L, P)
    
    print_separator("=", 70, Colors.SEPARATOR)
    
    input(f"\n{Colors.WARNING}Appuyez sur Entrée pour retourner au menu principal...{Colors.RESET}")
    return True  # Continue the loop


def visualize_graph_menu(graphs_dir="graphs"):
    """
    Gère la visualisation d'un graphe avec pyvis.
    """
    if not PYVIS_AVAILABLE:
        print(f"\n{Colors.ERROR}pyvis n'est pas installé.{Colors.RESET}")
        print(f"{Colors.WARNING}Pour installer pyvis, exécutez : pip install pyvis{Colors.RESET}")
        input(f"\n{Colors.WARNING}Appuyez sur Entrée pour continuer...{Colors.RESET}")
        return
    
    path = choose_graph_file(graphs_dir)
    
    if path is None:
        print(f"{Colors.WARNING}Visualisation annulée.{Colors.RESET}")
        input(f"\n{Colors.WARNING}Appuyez sur Entrée pour continuer...{Colors.RESET}")
        return
    
    print(f"\n{Colors.TITLE}Chargement du graphe : {path}{Colors.RESET}")
    
    try:
        g = load_graph_from_file(path)
    except Exception as e:
        print(f"{Colors.ERROR}Erreur lors du chargement du graphe : {e}{Colors.RESET}")
        input(f"\n{Colors.WARNING}Appuyez sur Entrée pour continuer...{Colors.RESET}")
        return
    
    # Générer le nom du fichier de sortie basé sur le nom du fichier source
    import os
    base_name = os.path.splitext(os.path.basename(path))[0]
    output_file = f"{base_name}_visualization.html"
    
    print(f"\n{Colors.TITLE}Génération de la visualisation...{Colors.RESET}")
    
    result = visualize_graph(g, output_file, show_weights=True)
    
    if result is None or result[0] is None:
        print(f"{Colors.ERROR}Erreur lors de la génération de la visualisation.{Colors.RESET}")
        input(f"\n{Colors.WARNING}Appuyez sur Entrée pour continuer...{Colors.RESET}")
        return
    
    file_path, arc_count = result
    
    print(f"\n{Colors.SUCCESS}✓ Visualisation générée avec succès !{Colors.RESET}")
    print(f"  • Fichier : {Colors.BOLD}{file_path}{Colors.RESET}")
    print(f"  • Nombre de sommets : {Colors.BOLD}{g.n}{Colors.RESET}")
    print(f"  • Nombre d'arcs : {Colors.BOLD}{arc_count}{Colors.RESET}")
    
    # Proposer d'ouvrir dans le navigateur
    print()
    ouvrir = input(f"{Colors.BOLD}Ouvrir dans le navigateur ? (o/n) : {Colors.RESET}").strip().lower()
    
    if ouvrir in ('o', 'oui', 'y', 'yes'):
        if open_in_browser(file_path):
            print(f"{Colors.SUCCESS}Ouverture dans le navigateur...{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}Impossible d'ouvrir automatiquement. Ouvrez manuellement : {file_path}{Colors.RESET}")
    else:
        print(f"{Colors.WARNING}Pour visualiser le graphe, ouvrez le fichier : {file_path}{Colors.RESET}")
    
    print_separator("=", 70, Colors.SEPARATOR)
    input(f"\n{Colors.WARNING}Appuyez sur Entrée pour retourner au menu principal...{Colors.RESET}")


def main():
    """Point d'entrée principal du programme."""
    print_header()
    
    # Boucle principale : on reste dans le menu jusqu'à ce que l'utilisateur quitte
    while True:
        choix = show_main_menu()
        
        if choix == '1':
            # Lister les graphes
            print()
            files = display_graph_list("graphs")
            if files:
                print(f"\n{Colors.SUCCESS}Total : {len(files)} graphe(s) disponible(s).{Colors.RESET}")
            input(f"\n{Colors.WARNING}Appuyez sur Entrée pour continuer...{Colors.RESET}")
        
        elif choix == '2':
            # Analyser un graphe
            analyze_graph("graphs")
        
        elif choix == '3':
            # Tests automatiques
            run_automatic_tests("graphs")
            input(f"\n{Colors.WARNING}Appuyez sur Entrée pour continuer...{Colors.RESET}")
        
        elif choix == '4':
            # Visualiser un graphe
            visualize_graph_menu("graphs")
        
        elif choix == '5':
            # Quitter
            print()
            print_separator("=", 60, Colors.HEADER)
            print(f"{Colors.SUCCESS}Merci d'avoir utilisé le programme !{Colors.RESET}")
            print(f"{Colors.SUCCESS}Au revoir.{Colors.RESET}")
            print_separator("=", 60, Colors.HEADER)
            break


if __name__ == "__main__":
    main()
