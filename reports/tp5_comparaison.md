# Modele manuel ou modele AutoML ? (TP05)

Mesures relevees le 29 octobre 2026 sur le meme jeu de test (1 250 transactions) et les deux services locaux.

| Critere | Manuel (RF 500/16) | AutoML (FLAML 90 s) |
|---|---:|---:|
| Famille de modele | RandomForestClassifier | XGBoost (XGBClassifier) |
| F1 sur le jeu de test | 0.8669 | 0.8582 |
| Temps de recherche / entrainement machine | 2.2 s | 90.3 s |
| Temps humain estime | Environ 45 min au TP2 (estimation) | Environ 2 min, lancement compris (estimation) |
| Latence mediane (ms), mesure 1 | 92.9 | 16.4 |
| Latence p95 (ms), mesure 1 | 141.1 | 29.4 |
| Latence mediane (ms), mesure 2 | 92.2 | 18.0 |
| Latence p95 (ms), mesure 2 | 125.5 | 37.8 |
| Taille du fichier local (Mo) | 13.37 | 0.29 |
| Explicabilite | Importance des variables ; 500 arbres, profondeur max. 16 | Importance des variables XGBoost ; 333 estimateurs, max_leaves=4 |

## Decision (5 lignes)

Pour ce service, je retiens le modele FLAML/XGBoost : son F1 (0.8582) reste proche du Random Forest manuel (0.8669).
Sa latence mediane mesuree est d'environ 16-18 ms, contre 92-93 ms pour le modele manuel.
Son p95 reste entre 29 et 38 ms, contre 126-141 ms, et son fichier pese 0.29 Mo contre 13.37 Mo.
Ces gains de latence et de taille sont importants pour servir davantage de requetes avec moins de ressources.
Avant une mise en production reelle, je validerais aussi le rappel et les faux negatifs avec le metier.
