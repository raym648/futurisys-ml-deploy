# futurisys-ml-deploy/src/db/models.py

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Dict, Optional

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# ============================================================
# Base SQLAlchemy 2.0
# ============================================================
class Base(DeclarativeBase):
    pass


# ============================================================
# Prediction Request (DB-first)
# ============================================================
class PredictionRequest(Base):
    __tablename__ = "prediction_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    model_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    inputs: Mapped[Dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="PENDING",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # ---- Relation 1–1 vers PredictionResult
    result: Mapped[Optional["PredictionResult"]] = relationship(
        back_populates="request",
        uselist=False,
        cascade="all, delete-orphan",
    )


# ============================================================
# Prediction Result
# ============================================================
class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("prediction_requests.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    prediction: Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )

    probability: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    model_name: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    model_version: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # ---- Relation inverse
    request: Mapped["PredictionRequest"] = relationship(
        back_populates="result",
    )
