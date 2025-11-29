# loader.py
# Charge un graphe depuis un fichier texte au format du sujet
# Format : première ligne = nombre de sommets, deuxième = nombre d'arcs, puis les arcs

from graph import Graph

def load_graph_from_file(path):
    """
    Lit un graphe depuis un fichier texte.
    Format attendu (comme dans l'annexe du sujet) :

    Ligne 1 : nombre de sommets (n)
    Ligne 2 : nombre d'arcs (m)
    Lignes suivantes (m lignes) : u v w
        u = sommet initial
        v = sommet terminal
        w = poids (entier)

    On ignore les lignes vides et les lignes commençant par '#'.
    """
    with open(path, "r", encoding="utf-8") as f:
        # On filtre les commentaires et les lignes vides
        lignes_utiles = []
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            if ligne.startswith("#"):
                continue
            lignes_utiles.append(ligne)

        if len(lignes_utiles) < 2:
            raise ValueError("Fichier de graphe trop court ou mal formé.")

        n = int(lignes_utiles[0])
        m = int(lignes_utiles[1])

        if len(lignes_utiles) < 2 + m:
            raise ValueError("Nombre de lignes d'arcs incohérent avec m.")

        g = Graph(n)

        # On ajoute chaque arc au graphe
        for i in range(m):
            u_str, v_str, w_str = lignes_utiles[2 + i].split()
            u = int(u_str)
            v = int(v_str)
            w = int(w_str)
            g.add_arc(u, v, w)

    return g
