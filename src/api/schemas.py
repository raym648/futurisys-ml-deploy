# futurisys-ml-deploy/src/api/schemas.py

from typing import Any, Dict

from pydantic import BaseModel

# =========================
# ===== INPUT SCHEMA ======
# =========================


class PredictionRequest(BaseModel):
    """
    Payload générique de prédiction ML.
    Les clés doivent correspondre aux features utilisées à l'entraînement.
    """

    data: Dict[str, Any]


# ==========================
# ===== OUTPUT SCHEMA ======
# ==========================


class PredictionResponse(BaseModel):
    request_id: str
    prediction: int
    probability: float
