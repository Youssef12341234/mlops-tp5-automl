# Modele manuel ou modele AutoML ? (TP05)

Mesures a renseigner apres l'execution locale. Ne pas remplacer les valeurs manquantes par des estimations.

| Critere | Manuel (RF 500/16) | AutoML (FLAML 90 s) |
|---|---:|---:|
| Famille de modele | RandomForestClassifier | A relever dans le run MLflow |
| F1 sur le jeu de test | A mesurer | A mesurer |
| Temps de recherche / entrainement (s) | A mesurer | A relever dans MLflow |
| Temps humain estime (min) | A estimer | A estimer |
| Latence mediane (ms), mesure 1 | A mesurer | A mesurer |
| Latence p95 (ms), mesure 1 | A mesurer | A mesurer |
| Latence mediane (ms), mesure 2 | A mesurer | A mesurer |
| Latence p95 (ms), mesure 2 | A mesurer | A mesurer |
| Taille du fichier local (Mo) | A mesurer | A mesurer |
| Explicabilite | Importance des variables ; 500 arbres, profondeur max. 16 | Depend de la famille ; importance des variables si disponible |

## Decision (5 lignes)

A completer apres les mesures : choisir le modele qui satisfait le niveau de F1 necessaire tout en comparant p95, taille du fichier et capacite a expliquer les predictions. Indiquer les compromis observes et justifier le choix a partir des chiffres du tableau.
