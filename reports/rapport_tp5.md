# Rapport de TP05 - AutoML : creer et deployer un modele

**Nom et prenom :** Youssef Hachimi Alaoui  
**Filiere :** 5IASD  
**Groupe :** A completer

> Rapport de travail : ajouter les captures et les mesures du poste avant de remettre le PDF ou le DOCX.

## Realisation

Le TP compare le modele FLAML (budget de 90 secondes) et le modele manuel Random Forest du TP2 (500 arbres, profondeur maximale 16). Les deux sont suivis dans MLflow, promus avec l'alias `production`, servis en HTTP sur les ports 8100 et 8101 et appeles par un client qui mesure la latence.

**Parcours effectue :** FLAML (remplacer par le plan B scikit-learn si necessaire).  
**F1 AutoML :** a completer. **F1 manuel :** a completer.  
**Mesures de latence :** voir le tableau `tp5_comparaison.md` et reporter ici les 4 resultats.

## Questions du sujet

### 1. Quel modele mettre en production ?

La decision finale depend des mesures du bloc D et du tableau comparatif. Il faut retenir le modele qui respecte le seuil de qualite requis tout en offrant une latence p95, une taille et une explicabilite acceptables. Completer cette reponse avec les valeurs observees et le nom du modele retenu.

### 2. Cout mensuel indicatif d'un point de terminaison cloud

Consultation de la tarification Google Cloud : 29 octobre 2026. Pour une estimation simple, un noeud `n4-highcpu-2` a 0,088021 USD par heure represente environ **64,26 USD pour 730 heures** (0,088021 x 730), meme sans requete si le noeud reste pret. C'est une estimation indicative avant taxes et autres frais, qui depend de la region et de la configuration ; verifier le tarif affiche au moment du deploiement. Google indique que le modele deploye est facture pendant que son noeud est pret, meme sans prediction. Source : https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing

### 3. Pourquoi le cloud est-il plus lent que le service local ?

Un appel cloud ajoute le trajet reseau entre le client et la region cloud, les delais TLS/HTTP, le routage et parfois l'attente de mise a disposition du service. En local, l'appel reste sur la machine et evite l'essentiel de ces couts reseau. Completer par les medianes et p95 observes aux blocs D (les mesures de ce TP sont locales).

### 4. Que risque-t-on si le moteur AutoML cloud change de version ?

Un changement de moteur, de bibliotheques ou de valeurs par defaut peut modifier les performances, les predictions, la latence ou le format de l'artefact. Il peut aussi rendre une ancienne procedure de reproduction incompatible. Il faut versionner les donnees, les parametres, l'environnement et les metriques, puis valider la nouvelle version avant de la promouvoir.

### 5. Comment garantir la reversibilite d'un modele manage ?

Conserver les donnees et le schema, le code de preparation, les hyperparametres, les metriques et l'artefact exporte dans un format documente, avec ses dependances et sa version. Garder une copie hors de la plateforme dans un registre independant, tester son chargement et sa re-inference, et documenter un chemin de redeploiement sur une autre infrastructure.

### 6. Pourquoi cloudpickle pour AutoML et skops pour le modele manuel ? Quels risques ?

FLAML peut retourner un estimateur issu de familles variees ; `cloudpickle` sait serialiser des objets Python et composants dynamiques plus larges, ce qui facilite l'export de cet estimateur. `skops` permet une approche plus restrictive pour le Random Forest scikit-learn du TP2, avec les types de confiance declares. Comme les autres formats pickle, cloudpickle peut executer du code lors du chargement d'un artefact malveillant ou modifie. Il est acceptable dans ce TP parce que l'artefact est produit localement et charge depuis le registre local de confiance ; il ne faut pas charger un tel modele provenant d'une source non verifiee.

## Captures a inserer

1. MLflow : run AutoML (parametres, F1) et artefact `MLmodel`.
2. Les deux services MLflow actifs sur 8100 et 8101.
3. Sorties du client pour les deux ports et reponse a la requete invalide (colonnes absentes).

## Conclusion

A completer apres execution : decision de mise en production justifiee par la qualite, la latence, la taille et l'explicabilite mesurees.
