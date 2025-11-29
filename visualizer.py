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
    
    # Configuration de l'espacement pour tous les graphes
    # On augmente l'espacement pour améliorer la lisibilité
    is_large_graph = graph.n >= 10
    if is_large_graph:
        # Pour les grands graphes, espacement encore plus important
        spring_length = 500
        gravitational_constant = -6000
        central_gravity = 0.05
        node_size = 50
        font_size = 16
    else:
        # Pour les petits graphes aussi, on augmente l'espacement
        spring_length = 350
        gravitational_constant = -4000
        central_gravity = 0.15
        node_size = 45
        font_size = 18
    
    try:
        # Créer un réseau pyvis avec une hauteur augmentée pour tous les cas
        net = Network(
            height="900px" if is_large_graph else "700px",
            width="100%",
            directed=True,
            notebook=False,
            cdn_resources="remote"
        )
        
        # Configuration pour un meilleur rendu avec labels à l'intérieur
        # Espacement augmenté pour les grands graphes
        # La physique se désactive après stabilisation pour que les nœuds restent en place
        net.set_options(f"""
        {{
          "physics": {{
            "enabled": true,
            "stabilization": {{
              "enabled": true,
              "iterations": 200,
              "fit": true
            }},
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
        
        # Ajouter du code JavaScript pour que les nœuds restent à leur position après déplacement
        # On lit le fichier, on ajoute le script, et on le réécrit
        with open(output_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Script JavaScript pour désactiver la physique après stabilisation
        # et permettre aux nœuds de rester à leur position après déplacement
        js_code = """
        <script type="text/javascript">
          (function() {
            var networkInstance = null;
            
            // Fonction pour trouver le réseau vis.js
            function findNetwork() {
              // Chercher dans toutes les divs
              var allDivs = document.querySelectorAll('div');
              for (var i = 0; i < allDivs.length; i++) {
                var div = allDivs[i];
                // Pyvis stocke souvent le réseau dans une propriété du conteneur
                if (div.network && typeof div.network.setOptions === 'function') {
                  return div.network;
                }
                // Ou dans une variable globale
                if (window.network && typeof window.network.setOptions === 'function') {
                  return window.network;
                }
              }
              return null;
            }
            
            // Fonction pour configurer le réseau
            function setupNetwork() {
              if (!networkInstance) {
                networkInstance = findNetwork();
              }
              
              if (networkInstance) {
                // Désactiver la physique après stabilisation
                networkInstance.once("stabilizationEnd", function() {
                  networkInstance.setOptions({ physics: { enabled: false } });
                });
                
                // Désactiver la physique quand on commence à déplacer un nœud
                networkInstance.on("dragStart", function() {
                  networkInstance.setOptions({ physics: { enabled: false } });
                });
                
                // S'assurer que la physique reste désactivée après relâchement
                networkInstance.on("dragEnd", function() {
                  networkInstance.setOptions({ physics: { enabled: false } });
                });
                
                // Vérifier périodiquement et désactiver la physique si elle est activée
                var checkInterval = setInterval(function() {
                  if (networkInstance) {
                    networkInstance.setOptions({ physics: { enabled: false } });
                  }
                }, 100);
                
                // Arrêter la vérification après 5 secondes
                setTimeout(function() {
                  clearInterval(checkInterval);
                }, 5000);
              }
            }
            
            // Essayer plusieurs fois pour trouver le réseau
            var attempts = 0;
            var maxAttempts = 20;
            var trySetup = setInterval(function() {
              attempts++;
              setupNetwork();
              if (networkInstance || attempts >= maxAttempts) {
                clearInterval(trySetup);
              }
            }, 200);
          })();
        </script>
        """
        
        # Insérer le script avant la balise </body>
        if '</body>' in html_content:
            html_content = html_content.replace('</body>', js_code + '</body>')
        else:
            # Si pas de </body>, on ajoute à la fin
            html_content += js_code
        
        # Réécrire le fichier avec le script ajouté
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
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

