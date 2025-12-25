# futurisys-ml-deploy/tests/functional/test_functional_model.py

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.db.session import get_async_session
from src.models.enums import PredictionStatus

# from datetime import datetime


# from src.models.prediction_request import PredictionRequest

# ============================================================
# Test client
# ============================================================

client = TestClient(app)


# ============================================================
# Fixtures – Mock DB AsyncSession
# ============================================================


@pytest.fixture
def mock_async_session():
    """
    Mock complet d'une AsyncSession SQLAlchemy.
    Permet d'exécuter les routes sans base réelle.
    """
    session = AsyncMock()

    # session.add.return_value = None
    session.add = lambda _: None
    session.commit.return_value = None
    session.refresh.return_value = None
    session.rollback.return_value = None

    return session


@pytest.fixture(autouse=True)
def override_get_async_session(mock_async_session):
    """
    Override de la dépendance FastAPI get_async_session
    utilisée dans routes/predictions.py
    """

    async def _override():
        return mock_async_session

    app.dependency_overrides[get_async_session] = _override
    yield
    app.dependency_overrides.clear()


# ============================================================
# Tests fonctionnels – POST /predictions/request
# ============================================================


def test_create_prediction_request_success():
    """
    Cas nominal :
    - payload valide
    - route existante
    - DB mockée
    → 201 Created
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
    assert body["status"] == PredictionStatus.pending
    assert "created_at" in body


def test_create_prediction_request_invalid_enum():
    """
    Cas erreur utilisateur :
    - Enum invalide
    → 422 Unprocessable Entity (Pydantic)
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
# Tests fonctionnels – GET /predictions/{request_id}
# ============================================================


def test_get_prediction_result_not_found(mock_async_session):
    """
    Cas métier réel :
    - UUID valide
    - SELECT sur PredictionRequest retourne None
    → 404 Prediction request not found
    """

    # Mock du résultat SQLAlchemy
    execute_result_mock = AsyncMock()
    execute_result_mock.scalar_one_or_none.return_value = None

    # session.execute() doit retourner cet objet
    mock_async_session.execute = AsyncMock(return_value=execute_result_mock)

    request_id = uuid4()

    response = client.get(f"/predictions/{request_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Prediction request not found"
