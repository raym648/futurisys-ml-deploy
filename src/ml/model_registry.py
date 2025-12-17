# futurisys-ml-deploy/src/ml/model_registry.py

import json
import os
from functools import lru_cache
from pathlib import Path

import joblib

# ============================================================
# Base path for ML artifacts
# ============================================================

BASE_PATH = Path("data/ml_artifacts")

# ============================================================
# Environment
# ============================================================

ENV = os.getenv("ENV", "prod")

# ============================================================
# Lazy loading helpers
# ============================================================


@lru_cache
def get_metadata() -> dict:
    """
    Retourne les métadonnées du modèle.
    En mode test, retourne un dictionnaire minimal mocké.
    """
    if ENV == "test":
        return {
            "model_name": "mock_model",
            "version": "test",
            "description": "Mocked metadata for CI tests",
        }

    metadata_path = BASE_PATH / "metadata.json"

    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

    return json.loads(metadata_path.read_text(encoding="utf-8"))


@lru_cache
def get_features() -> list[str]:
    """
    Retourne la liste des features utilisées par le modèle.
    En mode test, retourne une liste mockée.
    """
    if ENV == "test":
        return [
            "age",
            "revenu_mensuel",
            "annees_dans_l_entreprise",
            "frequence_deplacement",
        ]

    features_path = (
        # fmt: off
        BASE_PATH
        / "features"
        / "e02_all_features_final_list.joblib"
        # fmt: on
    )

    if not features_path.exists():
        raise FileNotFoundError(f"Features file not found: {features_path}")

    return joblib.load(features_path)


@lru_cache
def _load_models() -> dict:
    """
    Charge les modèles ML disponibles.
    En mode test, retourne des modèles mockés.
    """
    if ENV == "test":

        class MockModel:
            def predict(self, X):
                return [0]

            def predict_proba(self, X):
                return [[0.05, 0.95]]

        return {
            "dummy": MockModel(),
            "logistic": MockModel(),
            "random_forest": MockModel(),
            "random_forest_e04": MockModel(),
        }

    return {
        "dummy": joblib.load(
            # fmt: off
            BASE_PATH / "models" / "e03_dummy_most_frequent.joblib"
            # fmt: on
        ),
        "logistic": joblib.load(
            # fmt: off
            BASE_PATH / "models" / "e03_logistic_regression_balanced.joblib"
            # fmt: on
        ),
        "random_forest": joblib.load(
            # fmt: off
            BASE_PATH / "models" / "e03_random_forest_balanced.joblib"
            # fmt: on
        ),
        "random_forest_e04": joblib.load(
            # fmt: off
            BASE_PATH / "models" / "e04_random_forest_final.joblib"
            # fmt: on
        ),
    }


# ============================================================
# Default model
# ============================================================

DEFAULT_MODEL_NAME = "random_forest_e04"

# ============================================================
# Public API
# ============================================================


def get_model(name: str | None = None):
    """
    Retourne un modèle ML à partir de son nom.
    Si aucun nom n'est fourni, retourne le modèle par défaut.
    """
    models = _load_models()

    if name is None:
        name = DEFAULT_MODEL_NAME

    if name not in models:
        raise ValueError(f"Unknown model: {name}")

    return models[name]
