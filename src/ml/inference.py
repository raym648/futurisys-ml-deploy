# futurisys-ml-deploy/src/ml/inference.py

from typing import Any, Dict

from src.ml.loader import MLModelLoader

# ============================================================
# Feature normalization (API → ML)
# ============================================================

FREQUENCE_MAPPING = {
    "aucun": 0,
    "occasionnel": 1,
    "frequent": 2,
}


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalise les entrées pour le modèle ML.
    Accepte str ou Enum.value sans dépendre de la couche API.
    """
    payload = payload.copy()

    freq = payload.get("frequence_deplacement")

    if freq is not None:
        payload["frequence_deplacement"] = FREQUENCE_MAPPING.get(str(freq), 0)

    return payload


# ============================================================
# Public inference API
# ============================================================


def run_inference(
    payload: Dict[str, Any],
    model_name: str | None = None,
) -> Dict[str, Any]:
    """
    Inference synchrone, registry-first.
    """
    normalized_payload = normalize_payload(payload)

    loader = MLModelLoader(model_name=model_name)

    return loader.predict(normalized_payload)
