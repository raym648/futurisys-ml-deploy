# futurisys-ml-deploy/src/workers/prediction_worker.py

import asyncio
from datetime import UTC, datetime

from sqlalchemy import select

from src.db.session import get_async_session
from src.ml.inference import run_inference
from src.ml.model_registry import get_metadata
from src.models.enums import PredictionStatus
from src.models.prediction_request import PredictionRequest
from src.models.prediction_result import PredictionResult

# from sqlalchemy.ext.asyncio import AsyncSession


POLL_INTERVAL = 5  # secondes


async def _run_inference_async(payload: dict) -> tuple[int, float]:
    """
    Exécute l'inférence ML dans un thread pour ne pas bloquer l'event loop.
    """
    return await asyncio.to_thread(run_inference, payload)


async def process_pending_requests():
    # ✅ conforme à ton architecture
    async for session in get_async_session():
        stmt = select(PredictionRequest).where(
            PredictionRequest.status == PredictionStatus.pending
        )

        result = await session.execute(stmt)
        requests = result.scalars().all()

        if not requests:
            return

        metadata = get_metadata()

        for req in requests:
            try:
                # 1️⃣ Inference ML (non bloquante)
                prediction, probability = await _run_inference_async(  # noqa: E501
                    {
                        "age": req.age,
                        "revenu_mensuel": req.revenu_mensuel,
                        "annees_dans_l_entreprise": req.annees_dans_l_entreprise,  # noqa: E501
                        "frequence_deplacement": req.frequence_deplacement,
                    }
                )

                # 2️⃣ Écriture du résultat
                prediction_result = PredictionResult(
                    request_id=req.id,
                    prediction=prediction,
                    probability=probability,
                    model_name=metadata.get("model_name"),
                    model_version=metadata.get("version"),
                    created_at=datetime.now(UTC),
                )

                session.add(prediction_result)

                # 3️⃣ Mise à jour statut
                req.status = PredictionStatus.completed

                await session.commit()

            except Exception as e:
                await session.rollback()
                req.status = PredictionStatus.failed
                await session.commit()
                print(f"[WORKER ERROR] request_id={req.request_id} → {e}")


async def main():
    while True:
        await process_pending_requests()
        await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
