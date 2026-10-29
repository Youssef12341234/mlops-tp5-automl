"""Appelle le service MLflow et mesure mediane et p95 sur 200 requetes."""
import json
import statistics
import sys
import time
from pathlib import Path
import requests
port = sys.argv[1] if len(sys.argv) > 1 else "8100"
url = f"http://127.0.0.1:{port}/invocations"
corps = {"dataframe_records": [{"montant": 8500.0, "anciennete": 3,
                                  "freq_24h": 9, "nuit": 1}]}
r = requests.post(url, json=corps, timeout=10)
r.raise_for_status()
print("reponse :", r.status_code, r.json())
for _ in range(10):
    requests.post(url, json=corps, timeout=10).raise_for_status()
lat = []
for _ in range(200):
    t = time.perf_counter()
    requests.post(url, json=corps, timeout=10).raise_for_status()
    lat.append((time.perf_counter() - t) * 1000)
med = round(statistics.median(lat), 1)
p95 = round(statistics.quantiles(lat, n=20)[18], 1)
print(f"port {port} | mediane : {med:.1f} ms | p95 : {p95:.1f} ms")
path = Path("reports/latences.json")
results = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
results[port] = {"mediane_ms": med, "p95_ms": p95, "appels_mesures": 200}
path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
