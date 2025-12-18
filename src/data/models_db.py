# futurisys-ml-deploy/src/data/models_db.py
# Définitions des modèles SQLAlchemy (ORM) pour les tables principales.
# Version MLOps orientée JSONB – Dataset, Inputs, Outputs
# Étape 4 – PostgreSQL / SQLAlchemy


from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import text

Base = declarative_base()


class Dataset(Base):
    """
    Table dataset :
    - 1 ligne = 1 enregistrement du CSV clean
    - payload JSONB = données métier complètes (features + target)
    - meta JSONB = informations MLOps (optionnelles)
    """

    __tablename__ = "dataset"

    # Clé primaire technique
    dataset_id = Column(Integer, primary_key=True, autoincrement=True)

    # Traçabilité du fichier source
    source_file = Column(String(255), nullable=False, index=True)

    # Données CSV complètes (ligne par ligne)
    payload = Column(JSONB, nullable=False)

    # Métadonnées MLOps
    # Exemples :
    # {
    #   "dataset_version": "e01-clean-v1",
    #   "split": "train",
    #   "checksum": "...",
    #   "ingestion_job": "import_dataset_csv.py"
    # }
    meta = Column(JSONB, nullable=True)

    # Horodatage d’ingestion
    created_at = Column(
        DateTime(timezone=True), server_default=text("NOW()"), nullable=False
    )


class ModelInput(Base):
    """
    Table model_inputs :
    - Enregistre toutes les requêtes envoyées à l'API
    """

    __tablename__ = "model_inputs"

    input_id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String(36), nullable=False, index=True)

    payload = Column(JSONB, nullable=False)
    model_version = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="queued")

    created_at = Column(
        DateTime(timezone=True), server_default=text("NOW()"), nullable=False
    )


class ModelOutput(Base):
    """
    Table model_outputs :
    - Résultats produits par le modèle
    - Liés aux inputs pour traçabilité complète
    """

    __tablename__ = "model_outputs"

    output_id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String(36), nullable=False, index=True)

    model_version = Column(String(50), nullable=False)
    result = Column(JSONB, nullable=False)
    metrics = Column(JSONB, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=text("NOW()"), nullable=False
    )
