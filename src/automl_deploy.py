"""Entraine FLAML, exporte le meilleur estimateur et l'enregistre dans MLflow."""
import time\nimport sys\nfrom pathlib import Path
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from flaml import AutoML
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
\nsys.stdout.reconfigure(encoding="utf-8", errors="replace")\n
BUDGET = 90
TRACKING_URI = "http://127.0.0.1:5000"
EXPERIMENT = "tp5-automl-deploiement"

df = pd.read_csv("data/transactions.csv")
X, y = df.drop(columns="fraude"), df["fraude"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)
Path("reports").mkdir(exist_ok=True)
Path("models").mkdir(exist_ok=True)
automl = AutoML()
t0 = time.time()
automl.fit(Xtr, ytr, task="classification", metric="f1", time_budget=BUDGET,
           seed=42, verbose=0, log_file_name="reports/flaml_tp5.log")
duree = round(time.time() - t0, 1)
modele = automl.model.estimator
f1_flaml = round(f1_score(yte, automl.predict(Xte)), 4)
f1_modele = round(f1_score(yte, modele.predict(Xte)), 4)
print("famille retenue :", automl.best_estimator, "| classe :", type(modele).__name__)
print("F1 (objet FLAML) :", f1_flaml)
print("F1 (modele exporte) :", f1_modele, "<- doit etre identique")
if f1_flaml != f1_modele:
    raise RuntimeError("Le modele exporte ne reproduit pas les predictions FLAML.")
joblib.dump(modele, "models/model_automl.pkl")
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT)
with mlflow.start_run(run_name=f"automl-{BUDGET}s"):
    mlflow.log_params({"outil": "flaml", "budget_s": BUDGET,
                       "famille": automl.best_estimator})
    mlflow.log_params({f"cfg_{k}": str(v) for k, v in automl.best_config.items()})
    mlflow.log_metrics({"f1": f1_modele, "duree_recherche_s": duree})
    mlflow.log_artifact("reports/flaml_tp5.log")
    info = mlflow.sklearn.log_model(
        modele, name="model", input_example=Xte.head(3),
        registered_model_name="fraude-automl", serialization_format="cloudpickle")
print("enregistre : fraude-automl, version", info.registered_model_version)

