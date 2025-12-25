# futurisys-ml-deploy/src/data/models_db.py
# Définitions des modèles SQLAlchemy (ORM) – DDL / CI
# Création des tables PostgreSQL via GitHub Actions (Neon serverless)
# ⚠️ Miroir STRICT des tables définies dans models_predictions.py
# ⚠️ Aucune logique runtime / API / async

import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import text

# Base ORM dédiée aux opérations DDL (CI uniquement)
Base = declarative_base()


# ============================================================
# DATASET (offline / MLOps)
# ============================================================
class Dataset(Base):
    """
    Table dataset :
    - 1 ligne = 1 enregistrement issu du CSV clean
    - Utilisée pour ingestion, entraînement, audit MLOps
    - Créée via GitHub Actions sur Neon serverless
    """

    __tablename__ = "dataset"

    dataset_id = Column(Integer, primary_key=True, autoincrement=True)

    source_file = Column(String(255), nullable=False, index=True)

    payload = Column(JSONB, nullable=False)

    meta = Column(JSONB, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
    )


# ============================================================
# PREDICTION REQUESTS (MIROIR API)
# ============================================================
class PredictionRequest(Base):
    """
    Table prediction_requests
    Miroir DDL de models_predictions.PredictionRequest
    """

    __tablename__ = "prediction_requests"

    # PK technique
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Identifiant exposé à l'API (UUID)
    request_id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )

    # Métadonnées requête
    model_name = Column(String(100), nullable=False)
    source = Column(String(50), nullable=False, default="api")

    # Features (STRICTEMENT identiques)
    age = Column(Integer, nullable=False)
    revenu_mensuel = Column(Float, nullable=False)
    annees_dans_l_entreprise = Column(Integer, nullable=False)
    frequence_deplacement = Column(String(50), nullable=False)

    # Statut du workflow
    status = Column(String(20), nullable=False, index=True)

    # Message d’erreur éventuel
    error_message = Column(String, nullable=True)

    # Horodatage
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Relation 1–1 vers le résultat
    result = relationship(
        "PredictionResult",
        back_populates="request",
        uselist=False,
        cascade="all, delete-orphan",
    )


# ============================================================
# PREDICTION RESULTS (MIROIR API)
# ============================================================
class PredictionResult(Base):
    """
    Table prediction_results
    Miroir DDL de models_predictions.PredictionResult
    """

    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, autoincrement=True)

    prediction_request_id = Column(
        Integer,
        ForeignKey("prediction_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    prediction = Column(Integer, nullable=False)
    probability = Column(Float, nullable=False)

    model_name = Column(String(100), nullable=False)
    model_version = Column(String(50), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
    )

    request = relationship(
        "PredictionRequest",
        back_populates="result",
    )
