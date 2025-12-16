# futurisys-ml-deploy/src/api/routes/metadata.py

from fastapi import APIRouter

from src.ml.model_registry import METADATA

router = APIRouter(prefix="/metadata", tags=["metadata"])


@router.get("/")
def get_metadata():
    """
    Retourne les métadonnées complètes des artefacts ML.
    Lecture seule.
    """
    return METADATA
