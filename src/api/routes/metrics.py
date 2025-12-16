# futurisys-ml-deploy/src/api/routes/metrics.py


from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/metrics", tags=["metrics"])

METRICS_PATH = Path("data/ml_artifacts/metrics")


@router.get("/")
def list_metrics():
    """
    Liste les fichiers de métriques disponibles.
    """
    if not METRICS_PATH.exists():
        return {"metrics": []}

    return {"metrics": [f.name for f in METRICS_PATH.glob("*.csv")]}


@router.get("/{filename}")
def get_metric_file(filename: str):
    """
    Retourne le contenu d'un fichier de métriques CSV.
    """
    file_path = METRICS_PATH / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Metric file not found")

    df = pd.read_csv(file_path)
    return {
        "file": filename,
        "rows": len(df),
        "data": df.to_dict(orient="records"),
    }
