# futurisys-ml-deploy/src/ml/predictor.py

from typing import Optional

import numpy as np

from src.ml.model_registry import get_features, get_model


def prepare_features(payload: dict) -> np.ndarray:
    """
    Reconstruit le vecteur numpy dans l'ordre exact utilisé au training.
    Les features absentes sont mises à 0.
    """
    features = get_features()
    vector = [payload.get(feature, 0) for feature in features]
    return np.array(vector).reshape(1, -1)


def predict(payload: dict, model_name: Optional[str] = None) -> dict:
    """
    Prédiction ML avec sélection dynamique du modèle.
    """
    try:
        model = get_model(model_name)

        X = prepare_features(payload)

        proba = model.predict_proba(X)[0][1]
        prediction = int(proba >= 0.5)

        return {
            "prediction": prediction,
            "probability": round(float(proba), 4),
        }

    except Exception:
        # Comportement attendu par tes tests
        return {
            "prediction": -1,
            "probability": 0.0,
        }
