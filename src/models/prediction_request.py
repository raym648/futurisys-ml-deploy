# futurisys-ml-deploy/src/models/prediction_request.py

from datetime import datetime
from typing import TYPE_CHECKING

# from sqlalchemy import DateTime, Enum, Float, Integer, String
from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.models.enums import PredictionStatus

if TYPE_CHECKING:
    from src.models.prediction_result import PredictionResult


class PredictionRequest(Base):
    __tablename__ = "prediction_requests"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Métadonnées
    request_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        index=True,
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[PredictionStatus] = mapped_column(
        Enum(PredictionStatus),
        default=PredictionStatus.pending,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    # Features ML
    age: Mapped[int]
    revenu_mensuel: Mapped[float]
    annees_dans_l_entreprise: Mapped[int]
    frequence_deplacement: Mapped[str]

    # Relation 1–1
    result: Mapped["PredictionResult"] = relationship(
        back_populates="request",
        uselist=False,
        cascade="all, delete-orphan",
    )
