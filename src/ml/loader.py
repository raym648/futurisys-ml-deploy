# futurisys-ml-deploy/src/ml/loader.py

from typing import Any, Dict

import pandas as pd

from src.ml.model_registry import (
    get_features,
    get_metadata,
    get_model,
)

# ============================================================
# ML Loader (isolé, registry-first)
# ============================================================


class MLModelLoader:
    """
    Loader ML responsable de :
    - préparer les features
    - exécuter l'inférence
    - exposer les métadonnées du modèle

    Toute la logique de chargement est déléguée à model_registry.py
    """

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name
        self.model = get_model(model_name)
        self.features = get_features()
        self.metadata = get_metadata()

    # --------------------------------------------------------
    # Input preparation
    # --------------------------------------------------------
    def prepare_inputs(self, raw_inputs: Dict[str, Any]) -> pd.DataFrame:
        """
        Transforme un dict brut en DataFrame
        aligné avec les features du modèle.
        """
        data = {feature: raw_inputs.get(feature) for feature in self.features}
        return pd.DataFrame([data])

    # --------------------------------------------------------
    # Inference
    # --------------------------------------------------------
    def predict(self, raw_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute l'inférence ML et retourne un résultat structuré.
        """
        X = self.prepare_inputs(raw_inputs)

        prediction = int(self.model.predict(X)[0])

        probability = None
        if hasattr(self.model, "predict_proba"):
            probability = float(self.model.predict_proba(X)[0][1])

        return {
            "prediction": prediction,
            "probability": probability,
            "model_name": self.metadata.get("model_name"),
            "model_version": self.metadata.get("version"),
        }
