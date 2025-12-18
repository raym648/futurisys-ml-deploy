# futurisys-ml-deploy/src/data/api_db_integration.py
# Fonctions utilitaires utilisées par l’API / workers ML
# pour tracer les inputs et outputs des prédictions (MLOps).

import uuid

from src.data.db import SessionLocal
from src.data.models_db import ModelInput, ModelOutput


def record_input(payload: dict, model_version: str):
    request_id = str(uuid.uuid4())

    with SessionLocal() as session:
        mi = ModelInput(
            request_id=request_id,
            payload=payload,
            model_version=model_version,
            status="queued",
        )
        session.add(mi)
        session.commit()
        session.refresh(mi)

    return {"input_id": mi.input_id, "request_id": request_id}


def record_output(
    input_id: int,
    request_id: str,
    result: dict,
    model_version: str,
):
    with SessionLocal() as session:
        mo = ModelOutput(
            input_id=input_id,
            request_id=request_id,
            result=result,
            model_version=model_version,
        )
        session.add(mo)

        (
            session.query(ModelInput)
            .filter(ModelInput.input_id == input_id)
            .update({"status": "success"})
        )

        session.commit()
