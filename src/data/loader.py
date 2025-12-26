# futurisys-ml-deploy/src/data/loader.py
# Chargement d'un dataset CSV dans PostgreSQL (table dataset)
# Chaque ligne du CSV est stockée comme un document JSONB.
# Conforme à l'Étape 4 – Projet 5 (MLOps & traçabilité)

# futurisys-ml-deploy/src/data/loader.py
# Chargement d'un dataset CSV dans PostgreSQL (table dataset)
# Chaque ligne du CSV est stockée comme un document JSONB.
# Conforme à l'Étape 4 – Projet 5 (MLOps & traçabilité)

from pathlib import Path

import pandas as pd

from src.data.db import SessionLocal
from src.data.models_db_archive import Dataset


def load_csv_to_db(
    csv_path: str | Path,
    dataset_version: str = "e01-clean-v1",
    split: str | None = None,
) -> None:
    """
    Charge un fichier CSV clean dans la table dataset.

    - 1 ligne CSV = 1 ligne SQL
    - payload (JSONB) : toutes les features métier
    - meta (JSONB) : informations MLOps (version, split, etc.)

    Args:
        csv_path (str | Path): chemin vers le fichier CSV
        dataset_version (str): version logique du dataset
        split (str, optional): train / test / inference
    """

    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"❌ Fichier CSV introuvable: {csv_path}")

    df = pd.read_csv(csv_path)

    records: list[Dataset] = []

    for row in df.to_dict(orient="records"):
        records.append(
            Dataset(
                source_file=csv_path.name,
                payload=row,
                meta={"dataset_version": dataset_version, "split": split},
            )
        )

    with SessionLocal() as session:
        session.bulk_save_objects(records)
        session.commit()

    print(f"✅ {len(records)} lignes insérées depuis {csv_path.name}")


if __name__ == "__main__":
    load_csv_to_db(
        csv_path="data/processed/e01_df_central_left_clean.csv",
        dataset_version="e01-clean-v1",
        split="train",
    )
