# futurisys-ml-deploy/src/data/models_predictions.py

"""
Modèles SQLAlchemy ORM – API Predictions (DB-first)
Tables dédiées à l'API / Dashboard :
- prediction_requests
- prediction_results
⚠️ Ne pas mélanger avec models_db.py (Dataset / MLOps offline)
"""

import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import text

Base = declarative_base()


# ============================================================
# PREDICTION REQUESTS
# ============================================================
class PredictionRequest(Base):
    """
    Table prediction_requests
    1 ligne = 1 requête envoyée par l'API / dashboard
    La requête est créée AVANT toute inférence ML.
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

    # Features (alignées PredictionInput)
    age = Column(Integer, nullable=False)
    revenu_mensuel = Column(Float, nullable=False)
    annees_dans_l_entreprise = Column(Integer, nullable=False)
    frequence_deplacement = Column(String(50), nullable=False)

    # Statut du workflow
    # PENDING | RUNNING | DONE | FAILED
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
# PREDICTION RESULTS
# ============================================================
class PredictionResult(Base):
    """
    Table prediction_results
    1 ligne = résultat ML associé à une requête
    Écrite par le worker ML après inférence.
    """

    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Lien vers prediction_requests
    prediction_request_id = Column(
        Integer,
        ForeignKey("prediction_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Résultat ML
    prediction = Column(Integer, nullable=False)
    probability = Column(Float, nullable=False)

    # Métadonnées modèle
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(50), nullable=False)

    # Horodatage
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
    )

    # Relation inverse
    request = relationship(
        "PredictionRequest",
        back_populates="result",
    )
