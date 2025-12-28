# futurisys-ml-deploy/src/api/routes/predictions.py

"""
Routes de gestion des prédictions ML (DB-first).
- Soumission de requêtes de prédiction
- Consultation des résultats (polling)
- Historique des prédictions
- Aucune inférence ML n'est exécutée ici
"""

from datetime import UTC, datetime
from time import perf_counter
from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.schemas.input import PredictionInput
from src.api.schemas.output import (  # fmt: off; fmt: on;
    PredictionResultResponse,
)
from src.db.session import get_async_session
from src.ml.inference import run_inference
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
    response_model=PredictionResultResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_prediction_request(
    payload: PredictionInput,
    model_name: str = Query("default"),
    session: AsyncSession = Depends(get_async_session),
):
    request_uuid = str(uuid4())
    now = datetime.now(UTC)

    # 1️⃣ Create request
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
    await session.flush()  # 🔑 get DB id

    # 2️⃣ Run inference
    start = perf_counter()

    result = run_inference(
        payload.dict(),
        model_name=model_name,
    )

    latency_ms = (perf_counter() - start) * 1000

    prediction = result["prediction"]
    probability = result["probability"]

    # 3️⃣ Save result
    prediction_result = PredictionResult(
        request_id=prediction_request.id,
        prediction=prediction,
        probability=probability,
        latency_ms=latency_ms,
        created_at=now,
    )

    session.add(prediction_result)

    # 4️⃣ Update status
    prediction_request.status = PredictionStatus.completed

    # 5️⃣ Commit transaction
    await session.commit()

    return PredictionResultResponse(
        request_id=request_uuid,
        status=PredictionStatus.completed.value,
        prediction=prediction,
        probability=probability,
        created_at=now,
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
    stmt = (
        select(PredictionResult)
        .options(selectinload(PredictionResult.request))
        .order_by(PredictionResult.created_at.desc())
        .limit(limit)
    )

    result = await session.execute(stmt)
    results = result.scalars().all()

    history: List[PredictionResultResponse] = []

    for r in results:
        history.append(
            PredictionResultResponse(
                request_id=r.request.request_id,  # ✅ SAFE maintenant
                status=PredictionStatus.completed.value,
                prediction=r.prediction,
                probability=r.probability,
                created_at=r.created_at,
            )
        )

    return history


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
        status=PredictionStatus.completed.value,
        prediction=prediction_result.prediction,
        probability=prediction_result.probability,
        created_at=prediction_result.created_at,
    )
