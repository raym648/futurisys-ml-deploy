# futurisys-ml-deploy/tests/functional/test_functional_model.py

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


# ============================================================
# Fixtures – Mock Async DB session
# ============================================================


@pytest.fixture(autouse=True)
def mock_async_session(monkeypatch):
    """
    Mocke la session async SQLAlchemy utilisée par Depends(get_async_session)
    """

    async def fake_get_async_session():
        session = AsyncMock()

        # session.execute().scalar_one_or_none() -> None
        session.execute.return_value.scalar_one_or_none.return_value = None

        yield session

    monkeypatch.setattr(
        "src.api.routes.predictions.get_async_session",
        fake_get_async_session,
    )


# ============================================================
# Tests fonctionnels /predictions/request
# ============================================================


def test_create_prediction_request_success():
    """
    Cas nominal : payload valide → requête créée (201)
    """
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "frequent",
    }

    response = client.post(
        "/predictions/request?model_name=baseline",
        json=payload,
    )

    assert response.status_code == 201

    body = response.json()
    assert "request_id" in body
    assert body["status"] == "pending"


def test_create_prediction_request_invalid_enum():
    """
    Cas erreur utilisateur : Enum invalide → 422
    """
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "Rarement",  # ❌ hors Enum
    }

    response = client.post(
        "/predictions/request",
        json=payload,
    )

    assert response.status_code == 422


# ============================================================
# Tests fonctionnels GET /predictions/{request_id}
# ============================================================


def test_get_prediction_result_not_found():
    """
    Cas : request_id inconnu → 404
    """
    response = client.get("/predictions/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
