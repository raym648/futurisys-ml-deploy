# futurisys-ml-deploy/src/api/schemas/output.py

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    """
    Réponse standard de l'API de prédiction ML.
    """

    request_id: str
    prediction: int
    probability: float
