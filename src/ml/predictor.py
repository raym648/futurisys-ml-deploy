# futurisys-ml-deploy/src/ml/predictor.py

from typing import Optional

import numpy as np

from src.ml.model_registry import get_features, get_model

# Valeurs catégorielles autorisées (source de vérité = CSV)
FREQUENCE_DEPLACEMENT_MAPPING = {
    "aucun": 0,
    "occasionnel": 1,
    "frequent": 2,
}

ALLOWED_FREQUENCE_DEPLACEMENT = set(FREQUENCE_DEPLACEMENT_MAPPING.keys())


def prepare_features(payload: dict) -> np.ndarray:
    """
    Reconstruit le vecteur numpy dans l'ordre exact utilisé au training.

    - Valide les catégories métier
    - Encode les variables catégorielles
    - Retourne un array numpy 2D
    """
    freq = payload.get("frequence_deplacement")

    if freq not in ALLOWED_FREQUENCE_DEPLACEMENT:
        raise ValueError(f"Invalid frequence_deplacement value: {freq}")

    encoded_freq = FREQUENCE_DEPLACEMENT_MAPPING[freq]

    features = get_features()

    vector = []
    for feature in features:
        if feature == "frequence_deplacement":
            vector.append(encoded_freq)
        else:
            vector.append(payload.get(feature, 0))

    return np.array(vector, dtype=float).reshape(1, -1)


def predict(payload: dict, model_name: Optional[str] = None) -> dict:
    """
    Prédiction ML avec sélection dynamique du modèle.

    Lève explicitement des erreurs métier :
    - ValueError si modèle inconnu
    - ValueError si features invalides
    """
    model = get_model(model_name)

    X = prepare_features(payload)

    proba = model.predict_proba(X)[0][1]
    prediction = int(proba >= 0.5)

    return {
        "prediction": prediction,
        "probability": round(float(proba), 4),
    }
