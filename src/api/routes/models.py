# futurisys-ml-deploy/src/api/routes/models.py


from fastapi import APIRouter

from src.ml.model_registry import DEFAULT_MODEL_NAME, MODELS

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/")
def list_models():
    """
    Liste les modèles disponibles dans le registry.
    """
    return {
        "available_models": list(MODELS.keys()),
        "default_model": DEFAULT_MODEL_NAME,
    }
