# Exemple d'application réelle : marathon d'un client Amazon pressé

Pour illustrer l'algorithme de Floyd-Warshall, on met en scène Jules, client
Amazon convaincu que "livraison en un jour" est un droit constitutionnel. Il
veut savoir quel entrepôt expédiera son nouveau grille-pain connecté le plus
rapidement, et quels détours absurdes (ou pas) son colis pourrait emprunter
avant d'atterrir chez lui.

## Contexte amusé mais sérieux

- Douze entrepôts européens (numérotés de 0 à 11) sont reliés par 44 arcs
  orientés représentant des routes logistiques possibles. Les arcs peuvent avoir
  des temps négatifs si un pilote de camion a découvert un raccourci improbable
  ou simplement oublié d'arrêter le chrono.
- Jules ne veut pas seulement le plus court chemin pour sa commande : il veut
  vérifier **tous** les couples d'entrepôts afin d'anticiper d'éventuels retours
  (parce qu'il commande parfois en double quand il clique trop vite).
- Si un circuit absorbant se cache dans le réseau, Jules saura qu'un colis peut
  tourner en rond éternellement — pratique pour ceux qui aiment recevoir des
  notifications "votre colis arrive… un jour".

## Données utilisées

- Le graphe complet est stocké dans `graphs/g14_application.txt` avec
  `12` sommets et `44` arcs (format : nombre de sommets, nombre d'arcs puis
  triplets "origine destination temps").
- Les poids représentent un temps de transit estimé en heures ; des valeurs
  négatives sont autorisées pour coller au cahier des charges.
- `application_example.py` contient une table de correspondance humoristique
  entre indices et villes (par exemple `0` = Lille Prime Now, `3` = Lyon
  emballage façon origami, `11` = Marseille où l'on promet qu'aucun colis ne
  finit à la mer).

## Lancer la simulation

```bash
python application_example.py
```

Le script charge le graphe en mémoire, affiche la matrice initiale puis exécute
Floyd-Warshall. Il signale immédiatement tout circuit absorbant (le fameux colis
qui revient au point de départ plus vite qu'il n'en est parti) et peut afficher
les plus courts chemins sur demande.

## Résultats et interprétation pour Jules

- Aucun circuit absorbant n'apparaît : aucun chauffeur ne fait la course à
  l'infini pour booster son compteur de kilomètres.
- Commande depuis Lille (`0`) vers Nice (`10`) : chemin
  `Lille → Paris → Lyon → Marseille → Nice` en environ 14 h. Jules comprend que
  la Côte d'Azur reste dépendante de l'axe Paris–Lyon, sauf si un drone géant
  est disponible.
- Retour de Nice (`10`) vers Bordeaux (`9`) : itinéraire optimal
  `Nice → Marseille → Clermont-Ferrand → Bordeaux` (8 h). Le grille-pain fera un
  détour gastronomique avant d'arriver chez Mamie.
- Paris (`1`) vers Strasbourg (`4`) : route la plus rapide
  `Paris → Lyon → Strasbourg` (9 h). Jules se dit que même son panier voyage plus
  que lui.
- Toulouse (`7`) vers Lille (`0`) : meilleur chemin `Toulouse → Paris → Lille`
  (8 h) ; pas besoin d'envoyer le colis faire un stage à Marseille.

Ces résultats montrent que la couche logistique Amazon de Jules respecte le
cahier des charges : un graphe orienté, valué, sans limite sur les poids ni le
nombre d'arcs, et un client qui peut enfin suivre ses colis en temps (presque)
réel… avec un sourire en prime.
