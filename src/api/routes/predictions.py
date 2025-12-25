# futurisys-ml-deploy/src/api/routes/predictions.py

"""
Routes de gestion des prédictions ML (DB-first).
- Soumission de requêtes de prédiction
- Consultation des résultats (polling)
- Historique des prédictions
- Aucune inférence ML n'est exécutée ici
"""

from datetime import UTC, datetime
from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.input import PredictionInput
from src.api.schemas.output import (
    PredictionRequestResponse,
    PredictionResultResponse,
)
from src.db.session import get_async_session
from src.models.enums import PredictionStatus
from src.models.prediction_request import PredictionRequest
from src.models.prediction_result import PredictionResult

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


# ============================================================
# SUBMIT PREDICTION REQUEST
# POST /predictions/request
# ============================================================
@router.post(
    "/request",
    response_model=PredictionRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_prediction_request(
    payload: PredictionInput,
    model_name: str = Query("default", description="Nom du modèle ML"),
    source: str = Query("dashboard", description="Source de la requête"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Enregistre une requête de prédiction en base (Neon).
    Aucune inférence n'est effectuée ici.
    """

    request_uuid = str(uuid4())
    now = datetime.now(UTC)

    prediction_request = PredictionRequest(
        request_id=request_uuid,
        model_name=model_name,
        status=PredictionStatus.pending,
        created_at=now,
        age=payload.age,
        revenu_mensuel=payload.revenu_mensuel,
        annees_dans_l_entreprise=payload.annees_dans_l_entreprise,
        frequence_deplacement=payload.frequence_deplacement.value,
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
        request_id=request_uuid,
        status=PredictionStatus.pending,
        created_at=now,
    )


# ============================================================
# GET PREDICTION RESULT (POLLING)
# GET /predictions/{request_id}
# ============================================================
@router.get(
    "/{request_id}",
    response_model=PredictionResultResponse,
)
async def get_prediction_result(
    request_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Récupère le statut et le résultat d'une prédiction.
    Utilisé par le dashboard (polling).
    """

    stmt_request = select(PredictionRequest).where(
        PredictionRequest.request_id == str(request_id)
    )
    result_request = await session.execute(stmt_request)
    prediction_request = result_request.scalar_one_or_none()

    if prediction_request is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction request not found",
        )

    stmt_result = select(PredictionResult).where(
        PredictionResult.request_id == prediction_request.id
    )
    result_result = await session.execute(stmt_result)
    prediction_result = result_result.scalar_one_or_none()

    # Résultat non encore calculé
    if prediction_result is None:
        return PredictionResultResponse(
            request_id=prediction_request.request_id,
            status=prediction_request.status,
            created_at=prediction_request.created_at,
        )

    # Résultat disponible
    return PredictionResultResponse(
        request_id=prediction_request.request_id,
        status=PredictionStatus.completed,
        prediction=prediction_result.prediction,
        probability=prediction_result.probability,
        created_at=prediction_result.created_at,
    )


# ============================================================
# PREDICTION HISTORY
# GET /predictions/history
# ============================================================
@router.get(
    "/history",
    response_model=List[PredictionResultResponse],
)
async def get_prediction_history(
    limit: int = Query(50, ge=1, le=500),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Retourne l'historique des prédictions terminées.
    Utilisé par la page 'Prediction History' du dashboard.
    """

    stmt = (
        select(PredictionResult)
        .order_by(PredictionResult.created_at.desc())
        .limit(limit)
    )

    result = await session.execute(stmt)
    results = result.scalars().all()

    history: List[PredictionResultResponse] = []

    for r in results:
        history.append(
            PredictionResultResponse(
                request_id=str(r.request_id),
                status=PredictionStatus.completed,
                prediction=r.prediction,
                probability=r.probability,
                created_at=r.created_at,
            )
        )

    return history
