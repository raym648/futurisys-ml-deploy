# futurisys-ml-deploy/src/ml/predictor.py


from typing import Optional

import numpy as np

from src.ml.artifacts import FEATURES, MODELS, default_model


def prepare_features(payload: dict) -> np.ndarray:
    """
    Reconstruit le vecteur numpy dans l'ordre exact utilisé au training.
    Les features absentes sont mises à 0.
    """
    vector = [payload.get(feature, 0) for feature in FEATURES]
    return np.array(vector).reshape(1, -1)


def get_model(model_name: Optional[str] = None):
    """
    Retourne le modèle demandé ou le modèle par défaut.
    """
    if model_name is None:
        return default_model

    if model_name not in MODELS:
        raise ValueError(f"Modèle inconnu : {model_name}")

    return MODELS[model_name]


def predict(payload: dict, model_name: Optional[str] = None) -> dict:
    """
    Prédiction ML avec sélection dynamique du modèle.
    """
    model = get_model(model_name)

    X = prepare_features(payload)

    proba = model.predict_proba(X)[0, 1]
    prediction = int(proba >= 0.5)

    return {"prediction": prediction, "probability": round(float(proba), 4)}
