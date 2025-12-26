# futurisys-ml-deploy/src/api/routes/predict.py

"""
Routes de gestion des prédictions ML (DB-first).
- Soumission de requête de prédiction (sans inférence directe)
- Consultation du statut et du résultat (polling)
"""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models_archive import PredictionRequest, PredictionResult
from src.api.schemas.input import PredictionInput
from src.api.schemas.output import (  # fmt: off; fmt: on
    PredictionRequestResponse,
    PredictionResultResponse,
)
from src.db.session import get_async_session

router = APIRouter(tags=["Predictions"])


# ============================================================
# POST /predictions/request
# ============================================================
@router.post(
    "/predictions/request",
    response_model=PredictionRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_prediction_request(
    payload: PredictionInput,
    model_name: str = "default",
    source: str = "api",
    session: AsyncSession = Depends(get_async_session),
):
    """
    Enregistre une requête de prédiction en base.
    Aucune inférence n'est réalisée ici.
    """

    prediction_request = PredictionRequest(
        model_name=model_name,
        source=source,
        inputs=payload.model_dump(),
        status="PENDING",
        created_at=datetime.utcnow(),
    )

    session.add(prediction_request)

    try:
        await session.commit()
        await session.refresh(prediction_request)
    except Exception as exc:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create prediction request: {exc}",
        )

    return PredictionRequestResponse(
        request_id=str(prediction_request.id),
        status=prediction_request.status,
        created_at=prediction_request.created_at,
    )


# ============================================================
# GET /predictions/{request_id}
# ============================================================
@router.get(
    "/predictions/{request_id}",
    response_model=PredictionResultResponse,
)
async def get_prediction_result(
    request_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Récupère le statut et le résultat d'une prédiction.
    Compatible avec le polling.
    """

    # ---- Requête de prédiction
    stmt_request = select(PredictionRequest).where(
        # fmt: off
        PredictionRequest.id == request_id
        # fmt: on
    )
    result_request = await session.execute(stmt_request)
    request = result_request.scalar_one_or_none()

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction request not found",
        )

    # ---- Résultat de prédiction (optionnel)
    stmt_result = select(PredictionResult).where(
        PredictionResult.request_id == request_id
    )
    result_result = await session.execute(stmt_result)
    prediction_result = result_result.scalar_one_or_none()

    # ---- Cas : résultat non encore disponible
    if prediction_result is None:
        return PredictionResultResponse(
            request_id=str(request.id),
            status=request.status,
            prediction=None,
            probability=None,
            model_name=None,
            model_version=None,
            created_at=request.created_at,
        )

    # ---- Cas : résultat disponible
    return PredictionResultResponse(
        request_id=str(request.id),
        status="DONE",
        prediction=prediction_result.prediction,
        probability=prediction_result.probability,
        model_name=prediction_result.model_name,
        model_version=prediction_result.model_version,
        created_at=prediction_result.created_at,
    )
