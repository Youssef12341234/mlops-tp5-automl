# Rapport de TP05 - AutoML creer et deployer un modele

**Nom et prenom :** Youssef Hachimi Alaoui  
**Filiere :** 5IASD  
**Groupe :** a completer

## Synthese des resultats

Les deux modeles ont ete enregistres dans MLflow et servis localement sur les ports 8100 (AutoML) et 8101 (manuel). Sur le meme jeu de test, FLAML/XGBoost atteint un F1 de 0.8582 apres 90.3 secondes de recherche ; le Random Forest manuel atteint 0.8669 apres 2.2 secondes d'entrainement. Le service AutoML est nettement plus rapide sur les mesures locales (mediane 16.4-18.0 ms ; p95 29.4-37.8 ms) et son artefact est beaucoup plus compact (0.29 Mo contre 13.37 Mo). Pour un service local a latence contrainte, je retiens donc le modele AutoML, sous reserve de controler aussi le rappel et les faux negatifs avant une mise en production reelle.

## Resultats quantitatifs

Consulter le tableau complet dans `tp5_comparaison.md`. Chaque mesure de latence comprend 10 appels d'echauffement, puis 200 appels chronometres.

| Modele | F1 test | Temps machine | Mediane 1 / 2 | p95 1 / 2 | Taille |
|---|---:|---:|---:|---:|---:|
| Random Forest manuel (500 arbres, profondeur 16) | 0.8669 | 2.2 s | 92.9 / 92.2 ms | 141.1 / 125.5 ms | 13.37 Mo |
| FLAML, XGBoost | 0.8582 | 90.3 s | 16.4 / 18.0 ms | 29.4 / 37.8 ms | 0.29 Mo |

## Reponses aux questions du sujet

### 1. Le choix de production

Je mettrais le modele AutoML en production pour ce service a latence contrainte. Son F1 de 0.8582 est legerement inferieur au 0.8669 du Random Forest manuel, mais sa latence mediane est de 16-18 ms contre 92 ms et son p95 de 29-38 ms contre 126-141 ms. Son fichier est egalement bien plus petit (0.29 Mo contre 13.37 Mo). Ces mesures ne suffisent pas seules pour une vraie decision de fraude : je verifierais le rappel, la precision et le cout des faux negatifs avant la mise en production.

### 2. Le cout d'un point de terminaison cloud

Tarification Google Cloud consulte le 29 octobre 2026 : a titre indicatif, un noeud `n4-highcpu-2` a 0.088021 USD par heure revient a environ **64.26 USD pour 730 heures** (0.088021 x 730), meme sans requete si le noeud reste pret. Le total depend de la region, des ressources choisies, des taxes et des eventuels frais annexes ; il faut verifier le tarif au moment du deploiement. La page indique que le temps ou le noeud est pret a servir est facture. Aucun service cloud payant n'a ete cree dans ce TP. Source : https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing

### 3. Latence locale et latence cloud

Une prediction cloud ajoute les delais du reseau aller-retour, TLS/HTTP, du routage jusqu'a la region et de la file d'attente du service. Une prediction locale reste sur la machine et evite la plus grande partie de ces delais. Dans nos mesures locales, le service AutoML a une mediane de 16.4 a 18.0 ms et un p95 de 29.4 a 37.8 ms ; le service manuel a une mediane de 92.2 a 92.9 ms et un p95 de 125.5 a 141.1 ms. Nous n'avons pas mesure de point de terminaison cloud dans ce TP ; la comparaison cloud/local reste donc qualitative.

### 4. Le moteur change de version

Une nouvelle version du moteur AutoML, de ses dependances ou de ses valeurs par defaut peut changer le modele retenu, les predictions, les metriques, la latence ou le format de l'artefact. Cela peut rendre une reproduction anterieure difficile ou provoquer une incompatibilite. Pour limiter ce risque, il faut versionner les donnees, les parametres et l'environnement, conserver les artefacts et leurs metriques, puis evaluer la nouvelle version avant toute promotion.

### 5. Reversibilite

Je conserverais une copie du modele exporte hors de la plateforme, avec le schema des donnees, le code de preparation, les hyperparametres, les metriques, la version des bibliotheques et les instructions de chargement. Je garderais une copie dans un registre independant et testerais regulierement son chargement et ses predictions. Cela permet de re-deployer sur un autre service si la plateforme change ou devient indisponible.

### 6. skops ou cloudpickle

FLAML peut choisir des familles et objets Python differents ; le TP utilise donc `cloudpickle` pour exporter l'estimateur gagnant. Le modele manuel est un Random Forest scikit-learn connu et l'exercice demande `skops` avec le type d'arbre explicitement approuve. Comme pickle, cloudpickle peut executer du code lors du chargement d'un fichier malveillant. C'est acceptable ici car le modele est entraine localement et charge depuis notre propre registre MLflow local ; un artefact provenant d'une source non verifiee ne doit jamais etre charge sans controle.

## Captures a inserer dans la version finale

1. **Capture 1 - MLflow :** run `automl-90s` avec famille, configuration et F1, ainsi que le fichier `MLmodel`.
2. **Capture 2 - Services :** fenetres PowerShell des deux services en fonctionnement sur les ports 8100 et 8101.
3. **Capture 3 - Client :** sorties des mesures pour les deux ports et erreur de signature indiquant les colonnes manquantes `anciennete`, `freq_24h` et `nuit`.

## Conclusion

Les mesures de ce poste favorisent FLAML/XGBoost pour une API ou la latence et la taille de l'artefact comptent. La difference de F1 est de 0.0087 en faveur du Random Forest manuel. La validation du rappel, de la precision et de l'impact des faux negatifs reste indispensable pour une decision metier de fraude.
