# futurisys-ml-deploy/src/data/api_db_integration.py
# Fonctions utilitaires utilisées par l’API / workers ML
# pour tracer les inputs et outputs des prédictions (MLOps).

import os
import uuid
from typing import Any

try:
    from src.data.db import SessionLocal
except ImportError:
    SessionLocal = None  # Sécurité CI / tests


def record_input(payload: dict, model_version: str) -> dict[str, Any]:
    """
    Enregistre l'input d'une prédiction.
    En environnement test / CI, la DB est neutralisée.
    """
    request_id = str(uuid.uuid4())

    # 🔒 Mode test / CI : pas de DB
    if os.getenv("ENV") == "test" or SessionLocal is None:
        return {"input_id": 0, "request_id": request_id}

    # 🚀 Mode prod (future extension)
    raise NotImplementedError("Runtime prediction persistence is not enabled.")


def record_output(
    input_id: int,
    request_id: str,
    result: dict,
    model_version: str,
) -> None:
    """
    Enregistre l'output d'une prédiction.
    Neutralisé en environnement test.
    """

    if os.getenv("ENV") == "test" or SessionLocal is None:
        return None

    raise NotImplementedError("Runtime prediction persistence is not enabled.")
