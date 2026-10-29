"""Affecte l'alias production a la derniere version d'un modele enregistre."""
import sys
import mlflow
from mlflow import MlflowClient
if len(sys.argv) != 2 or sys.argv[1] not in {"fraude-automl", "fraude-manuel"}:
    raise SystemExit("Usage : python src/promouvoir.py fraude-automl|fraude-manuel")
nom = sys.argv[1]
mlflow.set_tracking_uri("http://127.0.0.1:5000")
client = MlflowClient()
versions = client.search_model_versions(f"name='{nom}'")
if not versions:
    raise SystemExit(f"Aucune version trouvee pour {nom}; lancer son entrainement d'abord.")
derniere = max(int(v.version) for v in versions)
client.set_registered_model_alias(nom, "production", str(derniere))
print(f"{nom} : version {derniere} promue (alias production)")
