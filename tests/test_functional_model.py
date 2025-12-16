# futurisys-ml-deploy/tests/test_functional_model.py

import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.data.api_db_integration import record_input, record_output
from src.ml.predictor import predict

client = TestClient(app)


@pytest.fixture
def setup_db():
    # Fixture pour insérer un input en base
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "Rarement",
    }
    trace = record_input(payload, "v1.0")
    yield trace
    # Clean up
    record_output(
        trace["input_id"],
        trace["request_id"],
        {"prediction": 1, "probability": 0.95},
        "v1.0",
    )


def test_predict_api(setup_db):
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "Rarement",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "request_id" in response.json()
    assert "prediction" in response.json()
    assert "probability" in response.json()


def test_predict_with_database_interaction(setup_db):
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "Rarement",
    }
    result = predict(payload, model_name="random_forest")
    assert "prediction" in result
    assert "probability" in result
    assert isinstance(result["probability"], float)
    assert result["prediction"] in [0, 1]
    # 0 ou 1 selon la classe prédite


def test_invalid_prediction_payload():
    payload = {
        "age": "not a number",
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "Rarement",
    }
    result = predict(payload, model_name="random_forest")
    assert result["prediction"] == -1
    # Valeur par défaut en cas d'erreur
