# main.py

from interface import (
    print_header, display_graph_list, choose_graph_file,
    display_graph_summary, ask_for_paths, run_automatic_tests,
    Colors, print_separator
)
from loader import load_graph_from_file
from floyd import floyd_warshall
from output import print_matrix


def show_main_menu():
    """Affiche le menu principal et retourne le choix de l'utilisateur."""
    print()
    print_separator("=", 60, Colors.TITLE)
    print(f"{Colors.BOLD}{Colors.TITLE}MENU PRINCIPAL{Colors.RESET}")
    print_separator("=", 60, Colors.TITLE)
    print(f"  {Colors.BOLD}1.{Colors.RESET} Lister les graphes disponibles")
    print(f"  {Colors.BOLD}2.{Colors.RESET} Analyser un graphe")
    print(f"  {Colors.BOLD}3.{Colors.RESET} Exécuter les tests automatiques")
    print(f"  {Colors.BOLD}4.{Colors.RESET} Quitter")
    print_separator("=", 60, Colors.TITLE)
    
    while True:
        choix = input(f"{Colors.BOLD}Votre choix (1-4) : {Colors.RESET}").strip()
        
        if choix in ('1', '2', '3', '4'):
            return choix
        
        print(f"{Colors.ERROR}Choix invalide. Veuillez entrer un nombre entre 1 et 4.{Colors.RESET}")


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
    
    if cycle_negatif:
        print(f"\n{Colors.ERROR}{Colors.BOLD}⚠ ATTENTION : Cycle absorbant détecté !{Colors.RESET}")
        print(f"{Colors.WARNING}Le graphe contient au moins un circuit de poids négatif.{Colors.RESET}")
        print(f"{Colors.WARNING}Les plus courts chemins ne sont pas définis.{Colors.RESET}")
    else:
        print(f"\n{Colors.SUCCESS}{Colors.BOLD}✓ Aucun cycle absorbant détecté{Colors.RESET}")
        print(f"{Colors.SUCCESS}Les plus courts chemins sont bien définis.{Colors.RESET}\n")
        
        # Proposer l'analyse des chemins
        ask_for_paths(L, P)
    
    print_separator("=", 70, Colors.SEPARATOR)
    
    input(f"\n{Colors.WARNING}Appuyez sur Entrée pour retourner au menu principal...{Colors.RESET}")
    return True  # Continue the loop


def main():
    """Point d'entrée principal du programme."""
    print_header()
    
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
            # Quitter
            print()
            print_separator("=", 60, Colors.HEADER)
            print(f"{Colors.SUCCESS}Merci d'avoir utilisé le programme !{Colors.RESET}")
            print(f"{Colors.SUCCESS}Au revoir.{Colors.RESET}")
            print_separator("=", 60, Colors.HEADER)
            break


if __name__ == "__main__":
    main()
