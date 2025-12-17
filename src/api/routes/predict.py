# futurisys-ml-deploy/src/api/routes/predict.py

import uuid

from fastapi import APIRouter, HTTPException, Query

from src.api.schemas import PredictionInput, PredictionResponse
from src.ml.predictor import predict as ml_predict

# Le prefix est géré dans main.py (app.include_router(..., prefix="/predict"))
router = APIRouter()


@router.post(
    "",  # ⬅️ endpoint final : POST /predict
    response_model=PredictionResponse,
    tags=["Prediction"],
)
def predict(
    payload: PredictionInput,
    model: str = Query("default", description="Nom du modèle ML"),
):
    """
    Endpoint de prédiction ML.

    - Validation des entrées assurée par Pydantic (422)
    - Erreurs métier ML traduites en erreurs HTTP (400)
    """
    try:
        result = ml_predict(payload.model_dump(), model_name=model)

    except ValueError as exc:
        # Erreur métier (modèle inconnu, feature invalide, etc.)
        raise HTTPException(status_code=400, detail=str(exc))

    return PredictionResponse(
        request_id=str(uuid.uuid4()),
        prediction=result["prediction"],
        probability=result["probability"],
    )
