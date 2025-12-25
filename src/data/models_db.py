# futurisys-ml-deploy/src/data/models_db.py
# Définitions des modèles SQLAlchemy (ORM) – Dataset offline
# Étape 4 – PostgreSQL / SQLAlchemy
# ⚠️ Ce fichier NE GÈRE PAS les prédictions runtime (API / dashboard)

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import text

Base = declarative_base()


class Dataset(Base):
    """
    Table dataset :
    - 1 ligne = 1 enregistrement issu du CSV clean
    - Utilisée pour :
        - entraînement
        - validation
        - audit MLOps
    - Aucune interaction directe avec l'API de prédiction
    """

    __tablename__ = "dataset"

    # Clé primaire technique
    dataset_id = Column(Integer, primary_key=True, autoincrement=True)

    # Traçabilité du fichier source
    source_file = Column(String(255), nullable=False, index=True)

    # Données CSV complètes (features + target éventuelle)
    payload = Column(JSONB, nullable=False)

    # Métadonnées MLOps
    # Exemple :
    # {
    #   "dataset_version": "e01-clean-v1",
    #   "split": "train",
    #   "checksum": "...",
    #   "ingestion_job": "import_dataset_csv.py"
    # }
    meta = Column(JSONB, nullable=True)

    # Horodatage d’ingestion
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
    )
