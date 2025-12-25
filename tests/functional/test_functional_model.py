# futurisys-ml-deploy/tests/functional/test_functional_model.py

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.db.session import get_async_session

# ============================================================
# Test client FastAPI
# ============================================================

client = TestClient(app)


# ============================================================
# Fake AsyncSession (mock DB layer)
# ============================================================


@asynccontextmanager
async def fake_async_session():
    """
    Fake Async SQLAlchemy session used to isolate
    functional API tests from the real database.
    """
    session = AsyncMock()

    # --- INSERT / UPDATE ---
    session.add.return_value = None
    session.commit.return_value = None
    session.refresh.return_value = None

    # --- SELECT ---
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none.return_value = None
    session.execute.return_value = mock_result

    yield session


# ============================================================
# Dependency override (applied automatically)
# ============================================================


@pytest.fixture(autouse=True)
def override_async_db():
    """
    Override get_async_session dependency for all tests
    in this module.
    """
    app.dependency_overrides[get_async_session] = fake_async_session
    yield
    app.dependency_overrides.clear()


# ============================================================
# Functional tests
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
    assert body["status"] == "created"


def test_create_prediction_request_invalid_enum():
    """
    Cas erreur utilisateur :
    - Enum invalide
    → validation Pydantic
    → 422 Unprocessable Entity
    """
    payload = {
        "age": 30,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "frequence_deplacement": "Rarement",  # ❌ hors Enum
    }

    response = client.post(
        "/predictions/request?model_name=baseline",
        json=payload,
    )

    assert response.status_code == 422


def test_get_prediction_result_not_found():
    """
    Cas nominal négatif :
    - ID inexistant
    - SELECT retourne None
    → 404 Not Found
    """
    response = client.get(
        "/predictions/result/999999",
    )

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Prediction request not found"
