# futurisys-ml-deploy/src/api/routes/dataset.py

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.data.models_db import Dataset

router = APIRouter(prefix="/dataset", tags=["Dataset"])


@router.get("/")
def list_datasets(
    source_file: Optional[str] = Query(
        None,
        description="Filtrer par nom de fichier",
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    query = db.query(Dataset)

    if source_file:
        query = query.filter(Dataset.source_file == source_file)

    query = query.order_by(Dataset.created_at.desc())

    results = query.offset(skip).limit(limit).all()

    return [
        {
            "dataset_id": d.dataset_id,
            "source_file": d.source_file,
            "payload": d.payload,
            "meta": d.meta,
            "created_at": d.created_at,
        }
        for d in results
    ]


@router.get("/{dataset_id}")
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = (
        # fmt: off
        db.query(Dataset)
        .filter(Dataset.dataset_id == dataset_id)
        .first()
        # fmt: on
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset non trouvé",
        )

    return {
        "dataset_id": dataset.dataset_id,
        "source_file": dataset.source_file,
        "payload": dataset.payload,
        "meta": dataset.meta,
        "created_at": dataset.created_at,
    }
