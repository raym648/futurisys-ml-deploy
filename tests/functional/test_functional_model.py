# futurisys-ml-deploy/tests/functional/test_functional_model.py

import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


# ============================================================
# Fixtures – Isolation des dépendances externes
# ============================================================


@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    """
    Neutralise toute interaction DB pour les tests fonctionnels
    """

    def fake_record_input(*args, **kwargs):
        return {"input_id": 1, "request_id": "test-request-id"}

    def fake_record_output(*args, **kwargs):
        return None

    monkeypatch.setattr(
        "src.data.api_db_integration.record_input",
        fake_record_input,
    )
    monkeypatch.setattr(
        "src.data.api_db_integration.record_output",
        fake_record_output,
    )


@pytest.fixture(autouse=True)
def mock_predict(monkeypatch):
    """
    Neutralise le modèle ML réel (joblib, preprocessing, registry)
    """

    def fake_predict(payload: dict, model_name: str):
        if model_name == "unknown":
            raise ValueError(f"Unknown model: {model_name}")

        return {
            "prediction": 1,
            "probability": 0.87,
        }

    # IMPORTANT : patcher là où la fonction est utilisée
    monkeypatch.setattr(
        "src.api.routes.predict.ml_predict",
        fake_predict,
    )


# ============================================================
# Tests fonctionnels API /predict
# ============================================================


def test_predict_api_success():
    """
    Cas nominal : payload conforme + modèle valide
    """
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "frequent",
    }

    response = client.post("/predict?model=baseline", json=payload)

    assert response.status_code == 200

    body = response.json()
    assert "request_id" in body
    assert body["prediction"] == 1
    assert body["probability"] == 0.87


def test_predict_api_invalid_enum_value():
    """
    Cas erreur utilisateur : valeur hors Enum (422)
    """
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "Rarement",  # ❌ hors Enum
    }

    response = client.post("/predict?model=baseline", json=payload)

    assert response.status_code == 422


def test_predict_api_invalid_model():
    """
    Cas erreur métier : modèle inconnu (400)
    """
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "frequent",
    }

    response = client.post("/predict?model=unknown", json=payload)

    assert response.status_code == 400
    assert "Unknown model" in response.json()["detail"]
