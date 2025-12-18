# futurisys-ml-deploy/tests/unit/test_predictor.py

import numpy as np
import pytest

from src.ml.predictor import get_model, predict, prepare_features


def test_prepare_features_basic():
    """
    Vérifie que la transformation des features produit un array numpy 2D
    conforme au pipeline d'entraînement.
    """
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "occasionnel",  # ✅ valeur CSV
    }

    X = prepare_features(payload)

    assert isinstance(X, np.ndarray)
    assert X.ndim == 2
    assert X.shape[0] == 1


def test_prepare_features_invalid_category():
    """
    Une catégorie hors dataset doit être rejetée par la couche ML.
    """
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "Rarement",  # ❌ hors CSV
    }

    with pytest.raises(ValueError):
        prepare_features(payload)


def test_get_model_default():
    model = get_model()
    assert model is not None
    assert hasattr(model, "predict_proba")


def test_get_model_valid_name():
    model = get_model("random_forest")
    assert model is not None
    assert hasattr(model, "predict_proba")


def test_get_model_invalid_name():
    with pytest.raises(ValueError):
        get_model("invalid_model")


def test_predict_contract():
    """
    Vérifie le contrat de sortie du prédicteur ML.
    """
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "frequent",  # ✅ valeur CSV
    }

    result = predict(payload)

    assert "prediction" in result
    assert "probability" in result
    assert isinstance(result["probability"], float)
    assert result["prediction"] in [0, 1]


def test_predict_invalid_model():
    """
    Un modèle inconnu est une erreur métier → exception.
    """
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "occasionnel",
    }

    with pytest.raises(ValueError):
        predict(payload, model_name="unknown")
