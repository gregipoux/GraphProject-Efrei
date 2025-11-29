# Exemple d'application réelle : réseau logistique national

Ce projet illustre l'usage de l'algorithme de Floyd-Warshall pour planifier les
itinéraires les plus courts entre toutes les plateformes d'un réseau
logistique couvrant plusieurs grandes aires urbaines françaises.

## Contexte métier

Un opérateur e-commerce exploite douze hubs régionaux qui mutualisent le tri et
le transfert de colis. Pour dimensionner ses tournées de nuit et identifier les
corridors structurants, l'entreprise doit connaître, pour chaque couple de
plateformes, le temps routier minimal.

## Données fournies

- Le réseau est modélisé par 12 sommets (hubs) et 44 arcs (liaisons routières
  dirigées) stockés dans `graphs/g14_application.txt`.
- Les poids d'arc représentent un temps de trajet estimé en heures pour un
  poids-lourd de nuit.
- Les sommets sont annotés par des hubs lisibles dans le script
  `application_example.py` (ex. `0` = Lille, `1` = Paris, `3` = Lyon, etc.).

## Exécution de l'algorithme

L'exemple peut être rejoué en lançant :

```bash
python application_example.py
```

Le script charge le graphe, vérifie l'absence de cycle absorbant puis affiche
quelques plus courts chemins représentatifs.

## Résultats et interprétations

- Aucun cycle absorbant n'est détecté : les temps minimaux sont cohérents.
- Lille → Nice : le meilleur itinéraire suit Lille → Paris → Lyon → Marseille →
  Nice pour un temps cumulé de 14 h, ce qui met en évidence le rôle central du
  corridor Paris–Lyon pour desservir la Côte d'Azur.
- Toulouse → Nice : le chemin optimal passe par Montpellier puis Marseille (9 h
  au total), confirmant la pertinence d'un axe méditerranéen sans remontée vers
  le nord.
- Rennes → Marseille : la route la plus rapide exploite l'axe Rennes → Bordeaux
  → Montpellier → Marseille (9 h), illustrant l'intérêt du hub bordelais pour
  accélérer les flux ouest–est.
- Strasbourg → Montpellier : la solution Strasbourg → Clermont-Ferrand →
  Montpellier (8 h) montre que la diagonale est–sud peut éviter Paris tout en
  restant compétitive.

Ces résultats peuvent ensuite être intégrés dans la planification des tournées
ou l'ouverture de nouvelles liaisons directes si certains arcs sont saturés.
