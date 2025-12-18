# futurisys-ml-deploy/tests/schemas/test_schemas_input.py

import pytest
from pydantic import ValidationError

from src.api.schemas import PredictionInput


def test_prediction_input_valid():
    payload = {
        "age": 45,
        "revenu_mensuel": 4800,
        "annees_dans_l_entreprise": 12,
        "frequence_deplacement": "frequent",
    }

    data = PredictionInput(**payload)
    assert data.frequence_deplacement.value == "frequent"


def test_prediction_input_invalid_enum():
    payload = {
        "age": 45,
        "revenu_mensuel": 4800,
        "annees_dans_l_entreprise": 12,
        "frequence_deplacement": "Rarement",
    }

    with pytest.raises(ValidationError):
        PredictionInput(**payload)
