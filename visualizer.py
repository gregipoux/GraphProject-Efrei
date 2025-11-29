# visualizer.py

from math import inf
import os

try:
    from pyvis.network import Network
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False


def visualize_graph(graph, output_file="graph_visualization.html", show_weights=True, node_labels=None):
    """
    Visualise un graphe avec pyvis.network.
    
    Paramètres :
    - graph : objet Graph à visualiser
    - output_file : nom du fichier HTML de sortie
    - show_weights : si True, affiche les poids sur les arcs
    - node_labels : dictionnaire {index: nom} pour personnaliser les labels des nœuds
    
    Retourne un tuple (chemin_absolu, nombre_arcs) ou (None, 0) en cas d'erreur.
    """
    if not PYVIS_AVAILABLE:
        print("ERREUR : pyvis n'est pas installé.")
        print("Installez-le avec : pip install pyvis")
        return None, 0
    
    # Détection automatique de g14_application pour utiliser les noms de villes
    is_g14 = "g14" in output_file.lower() or (node_labels is None and graph.n == 12)
    if is_g14 and node_labels is None:
        # Mapping des villes pour g14
        node_labels = {
            0: "Lille",
            1: "Paris",
            2: "Nantes",
            3: "Lyon",
            4: "Marseille",
            5: "Toulouse",
            6: "Bordeaux",
            7: "Strasbourg",
            8: "Rennes",
            9: "Nice",
            10: "Clermont-Ferrand",
            11: "Montpellier",
        }
    
    # Configuration de l'espacement selon la taille du graphe
    is_large_graph = graph.n >= 10
    if is_large_graph:
        # Pour les grands graphes, on augmente l'espacement
        spring_length = 400
        gravitational_constant = -5000
        central_gravity = 0.1
        node_size = 50
        font_size = 16
    else:
        spring_length = 200
        gravitational_constant = -2000
        central_gravity = 0.3
        node_size = 40
        font_size = 20
    
    try:
        # Créer un réseau pyvis
        net = Network(
            height="800px" if is_large_graph else "600px",
            width="100%",
            directed=True,
            notebook=False,
            cdn_resources="remote"
        )
        
        # Configuration pour un meilleur rendu avec labels à l'intérieur
        # Espacement augmenté pour les grands graphes
        net.set_options(f"""
        {{
          "physics": {{
            "enabled": true,
            "stabilization": {{"iterations": 200}},
            "barnesHut": {{
              "gravitationalConstant": {gravitational_constant},
              "centralGravity": {central_gravity},
              "springLength": {spring_length},
              "springConstant": 0.04,
              "damping": 0.09
            }}
          }},
          "nodes": {{
            "font": {{
              "size": {font_size},
              "face": "Arial",
              "color": "#000000",
              "strokeWidth": 2,
              "strokeColor": "#ffffff",
              "align": "center"
            }},
            "borderWidth": 2,
            "borderWidthSelected": 3,
            "shadow": true,
            "labelHighlightBold": true
          }},
          "edges": {{
            "arrows": {{
              "to": {{"enabled": true, "scaleFactor": 1.2}}
            }},
            "smooth": {{
              "type": "continuous"
            }},
            "font": {{
              "size": 14,
              "face": "Arial",
              "color": "#000000",
              "strokeWidth": 1,
              "strokeColor": "#ffffff"
            }}
          }}
        }}
        """)
        
        # Ajouter tous les sommets avec labels personnalisés ou numéros
        for i in range(graph.n):
            # Utiliser le label personnalisé si disponible, sinon le numéro
            if node_labels and i in node_labels:
                label = node_labels[i]
                title = f"{label} (sommet {i})"
            else:
                label = str(i)
                title = f"Sommet {i}"
            
            net.add_node(
                i,
                label=label,
                title=title,
                color="#97c2fc",  # Couleur bleue pour les sommets
                size=node_size,
                shape="circle",
                font={"size": font_size, "color": "#000000", "face": "Arial", "bold": True}
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
                    
                    # Titre de l'arc avec noms de villes si disponibles
                    if node_labels and i in node_labels and j in node_labels:
                        edge_title = f"{node_labels[i]} → {node_labels[j]} (poids: {weight})"
                    else:
                        edge_title = f"Arc {i} → {j} (poids: {weight})"
                    
                    net.add_edge(
                        i,
                        j,
                        label=edge_label,
                        title=edge_title,
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

