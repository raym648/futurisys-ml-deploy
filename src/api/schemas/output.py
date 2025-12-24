# futurisys-ml-deploy/src/api/schemas/output.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# RESPONSE AFTER REQUEST SUBMISSION
# POST /predictions/request
# ============================================================
class PredictionRequestResponse(BaseModel):
    """
    Réponse retournée après la soumission d'une requête de prédiction.
    Aucune inférence n'est effectuée à ce stade.
    """

    request_id: str = Field(
        ...,
        description="Identifiant unique de la requête de prédiction",
        json_schema_extra={"example": "b1f2e6c9-8d3c-4b6a-9c21-1c8f2f9a9a12"},
    )

    status: str = Field(
        ...,
        description="Statut initial de la requête",
        json_schema_extra={"example": "PENDING"},
    )

    created_at: datetime = Field(
        ...,
        description="Date de création de la requête",
        json_schema_extra={"example": "2025-01-15T10:12:45Z"},
    )


# ============================================================
# RESPONSE FOR POLLING & HISTORY
# GET /predictions/{request_id}
# GET /predictions/history
# ============================================================
class PredictionResultResponse(BaseModel):
    """
    Réponse retournée lors de la consultation d'une prédiction.
    Compatible avec le polling et l'historique.
    """

    request_id: str = Field(
        ...,
        description="Identifiant unique de la requête",
        json_schema_extra={"example": "b1f2e6c9-8d3c-4b6a-9c21-1c8f2f9a9a12"},
    )

    status: str = Field(
        ...,
        description="Statut de la prédiction",
        json_schema_extra={"example": "DONE"},
    )

    # Résultats ML (présents uniquement si status == DONE)
    prediction: Optional[int] = Field(
        default=None,
        description="Classe prédite par le modèle",
        json_schema_extra={"example": 1},
    )

    probability: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Probabilité associée à la prédiction",
        json_schema_extra={"example": 0.87},
    )

    # Métadonnées du modèle
    model_name: Optional[str] = Field(
        default=None,
        description="Nom du modèle utilisé",
        json_schema_extra={"example": "logreg_v1"},
    )

    model_version: Optional[str] = Field(
        default=None,
        description="Version exacte du modèle utilisé",
        json_schema_extra={"example": "2025-01-15"},
    )

    created_at: datetime = Field(
        ...,
        description="Date de création du résultat ou de la requête",
        json_schema_extra={"example": "2025-01-15T10:13:02Z"},
    )
