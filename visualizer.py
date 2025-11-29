# visualizer.py

from math import inf
import os

try:
    from pyvis.network import Network
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False


def visualize_graph(graph, output_file="graph_visualization.html", show_weights=True):
    """
    Visualise un graphe avec pyvis.network.
    
    Paramètres :
    - graph : objet Graph à visualiser
    - output_file : nom du fichier HTML de sortie
    - show_weights : si True, affiche les poids sur les arcs
    
    Retourne un tuple (chemin_absolu, nombre_arcs) ou (None, 0) en cas d'erreur.
    """
    if not PYVIS_AVAILABLE:
        print("ERREUR : pyvis n'est pas installé.")
        print("Installez-le avec : pip install pyvis")
        return None, 0
    
    try:
        # Créer un réseau pyvis
        net = Network(
            height="600px",
            width="100%",
            directed=True,
            notebook=False,
            cdn_resources="remote"
        )
        
        # Configuration pour un meilleur rendu avec labels à l'intérieur
        net.set_options("""
        {
          "physics": {
            "enabled": true,
            "stabilization": {"iterations": 100},
            "barnesHut": {
              "gravitationalConstant": -2000,
              "centralGravity": 0.3,
              "springLength": 200,
              "springConstant": 0.04,
              "damping": 0.09
            }
          },
          "nodes": {
            "font": {
              "size": 20,
              "face": "Arial",
              "color": "#000000",
              "strokeWidth": 2,
              "strokeColor": "#ffffff",
              "align": "center"
            },
            "borderWidth": 2,
            "borderWidthSelected": 3,
            "shadow": true,
            "labelHighlightBold": true
          },
          "edges": {
            "arrows": {
              "to": {"enabled": true, "scaleFactor": 1.2}
            },
            "smooth": {
              "type": "continuous"
            },
            "font": {
              "size": 14,
              "face": "Arial",
              "color": "#000000",
              "strokeWidth": 1,
              "strokeColor": "#ffffff"
            }
          }
        }
        """)
        
        # Ajouter tous les sommets avec numéros à l'intérieur
        for i in range(graph.n):
            net.add_node(
                i,
                label=str(i),  # Numéro du sommet affiché à l'intérieur
                title=f"Sommet {i}",
                color="#97c2fc",  # Couleur bleue pour les sommets
                size=40,  # Taille du nœud pour mieux voir le numéro
                shape="circle",
                font={"size": 20, "color": "#000000", "face": "Arial", "bold": True}
            )
        
        # Ajouter les arcs (extraits de la matrice L)
        arc_count = 0
        for i in range(graph.n):
            for j in range(graph.n):
                if i != j and graph.L[i][j] != inf:
                    weight = graph.L[i][j]
                    arc_count += 1
                    
                    # Couleur de l'arc selon le poids
                    if weight < 0:
                        edge_color = "#ff6b6b"  # Rouge pour poids négatif
                    elif weight == 0:
                        edge_color = "#95e1d3"  # Vert clair pour poids nul
                    else:
                        edge_color = "#4ecdc4"  # Turquoise pour poids positif
                    
                    # Label de l'arc
                    if show_weights:
                        edge_label = str(weight)
                    else:
                        edge_label = ""
                    
                    net.add_edge(
                        i,
                        j,
                        label=edge_label,
                        title=f"Arc {i} → {j} (poids: {weight})",
                        color=edge_color,
                        width=2
                    )
        
        # Sauvegarder le fichier HTML
        net.save_graph(output_file)
        
        # Obtenir le chemin absolu pour l'ouverture
        abs_path = os.path.abspath(output_file)
        
        return abs_path, arc_count
        
    except Exception as e:
        print(f"Erreur lors de la visualisation : {e}")
        return None, 0


def open_in_browser(file_path):
    """
    Ouvre le fichier HTML dans le navigateur par défaut.
    """
    import webbrowser
    try:
        # Convertir le chemin Windows en format URL
        if os.name == 'nt':  # Windows
            file_path = file_path.replace('\\', '/')
            if not file_path.startswith('/'):
                file_path = '/' + file_path
        webbrowser.open(f"file://{file_path}")
        return True
    except Exception as e:
        print(f"Impossible d'ouvrir le navigateur : {e}")
        return False

