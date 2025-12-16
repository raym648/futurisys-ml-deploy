# futurisys-ml-deploy/src/ml/artifacts.py

"""
Point d'accès unique aux artefacts ML.

⚠️ Ce module ne charge rien directement.
Toute la logique de chargement est centralisée dans model_registry.py
afin d'éviter toute duplication et garantir une source de vérité unique.
"""

from src.ml.model_registry import (
    DEFAULT_MODEL_NAME,
    FEATURES,
    MODELS,
    get_model,
)

__all__ = [
    "DEFAULT_MODEL_NAME",
    "FEATURES",
    "MODELS",
    "default_model",
]

# Modèle par défaut exposé explicitement
default_model = get_model(DEFAULT_MODEL_NAME)
