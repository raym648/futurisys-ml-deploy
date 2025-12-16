# futurisys-ml-deploy/src/ml/model_registry.py


import json
from pathlib import Path

import joblib

# ============================================================
# Base path for ML artifacts
# ============================================================

BASE_PATH = Path("data/ml_artifacts")

# ============================================================
# Load metadata (documentation + runtime exposure)
# ============================================================

METADATA = json.loads(
    # fmt: off
    (BASE_PATH / "metadata.json").read_text(encoding="utf-8")
    # fmt: on
)

# ============================================================
# Load features
# ============================================================

FEATURES = joblib.load(
    # fmt: off
    BASE_PATH / "features" / "e02_all_features_final_list.joblib"
    # fmt: on
)

# ============================================================
# Load models
# ============================================================

MODELS = {
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

# DEFAULT_MODEL_NAME = "logistic"

# ============================================================
# 🔵 Modèle promu en production
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
    if name is None:
        name = DEFAULT_MODEL_NAME

    if name not in MODELS:
        raise ValueError(f"Unknown model: {name}")

    return MODELS[name]
