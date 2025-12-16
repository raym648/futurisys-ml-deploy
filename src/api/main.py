# futurisys-ml-deploy/src/api/main.py


from fastapi import FastAPI

from src.api.routes.dataset import router as dataset_router
from src.api.routes.metadata import router as metadata_router
from src.api.routes.metrics import router as metrics_router
from src.api.routes.models import router as models_router
from src.api.routes.predict import router as predict_router

app = FastAPI(
    title="Futurisys ML API",
    description="API MLOps – Dataset, Prediction & Artefacts",
    version="1.1.0",
)

# ============================================================
# Routes datasets
# ============================================================

app.include_router(dataset_router, prefix="/dataset", tags=["dataset"])

# ============================================================
# Routes ML prediction
# ============================================================

app.include_router(predict_router, prefix="/predict", tags=["prediction"])

# ============================================================
# Routes metadata (artefacts)
# ============================================================

app.include_router(metadata_router, prefix="/metadata", tags=["metadata"])

# ============================================================
# Routes models registry
# ============================================================

app.include_router(models_router, prefix="/models", tags=["models"])

# ============================================================
# Routes metrics
# ============================================================

app.include_router(metrics_router, prefix="/metrics", tags=["metrics"])

# ============================================================
# Root / health
# ============================================================


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "futurisys-ml-api"}
