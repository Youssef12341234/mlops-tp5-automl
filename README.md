# TP05 - Creer et deployer un modele AutoML

Projet de deploiement de classification de fraude avec FLAML, MLflow et deux services HTTP locaux.
Les etapes suivent le sujet TP05 fourni. Le parcours Vertex AI (bloc G) est facultatif et peut engendrer des frais ; aucune ressource cloud n'est creee par ce projet.

## 1. Environnement et donnees

Depuis PowerShell dans ce dossier :

```powershell
py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python donnees.py
```

Le generateur repris du TP04 produit `data/transactions.csv` (5 000 lignes deterministes). Les donnees, modeles exportes et artefacts MLflow sont exclus de Git.

## 2. Demarrer MLflow

Ouvrir un premier terminal PowerShell dans le dossier du projet, activer `.venv`, puis :

```powershell
mlflow server --host 127.0.0.1 --port 5000 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts
```

Garder ce terminal ouvert. Interface : <http://127.0.0.1:5000>.

## 3. Entrainement et registre

Dans un deuxieme terminal active :

```powershell
python src/automl_deploy.py
python src/modele_manuel.py
```

FLAML est configure pour un budget de 90 secondes. Le deuxieme entrainement reproduit le Random Forest du TP2 (500 arbres, profondeur 16). Chaque modele est enregistre sous `fraude-automl` ou `fraude-manuel` dans le registre MLflow.

Si FLAML ne s'installe pas sur le Python utilise au TP04, le plan B de l'annexe A est disponible :

```powershell
python src/automl_deploy_sklearn.py
```

Noter dans le rapport que le plan B a ete utilise.

## 4. Alias de production et services

Dans le deuxieme terminal :

```powershell
python src/promouvoir.py fraude-automl
python src/promouvoir.py fraude-manuel
```

Ouvrir deux nouveaux terminaux PowerShell (un par service), dans le dossier du projet, activer `.venv` dans chacun et executer :

Terminal AutoML, port 8100 :

```powershell
$env:MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow models serve -m "models:/fraude-automl@production" -p 8100 --env-manager local
```

Terminal modele manuel, port 8101 :

```powershell
$env:MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow models serve -m "models:/fraude-manuel@production" -p 8101 --env-manager local
```

## 5. Appels, latence et requete invalide

Depuis le deuxieme terminal :

```powershell
python src/client.py 8100
python src/client.py 8101
python src/client.py 8100
python src/client.py 8101
```

Le client fait un appel d'exemple, 10 appels d'echauffement et 200 appels chronometres par port. Il ajoute les dernieres valeurs a `reports/latences.json` (fichier local ignore par Git).

Test de signature invalide, comme dans le sujet :

```powershell
$mauvais = @{ dataframe_records = @( @{ montant = 8500 } ) } | ConvertTo-Json -Depth 5
try {
  Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8100/invocations -ContentType 'application/json' -Body $mauvais
} catch {
  $_.ErrorDetails.Message
}
```

## 6. Comparaison, rapport et captures

- Completer `reports/tp5_comparaison.md` avec les F1, temps, tailles et quatre mesures de latence réellement observees.
- `reports/rapport_tp5.md` contient des reponses de travail aux questions du sujet. Il reste a y inserer les mesures et les captures demandees : run AutoML et fichier MLmodel ; services 8100/8101 ; sorties client et erreur de requete invalide.
- Identifier le rapport avec Nom, Prenom, Filiere et Groupe avant export PDF/Word.
- Arreter les services avec Ctrl+C dans leurs terminaux apres les captures.

## 7. GitHub

Le sujet demande un depot public `mlops-tp5-automl`, au moins 5 commits et l'absence de donnees/modeles/artefacts dans les fichiers suivis. Verifier avant publication :

```powershell
git ls-files
git status --short
```

Une fois le depot GitHub vide cree pour le compte voulu :

```powershell
git remote add origin https://github.com/VOTRE_COMPTE/mlops-tp5-automl.git
git push -u origin main
```

Le depot doit contenir `.gitignore`, `requirements.txt`, `donnees.py`, `src/` et `reports/tp5_comparaison.md`.
