# futurisys-ml-deploy/src/models/prediction_result.py

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.prediction_request import PredictionRequest


class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id: Mapped[int] = mapped_column(primary_key=True)

    request_id: Mapped[int] = mapped_column(
        ForeignKey("prediction_requests.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    prediction: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    latency_ms: Mapped[float | None]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    # Relation inverse 1–1
    request: Mapped["PredictionRequest"] = relationship(
        back_populates="result",
    )
