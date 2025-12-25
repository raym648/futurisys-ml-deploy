# futurisys-ml-deploy/src/api/routes/metrics.py

from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/metrics", tags=["metrics"])

METRICS_PATH = Path("data/ml_artifacts/metrics")


@router.get("/summary")
def get_metrics_summary():
    """
    Retourne les métriques agrégées par modèle
    (utilisé par le dashboard Streamlit).
    """
    metrics_file = METRICS_PATH / "e04_rf_smote_test_metrics.csv"

    if not metrics_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Summary metrics file not found",
        )

    try:
        df = pd.read_csv(metrics_file)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to read summary metrics file",
        )

    summary_df = df[df["fold"].isna()].copy()

    if summary_df.empty:
        raise HTTPException(
            status_code=500,
            detail="No summary metrics found in file",
        )

    summary_df = summary_df[["model", "mean_pr_auc", "std_pr_auc"]].rename(
        columns={
            "mean_pr_auc": "pr_auc_mean",
            "std_pr_auc": "pr_auc_std",
        }
    )

    return summary_df.to_dict(orient="records")


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
    if ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    if not filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed",
        )

    file_path = METRICS_PATH / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Metric file not found")

    try:
        df = pd.read_csv(file_path)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to read metric file",
        )

    return {
        "file": filename,
        "rows": len(df),
        "data": df.to_dict(orient="records"),
    }
