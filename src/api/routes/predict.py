# futurisys-ml-deploy/src/api/routes/predict.py

from fastapi import APIRouter, Query

from src.api.schemas import PredictionRequest, PredictionResponse
from src.data.api_db_integration import record_input, record_output
from src.ml.predictor import predict

router = APIRouter()

# Version globale (fallback)
MODEL_VERSION = "e02-ml-v1"


@router.post("/", response_model=PredictionResponse)
def predict_endpoint(
    payload: PredictionRequest,
    model: str
    | None = Query(
        default=None,
        # fmt: off
        description=(
            "Nom du modèle à utiliser "
            "(dummy, logistic, random_forest, random_forest_e04)"
        ),
        # fmt: on
    ),
):
    """
    Endpoint de prédiction ML.
    - Par défaut : modèle de production
    - Optionnel : ?model=random_forest
    """

    input_data = payload.data

    # Séparation claire entre tracking et sélection du modèle
    model_name = model
    model_version = MODEL_VERSION

    # 🔵 Enregistrement INPUT
    trace = record_input(payload=input_data, model_version=model_version)

    try:
        # 🔵 Prédiction
        result = predict(payload=input_data, model_name=model_name)

    except ValueError as exc:
        # Validation douce : modèle inconnu ou erreur métier
        result = {
            "prediction": -1,
            "probability": 0.0,
            "error": str(exc),
        }

    # 🔵 Enregistrement OUTPUT
    record_output(
        input_id=trace["input_id"],
        request_id=trace["request_id"],
        result=result,
        model_version=model_version,
    )

    return {"request_id": str(trace["request_id"]), **result}
