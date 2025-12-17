# futurisys-ml-deploy/tests/test_predictor.py

import numpy as np
import pytest

from src.ml.predictor import get_model, predict, prepare_features


def test_prepare_features_basic():
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "Rarement",
    }

    X = prepare_features(payload)

    assert isinstance(X, np.ndarray)
    assert X.shape == (1, len(payload))


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
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "Rarement",
    }

    result = predict(payload)

    assert "prediction" in result
    assert "probability" in result
    assert isinstance(result["probability"], float)
    assert result["prediction"] in [0, 1]


def test_predict_invalid_model():
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "Rarement",
    }

    result = predict(payload, model_name="unknown")

    assert result["prediction"] == -1
